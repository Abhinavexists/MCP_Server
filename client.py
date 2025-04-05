import asyncio
import sys
import os
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.sessions: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

        # Configure Gemini with API key from .env
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # Placeholder for chat and model
        self.model = None
        self.chat = None

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script should be a .py or .js file")
        
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env = None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.sessions = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.sessions.initialize()

        # List available tools
        response = await self.sessions.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:",[tool.name for tool in tools])

        available_tools = []
        for tool in tools:
            tool_definition = {
                "function_declarations": [
                    {
                        "name": tool.name,
                        "description": tool.description
                    }
                ]
            }
            available_tools.append(tool_definition)

        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            tools=available_tools
        )

        self.chat = self.model.start_chat()

    async def process_query(self, query: str) -> str:
        """Process a query using Gemini and available tools"""
        
        # Process response and handle tool calls
        final_text = []
        
        response = self.chat.send_message(
            query,
            generation_config={"max_output_tokens": 1000}
        )

        for part in response.parts:
            if part.text:
                final_text.append(part.text)

        return "\n".join(final_text)
    
    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
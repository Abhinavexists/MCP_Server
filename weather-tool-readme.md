# Weather Tool MCP Client

A command-line tool that provides access to US weather data through a client-server architecture using the Model Context Protocol (MCP) and Google's Gemini AI.

## Overview

This project connects a Python client application with a weather data server, allowing users to query weather information using natural language. The server communicates with the National Weather Service API to retrieve weather alerts and forecasts.

## Features

- Query weather alerts for US states using state codes
- Get detailed weather forecasts for specific locations using latitude and longitude
- Natural language interface powered by Google's Gemini AI
- Client-server architecture using Model Context Protocol (MCP)

## Prerequisites

- Python 3.8+
- Node.js (if running JavaScript server)
- Google Gemini API key
- uv package manager (required)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weather-tool.git
   cd weather-tool
   ```

2. Install uv if you don't have it already:
   ```
   pip install uv
   ```

3. Create and activate a virtual environment:
   ```
   uv venv
   ```
   - On Windows: `.venv\Scripts\activate`
   - On macOS/Linux: `source .venv/bin/activate`

4. Install dependencies using uv (this project uses uv.lock and pyproject.toml):
   ```
   uv pip sync
   ```

5. Create a `.env` file in the project root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

1. Start the client and connect to the weather server:
   ```
   python client.py server.py
   ```

2. Once connected, you can ask questions about weather information:
   ```
   Query: What are the current weather alerts in CA?
   Query: What's the forecast for latitude 37.7749, longitude -122.4194?
   ```

3. Type `quit` to exit the application.

## About uv Dependency Management

This project uses `uv` for dependency management with the following configuration files:
- `pyproject.toml`: Defines project metadata and dependencies
- `uv.lock`: Locks dependency versions for reproducible environments

Using `uv` instead of pip is required to ensure consistent dependencies and proper project setup.

## Available Tools

The server provides the following tools:

- **get_alerts**: Fetches weather alerts for a specified US state (using two-letter state code)
- **get_forecast**: Retrieves weather forecasts for a specific location (using latitude and longitude)

## Project Structure

- `client.py`: MCP client that connects to the server and processes user queries using Gemini AI
- `server.py`: MCP server that implements weather data tools and communicates with the National Weather Service API
- `pyproject.toml`: Project configuration and dependencies
- `uv.lock`: Locked dependency versions

## Error Handling

The application includes robust error handling for:
- Invalid server script paths
- Connection issues with the NWS API
- Invalid or missing data in API responses

## Future Improvements

- Add additional weather data endpoints
- Implement caching for frequently requested data
- Add support for location name lookup (instead of requiring lat/long)
- Create a web interface

## License

[MIT License](LICENSE)

## Acknowledgements

- National Weather Service for providing the weather data API
- Google for the Gemini AI API
- The MCP SDK developers

## Resources

For more information about Model Context Protocol (MCP), refer to the official Claude MCP documentation:
- [Claude MCP Documentation](https://docs.anthropic.com/claude/docs/model-context-protocol-mcp)
- [Claude MCP GitHub](https://github.com/anthropics/anthropic-tools)

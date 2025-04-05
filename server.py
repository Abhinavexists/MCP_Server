from typing import Any # disables typechecking
import httpx
from mcp.server.fastmcp import FastMCP

# initialise FastMCP server
mcp = FastMCP("weather")

# constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# helper function
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""   
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json0"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """Format the alert message into a readable string"""
    props = feature["properties"]
    return f"""
    Event: {props.get('event','unknown')}
    Area: {props.get('areaDesc','unknown')}
    Severity: {props.get('severity', 'unknown')}
    Description: {props.get('description', 'No description avaliable')}
    Instruction: {props.get('Instruction', 'No specific Instruction provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Get weather alert for US states.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "feature" not in data:
        return "Unable to fetch alerts or no alerts found"
    
    if not data["features"]:
        return "No active alerts for this state"
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forcast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    #  First get the forcast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch frocast data for this location"
    
    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forcast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast"
    
    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:
        forecast = f"""
        {period['name']}:
        Temperature: {period['temperature']}°{period['temperatureUnit']}
        Wind: {period['windSpeed']} {period['windDirection']}
        Forecast: {period['detailedForecast']}
        """
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

if __name__ == "__main__":
# Initialse and run the server
    mcp.run(transport='stdio')
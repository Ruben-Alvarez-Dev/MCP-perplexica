#!/usr/bin/env python3
"""MCP Vane Server - Auto-discovers Vane (Perplexica) port"""

import json
import logging
import os
from typing import Optional, Literal

import httpx
from mcp.server.fastmcp import FastMCP
from tavily import AsyncTavilyClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER_PORT = 8082

DEFAULT_PORTS = [3001, 3000]
FALLBACK_PORTS = [10301, 8000, 8001, 5000, 8080]
VANE_ENDPOINTS = ["/health", "/api/search", "/api/status", "/docs"]

mcp = FastMCP("vane-mcp", port=SERVER_PORT, sse_path="/sse", message_path="/messages/")


def discover_port(
    ports: list[int], endpoints: list[str], timeout: float = 2.0
) -> Optional[str]:
    """Scan ports for a responsive endpoint."""
    for port in ports:
        try:
            client = httpx.Client(timeout=timeout)
            for endpoint in endpoints:
                try:
                    resp = client.get(f"http://localhost:{port}{endpoint}")
                    if resp.status_code < 500:
                        logger.info(f"Discovered Vane on port {port}")
                        return f"http://localhost:{port}"
                except Exception:
                    continue
        except Exception:
            continue
    return None


def prompt_user(service_name: str, default_port: int) -> str:
    """Prompt user for port if not discovered."""
    try:
        user_input = input(
            f"\n⚠️  Could not find {service_name}.\n"
            f"   Default port: {default_port}\n"
            f"   Enter port number (or press Enter for default): "
        ).strip()
        if user_input:
            return f"http://localhost:{user_input}"
    except (EOFError, KeyboardInterrupt):
        pass
    return f"http://localhost:{default_port}"


def get_base_url() -> str:
    """Get base URL: env var -> discover -> prompt user -> fallback."""
    env_url = os.getenv("VANE_BASE_URL")
    if env_url:
        return env_url

    discovered = discover_port(DEFAULT_PORTS, VANE_ENDPOINTS)
    if discovered:
        return discovered

    logger.warning("Vane not found in default ports, trying fallback...")
    discovered = discover_port(FALLBACK_PORTS, VANE_ENDPOINTS, timeout=1.0)
    if discovered:
        return discovered

    return prompt_user("Vane (Perplexica)", 3001)


VANE_BASE_URL = get_base_url()
logger.info(f"Targeting Vane at: {VANE_BASE_URL}")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client: Optional[AsyncTavilyClient] = None
if TAVILY_API_KEY:
    tavily_client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
    logger.info("Tavily search enabled")
else:
    logger.warning("TAVILY_API_KEY not set — tavily_search tool will be unavailable")


@mcp.tool()
async def vane_search(
    query: str, mode: Literal["speed", "balanced", "quality"] = "balanced"
) -> str:
    """Search using Vane (Perplexica) for quick Q&A with sources

    Args:
        query: The search query
        mode: Search mode - speed (fast), balanced (default), quality (deep)
    """
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{VANE_BASE_URL}/api/search", json={"query": query, "mode": mode}
            )
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
    except httpx.HTTPError as e:
        logger.error(f"Vane API error: {e}")
        return json.dumps({"error": str(e), "sources": [], "success": False})


@mcp.tool()
async def tavily_search(
    query: str,
    search_depth: Literal["basic", "advanced"] = "advanced",
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
) -> str:
    """Search using Tavily for web results optimised for LLMs

    Args:
        query: The search query (max 400 chars)
        search_depth: basic (fast, 1 credit) or advanced (thorough, 2 credits)
        max_results: Number of results to return (1-20)
        topic: Search category — general, news, or finance
    """
    if tavily_client is None:
        return json.dumps({"error": "TAVILY_API_KEY is not configured", "results": []})
    try:
        response = await tavily_client.search(
            query=query[:400],
            search_depth=search_depth,
            max_results=max_results,
            topic=topic,
        )
        return json.dumps(response, indent=2)
    except Exception as e:
        logger.error(f"Tavily API error: {e}")
        return json.dumps({"error": str(e), "results": []})


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting Vane MCP on port {SERVER_PORT}")
    uvicorn.run(
        mcp.streamable_http_app(), host="0.0.0.0", port=SERVER_PORT, log_level="info"
    )

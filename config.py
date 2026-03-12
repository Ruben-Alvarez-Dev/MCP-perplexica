"""Configuration module for MCP Vane server."""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration for MCP Vane server."""

    def __init__(self) -> None:
        """Initialize configuration from environment variables."""
        self.vane_base_url: str = os.getenv("VANE_BASE_URL", "http://localhost:10301")
        port_str = os.getenv("SERVER_PORT")
        self.server_port: Optional[int] = int(port_str) if port_str else None
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def get_vane_url(self, endpoint: str) -> str:
        """Build full URL for Vane API endpoint."""
        base = self.vane_base_url.rstrip("/")
        endpoint = endpoint.lstrip("/")
        return f"{base}/{endpoint}"

    def validate(self) -> bool:
        """Validate configuration."""
        return bool(self.vane_base_url)


def get_config() -> Config:
    """Get configuration instance."""
    return Config()

from fastmcp import FastMCP
from src.config.settings import settings

# Instância do servidor FastMCP dedicado ao TheHive
mcp = FastMCP(settings.FAST_MCP_NAME)

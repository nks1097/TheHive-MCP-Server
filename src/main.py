import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.utils.logger import logger
from src.config.settings import settings
from src.tools.server import mcp
import src.tools.thehive_tools

def run():
    """Run the dedicated TheHive FastMCP server."""
    os.environ["FASTMCP_SHOW_SERVER_BANNER"] = "false"
    logger.info(f"Starting {settings.FAST_MCP_NAME} with {len(mcp._tools if hasattr(mcp, '_tools') else [])} tools...")
    try:
        mcp.run(show_banner=False)
    except Exception as e:
        logger.error(f"Server crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()

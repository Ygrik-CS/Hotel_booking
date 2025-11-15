"""Tests package."""
import sys
from pathlib import Path

# Add server directory to path for imports
server_dir = Path(__file__).parent.parent
sys.path.insert(0, str(server_dir))

import sys
import os

# Add parent directory to path so imports like `import init_db` work seamlessly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# HCLHackathon2025/conftest.py

import sys
from pathlib import Path

# Add the project root directory (HCLHackathon2025) to the Python path
# so that the 'backend' package can be imported correctly.
sys.path.insert(0, str(Path(__file__).parent))
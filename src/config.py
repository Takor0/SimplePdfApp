import os
from pathlib import Path

UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", "/tmp/uploads"))
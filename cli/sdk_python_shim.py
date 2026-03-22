from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SDK_SRC = ROOT / "sdk-python" / "src"
if str(SDK_SRC) not in sys.path:
    sys.path.insert(0, str(SDK_SRC))

from dsg import DSGClient  # noqa: E402


def get_client(base_url: str) -> DSGClient:
    return DSGClient(base_url=base_url)

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
REF_APP = ROOT / "reference-node" / "app"
if str(REF_APP) not in sys.path:
    sys.path.insert(0, str(REF_APP))

from settings import get_settings  # noqa: E402
from policy_validation import validate_policy  # noqa: E402


def load_policy_file(path: Path) -> dict:
    settings = get_settings()
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        data: dict = {}
        current_list_key: str | None = None
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.endswith(":"):
                current_list_key = line[:-1].strip()
                data[current_list_key] = []
                continue
            if line.startswith("-") and current_list_key:
                data[current_list_key].append(line[1:].strip())
        return data
    import json
    return json.loads(text)

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List


class AppendOnlyLedger:
    def __init__(self) -> None:
        self.chain: List[Dict] = []

    def append(self, data: Dict) -> str:
        prev_hash = self.chain[-1]["hash"] if self.chain else "0" * 64
        record = {
            "data": data,
            "prev_hash": prev_hash,
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        content = json.dumps(record, sort_keys=True).encode()
        record["hash"] = hashlib.sha256(content).hexdigest()
        self.chain.append(record)
        return record["hash"]

    def verify_chain(self) -> bool:
        for index, node in enumerate(self.chain):
            prev_hash = self.chain[index - 1]["hash"] if index > 0 else "0" * 64
            if node["prev_hash"] != prev_hash:
                return False
            data_to_verify = {k: v for k, v in node.items() if k != "hash"}
            content = json.dumps(data_to_verify, sort_keys=True).encode()
            if node["hash"] != hashlib.sha256(content).hexdigest():
                return False
        return True

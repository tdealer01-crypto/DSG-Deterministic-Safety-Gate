export interface DSGRequest {
  version: string;
  agent: string;
  state_next: Record<string, unknown>;
  signals: number[];
  nonce: string;
}

export interface DSGResponse {
  decision: 'ALLOW' | 'STABILIZE' | 'BLOCK';
  phase: 'UNITY' | 'TUNING' | 'CHAOS';
  stability: number;
  entropy: number;
  proof_hash: string;
  reasons: string[];
  ledger_hash: string;
  version: string;
}

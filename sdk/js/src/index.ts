import { DSGRequest, DSGResponse } from './types';

export class DSGClient {
  constructor(private endpoint: string, private version: string = '1.0.0') {}

  private genNonce(): string {
    return Array.from(globalThis.crypto.getRandomValues(new Uint8Array(16)))
      .map((b) => b.toString(16).padStart(2, '0'))
      .join('');
  }

  async evaluate(
    agent: string,
    state: Record<string, unknown>,
    signals: number[],
  ): Promise<DSGResponse> {
    const payload: DSGRequest = {
      version: this.version,
      agent,
      state_next: state,
      signals,
      nonce: this.genNonce(),
    };

    const response = await fetch(`${this.endpoint}/evaluate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error(`DSG_HTTP_ERROR: ${response.status}`);
    }

    return response.json() as Promise<DSGResponse>;
  }
}

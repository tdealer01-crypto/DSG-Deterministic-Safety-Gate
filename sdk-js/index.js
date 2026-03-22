export class DSGClient {
  constructor(baseUrl = 'http://localhost:8000', apiKey = null) {
    this.baseUrl = baseUrl.replace(/\/$/, '')
    this.apiKey = apiKey
  }

  headers() {
    return this.apiKey ? { 'x-api-key': this.apiKey, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' }
  }

  async health() {
    const res = await fetch(`${this.baseUrl}/health`)
    return res.json()
  }

  async metrics() {
    const res = await fetch(`${this.baseUrl}/metrics`, { headers: this.headers() })
    return res.json()
  }

  async ledger() {
    const res = await fetch(`${this.baseUrl}/ledger`, { headers: this.headers() })
    return res.json()
  }

  async execute(agentId, action, payload = {}) {
    const res = await fetch(`${this.baseUrl}/execute`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify({ agent_id: agentId, action, payload }),
    })
    return res.json()
  }
}

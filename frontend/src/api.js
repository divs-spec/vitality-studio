const BASE = process.env.VITALITY_BACKEND_URL || 'http://localhost:8000'

export async function generate(prompt, messages = [], preferred = null) {
  const body = { prompt, messages, preferred }
  const res = await fetch(`${BASE}/generate/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const txt = await res.text()
    throw new Error(`Generate API error: ${res.status} ${txt}`)
  }
  return res.json()
}

export async function execute(language, code) {
  const body = { language, code }
  const res = await fetch(`${BASE}/execute/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const txt = await res.text()
    throw new Error(`Execute API error: ${res.status} ${txt}`)
  }
  return res.json()
}

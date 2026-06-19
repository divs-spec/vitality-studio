import React, { useState } from 'react'
import { execute } from '../api'

export default function ExecutorPanel() {
  const [code, setCode] = useState('// write code to execute')
  const [lang, setLang] = useState('python')
  const [result, setResult] = useState(null)
  const [running, setRunning] = useState(false)

  async function run() {
    setRunning(true)
    try {
      const r = await execute(lang, code)
      setResult(r)
    } catch (err) {
      setResult({ stderr: err.message })
    } finally {
      setRunning(false)
    }
  }

  return (
    <div>
      <div>
        <label>Language:</label>
        <select value={lang} onChange={(e) => setLang(e.target.value)}>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
        </select>
      </div>
      <textarea value={code} onChange={(e) => setCode(e.target.value)} rows={10} style={{ width: '100%', marginTop: 8 }} />
      <div style={{ marginTop: 8 }}>
        <button onClick={run} disabled={running}>Execute</button>
      </div>
      {result && (
        <div style={{ marginTop: 12 }}>
          <h4>Result</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

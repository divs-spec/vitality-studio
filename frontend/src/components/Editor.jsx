import React, { useState } from 'react'
import MessageList from './MessageList'
import { generate } from '../api'

export default function Editor() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([
    { role: 'system', text: 'You are Vitality Assistant.' },
  ])
  const [loading, setLoading] = useState(false)

  async function send() {
    if (!input.trim()) return
    const userMsg = { role: 'user', text: input }
    const newMessages = [...messages, userMsg]
    setMessages(newMessages)
    setInput('')
    setLoading(true)
    try {
      const res = await generate(input, newMessages, 'openai')
      // backend returns provider and response object
      let assistantText = ''
      if (res && res.response) {
        // res.response may be nested; support simple echo stub
        assistantText = res.response.response || res.response
      }
      const assistantMsg = { role: 'assistant', text: assistantText }
      setMessages((m) => [...m, assistantMsg])
    } catch (err) {
      setMessages((m) => [...m, { role: 'assistant', text: `Error: ${err.message}` }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <MessageList messages={messages} />
      <div style={{ marginTop: 12 }}>
        <textarea value={input} onChange={(e) => setInput(e.target.value)} rows={4} style={{ width: '100%' }} />
        <div style={{ marginTop: 8 }}>
          <button onClick={send} disabled={loading}>Send</button>
        </div>
      </div>
    </div>
  )
}

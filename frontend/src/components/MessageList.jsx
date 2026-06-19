import React from 'react'

export default function MessageList({ messages = [] }) {
  return (
    <div className="messages">
      {messages.map((m, i) => (
        <div key={i} className={`msg ${m.role}`}>
          <strong>{m.role}:</strong> <span>{m.text}</span>
        </div>
      ))}
    </div>
  )
}

import React from 'react'
import Sidebar from './components/Sidebar'
import Editor from './components/Editor'
import ExecutorPanel from './components/ExecutorPanel'

export default function App() {
  return (
    <div className="app">
      <aside className="sidebar"><Sidebar /></aside>
      <main className="center"><Editor /></main>
      <aside className="right"><ExecutorPanel /></aside>
    </div>
  )
}

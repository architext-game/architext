import { useState, useEffect, useRef } from 'react'
import './App.css'
import { Login } from "./verbs/Login";
import { Verb } from './verbs/AbstractVerb';
import { useProcess } from './stupidLogic';

function App() {
  const [messages, setMessages] = useState<string[]>([])
  const [inputValue, setInputValue] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  const addServerMessage = (message: string) => {
    setMessages((prevMessages) => [...prevMessages, message])
  }
  const process = useProcess({ toClient: addServerMessage })

  const addUserMessage = () => {
    if (inputValue.trim() !== '') {
      setMessages((prevMessages) => [...prevMessages, inputValue])
      const newContext = process(inputValue)
      setInputValue('')
    }
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      addUserMessage()
    }
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="flex flex-col h-screen justify-end">
      <div className="flex-1 overflow-auto p-4 space-y-2">
        {messages.map((message, index) => (
          <div key={index} className="bg-gray-200 rounded p-2">
            {message}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div className="p-4 bg-white border-t-2 border-gray-200">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          className="p-2 border rounded w-full"
          placeholder="Type a message"
        />
        <button
          onClick={addUserMessage}
          className="bg-blue-500 text-white p-2 rounded w-full mt-2"
        >
          Add message
        </button>
      </div>
    </div>
  )
}

export default App

import { useState, useEffect, useRef } from 'react'
import './App.css'
import io from 'socket.io-client';
import { DefaultEventsMap } from '@socket.io/component-emitter';
import { Socket } from 'socket.io-client';

const SOCKET_SERVER_URL = 'http://localhost:5000';

function App() {
  const [messages, setMessages] = useState<string[]>([])
  const [inputValue, setInputValue] = useState('')
  const [socket, setSocket] = useState<Socket<DefaultEventsMap, DefaultEventsMap> | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null)

  const addServerMessage = (message: string) => {
    setMessages((prevMessages) => [...prevMessages, message.replace(/^\n|\n$/g, '')])
  }

  const addUserMessage = () => {
    socket?.emit('message', inputValue)
    setMessages((prevMessages) => [...prevMessages, inputValue])
    setInputValue('')
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      addUserMessage()
    }
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    const newSocket = io(SOCKET_SERVER_URL, /*{secure: true} TODO */);
    setSocket(newSocket);

    return () => { newSocket.disconnect() };
  }, []);

  useEffect(() => {
    if (socket) {
      socket.on('message', (message: string) => {
        console.log("reveived", message)
        addServerMessage(message)
      });

      socket.on('connect', () => {
        console.log("connected")
      });
    }
  }, [socket]);

  return (
    <div className=" bg-slate-800 w-screen h-screen text-white">
      <div className="flex flex-col h-screen justify-end max-w-3xl bg-slate-800 mx-auto">
        <div className="flex-1 overflow-auto p-4 space-y-2 whitespace-pre-wrap">
          {messages.map((message, index) => (
            <div key={index} className="rounded px-2 text-left font-console">
              {message}
            </div>
          ))}
          <div ref={bottomRef} />
        </div>
        <div className="p-4 border-t-2 border-gray-200">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            className="p-2 border rounded w-full bg-slate-800"
            placeholder="Type a message"
          />
        </div>
      </div>
    </div>
  )
}

export default App

"use client"; // Si estás usando app router en Next.js 13+

import { use, useEffect, useState } from "react";
import { authenticate, login, getWorlds, GetWorldsResponse, createWorld } from "@/architextSDK";
import { useStore } from "@/state";
import Link from "next/link";
import { useRouter } from 'next/navigation';

export default function Home() {
  const socket = useStore((state) => state.socket)
  const router = useRouter()
  const [getWorldsResponse, setGetWorldsResponse] = useState<GetWorldsResponse>()
  const [newWorldName, setNewWorldName] = useState('')
  const [error, setError] = useState('')

  async function updateWorlds(){
    setGetWorldsResponse(await getWorlds(socket, {}))
  }

  async function handleEnterWorld(worldId: string){
    router.push(`/world/${worldId}`)
  }

  useEffect(() => {
    if (socket) {
      socket.on('connect', async () => {
        console.log("connected, authenticating with jwt...")
        const jwt = localStorage.getItem("jwt")
        const response = await authenticate(socket, { jwt_token: jwt || '' })
        console.log("Authentication response: ", response)
        if(!response.success){
          console.log('Authentication error. Please go back to the login page')
          console.log(response.error || 'Unknown error')
        }
      });

      socket.on('connect_error', () => {
        console.log(`Error connecting to server. Check your connection. Contact oliverlsanz@gmail.com if the issue persists.`)
      });

      return () => { socket.removeAllListeners() }
    }
  }, [socket]);

  async function handleCreateWorldSubmit(e: React.FormEvent<HTMLFormElement>){
    e.preventDefault();
    const response = await createWorld(socket, { name: newWorldName, description: "Another world." })
    console.log(response)
    if(response.success) {
      router.push(`/world/${response.data?.world_id}`)
    } else {
      setError("Error: " + response.error)
    }
  }

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div>Elige a dónde ir</div>
        {
          getWorldsResponse?.data?.worlds.map(world => (
            <button onClick={() => handleEnterWorld(world.id)} key={world.id}>{world.name}</button>
          ))
        }
        <button onClick={updateWorlds}>
          [ Cargar mundos ]
        </button>

        <form onSubmit={handleCreateWorldSubmit} className="flex flex-col gap-4 w-full max-w-sm">
          {
            error &&
            <div>{error}</div>
          }
          <label htmlFor="worldname">Enter a new world</label>
          <input
            id="worldname"
            type="text"
            className="border border-gray-300 px-3 py-2 rounded"
            placeholder="Your world name"
            value={newWorldName}
            onChange={(e) => setNewWorldName(e.target.value)}
          />

          <button
            type="submit"
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
          >
            Enter
          </button>
        </form>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        Welcome to Architext
      </footer>
    </div>
  );
}

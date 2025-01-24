"use client"; // Si estás usando app router en Next.js 13+

import { use, useEffect, useState } from "react";
import { authenticate, login, getWorlds, GetWorldsResponse, createWorld, GetWorldTemplatesResponse, getWorldTemplates, requestWorldCreationFromTemplate, WorldTemplateListItem, getMe, GetMeResponse, createTemplate, enterWorld, getWorldTemplate } from "@/architextSDK";
import { useStore } from "@/state";
import Link from "next/link";
import { useRouter } from 'next/navigation';

export default function Home() {
  const socket = useStore((state) => state.socket)
  const router = useRouter()
  const [getWorldsResponse, setGetWorldsResponse] = useState<GetWorldsResponse>()
  const [getTemplatesResponse, setGetTemplatesResponse] = useState<GetWorldTemplatesResponse>()
  const [newWorldName, setNewWorldName] = useState('')
  const [worldCode, setWorldCode] = useState('')
  const [error, setError] = useState('')
  const [me, setMe] = useState<GetMeResponse>()

  useEffect(() => {
    getMe(socket, {}).then(meResponse => {
      setMe(meResponse)
      console.log(meResponse)
    })
  }, [socket])

  async function updateWorlds(){
    setGetWorldsResponse(await getWorlds(socket, {}))
    setGetTemplatesResponse(await getWorldTemplates(socket, {}))
  }

  // TODO: Esto no carga a veces porque no da tiempo al useeffect
  // de autenticar el socket a que lo haga. Claramente toda esta
  // página es una chapuza.
  useEffect(() => {
    getMe(socket, {}).then(meResponse => {
      setMe(meResponse)
      console.log(meResponse)
    })
    updateWorlds()
  }, [socket])

  async function handleEnterWorld(worldId: string){
    router.push(`/world/${worldId}`)
  }

  async function handleCreateTemplate(worldId: string, worldName: string, worldDescription: string){
    // Todo: smells like too much logic for the front...
    // but would like the core to be language agnostic.
    // Let's go with this for now.
    const templates = getTemplatesResponse
    const baseName = worldName
    let counter = 2
    let newTemplateName = baseName
    console.log(templates)
    while(templates?.data?.templates.some((t) => t.name === newTemplateName)){
      newTemplateName = `${baseName} ${counter}`
      counter++
    }
    const response = await createTemplate(socket, {
      name: newTemplateName,
      description: worldDescription,
      base_world_id: worldId
    })
    console.log(response)
    if(response.success){
      updateWorlds()
    }
  }

  async function handleEnterTemplate(template: WorldTemplateListItem){
    // TODO: smells like too much logic for the front...
    // but would like the core to be language agnostic.
    // Let's go with this for now.
    const me = await getMe(socket, {})
    const templates = await getWorlds(socket, {})
    const world_name_base = `${template.name} de ${me.data?.name}`
    let world_name = world_name_base
    let counter = 2
    while(templates.data?.worlds.some((w) => w.name === world_name)){
      world_name = `${world_name_base} ${counter}`
      counter++
    }
    const response = await requestWorldCreationFromTemplate(socket, {
      name: world_name,
      description: template.description,
      template_id: template.id
    })
    console.log(response)
    router.push(`/world/${response.data?.future_world_id}?future=true`)
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

  async function handleEnterWorldByCode(e: React.FormEvent<HTMLFormElement>){
    e.preventDefault();
    const enterWorldResponse = await enterWorld(socket, { world_id: worldCode })
    console.log(enterWorldResponse)
    if(enterWorldResponse.success) {
      router.push(`/world/${worldCode}`)
      return
    }
    const getTemplateResponse = await getWorldTemplate(socket, { template_id: worldCode })
    if(getTemplateResponse.success && getTemplateResponse.data){
      const template = getTemplateResponse.data
      handleEnterTemplate(template)
      return
    }
    console.log(`Error: Id ${worldCode} not found in worlds nor templates`)
    setError("World code is not valid")
  }

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div><b>Elige a dónde ir</b></div>
        {
          getWorldsResponse?.data?.worlds.map(world => (
            <div key={world.id} className="flex">
              <button onClick={() => handleEnterWorld(world.id)}>{world.name}</button>
              {
                world.owner && me && world.owner == me.data?.id &&
                <button onClick={() => handleCreateTemplate(world.id, world.name, world.description)} key={world.id}>[ Create Template ]</button>
              }
            </div>
          ))
        }
        <div><b>Templates</b></div>
        {
          getTemplatesResponse?.data?.templates.map(template => (
            <button onClick={() => handleEnterTemplate(template)} key={template.id}>{template.name}</button>
          ))
        }
        <button onClick={updateWorlds}><b>
          [ Refresh ]
        </b></button>

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

        <form onSubmit={handleEnterWorldByCode} className="flex flex-col gap-4 w-full max-w-sm">
          {
            error &&
            <div>{error}</div>
          }
          <label htmlFor="worldcode">Enter a world by its code</label>
          <input
            id="worldcode"
            type="text"
            className="border border-gray-300 px-3 py-2 rounded"
            placeholder="0000-0000-0000-0000"
            value={worldCode}
            onChange={(e) => setWorldCode(e.target.value)}
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

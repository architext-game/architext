"use client"; // Si estás usando app router en Next.js 13+

import { useEffect, useState } from "react";
import { authenticate, requestWorldCreationFromTemplate, getMe, GetMeResponse, enterWorld, getWorldTemplate } from "@/architextSDK";
import { useSocket, useStore } from "@/state";
import { useRouter } from 'next/navigation';
import { Header } from "@/components/header";
import { Card } from "@/components/card";
import { WorldsList } from "./worlds-list";
import { TemplatesList } from "./templates-list";
import { Overlay } from "@/components/overlay";
import { Button } from "@/components/button";
import { WorldByCodeOverlay } from "./world-by-code-overlay";

export default function Home() {
  const { socket, isAuthenticated } = useSocket()
  const router = useRouter()
  const [showCodeOverlay, setShowCodeOverlay] = useState(false)
  const [worldCode, setWorldCode] = useState('')
  const [worldByIdError, setWorldByIdError] = useState('')
  const [me, setMe] = useState<GetMeResponse>()
  const [expandedItem, setExpandedItem] = useState<string>()

  useEffect(() => {
    getMe(socket, {}).then(meResponse => {
      setMe(meResponse)
      console.log(meResponse)
    })
  }, [socket])

  useEffect(() => {
    if(!isAuthenticated){
      router.push('/login')
    }
  }, [isAuthenticated]);

  async function handleEnterTemplate({ name, description, id }: { name: string, description: string, id: string}){
    const response = await requestWorldCreationFromTemplate(socket, {
      name: name,
      description: description,
      template_id: id,
      // fixDuplicatedName: true
    })
    console.log(response)
    router.push(`/world/${response.data?.future_world_id}?future=true`)
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
    setWorldByIdError("World code is not valid")
  }

  function handleExpandedItem(key: string){
    if(key === expandedItem){
      setExpandedItem("")
    } else {
      setExpandedItem(key)
    }
  }

  return (
    <div className="flex flex-col items-center text-text font-mono  text-lg pb-40">
      <Header/>
      {
        showCodeOverlay &&
        <WorldByCodeOverlay 
          error={worldByIdError}
          onClose={() => {
            setShowCodeOverlay(false)
            setWorldByIdError("")
          }}
          onSubmit={handleEnterWorldByCode}
          setWorldCode={setWorldCode}
          worldCode={worldCode}
        />
      }
      <main className="flex flex-col gap-8 row-start-2 max-w-screen-md items-stretch">
        <Card>
        Welcome to Architext. This is a place where you can create and explore worlds made of words! Enter the Architexture Museum for a five minute tutorial.
        </Card>
        {
          me && 
          <>
          <WorldsList 
            router={router} 
            expandedItem={expandedItem} 
            onToggleExpanded={handleExpandedItem} 
            right={
              <button onClick={() => setShowCodeOverlay(true)} className="transition hover:underline text-sm"> 
                I have a Code
              </button>
            } 
          />
          <TemplatesList 
            router={router}
            expandedItem={expandedItem}
            onToggleExpanded={handleExpandedItem}
          />
          </>
        }
      </main>
    </div>
  );
}

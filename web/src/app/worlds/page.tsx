"use client"; // Si estás usando app router en Next.js 13+

import { useEffect, useState } from "react";
import { requestWorldCreationFromTemplate, enterWorld, getWorldTemplate } from "@/architextSDK";
import { useStore } from "@/state";
import { useRouter } from 'next/navigation';
import { Header } from "@/components/header";
import { Card } from "@/components/card";
import { WorldsList } from "./worlds-list";
import { TemplatesList } from "./templates-list";
import { WorldByCodeOverlay } from "./world-by-code-overlay";
import { Overlay } from "@/components/overlay";
import { EditWorldForm } from "../world/[world_id]/edit_world_form";
import { CreateTemplateForm } from "../world/[world_id]/create_template_form";

export default function Home() {
  const socket = useStore((state) => state.socket)
  const me = useStore((state) => state.me)
  const authChecked = useStore((state) => state.authChecked)
  const router = useRouter()
  const [showCodeOverlay, setShowCodeOverlay] = useState(false)
  const [worldCode, setWorldCode] = useState('')
  const [worldByIdError, setWorldByIdError] = useState('')
  const [expandedItem, setExpandedItem] = useState<string>()
  const [showEditWorldOverlay, setShowEditWorldOverlay] = useState(false)
  const [showCreateTemplateOverlay, setShowCreateTemplateOverlay] = useState(false)

  useEffect(() => {
    if(authChecked && !me?.success){
      router.push('/login')
    }
  }, [me, authChecked]);

  console.log(socket.id)

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

  function handleOpenCreateTemplate(key: string){
    setShowCreateTemplateOverlay(true)
  }

  function handleOpenSettings(key: string){
    setShowEditWorldOverlay(true)
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
            onOpenCreateTemplate={handleOpenCreateTemplate}
            onOpenSettings={handleOpenSettings}
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
      {
        showEditWorldOverlay && expandedItem &&
        <Overlay onClose={() => setShowEditWorldOverlay(false)}>
          <EditWorldForm id={expandedItem} onClose={() => setShowEditWorldOverlay(false)} />
        </Overlay>
      }
      {
        showCreateTemplateOverlay && expandedItem &&
        <Overlay onClose={() => setShowCreateTemplateOverlay(false)}>
          <CreateTemplateForm id={expandedItem} onClose={() => setShowCreateTemplateOverlay(false)} />
        </Overlay>
      }
    </div>
  );
}

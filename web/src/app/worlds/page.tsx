"use client";

import { useEffect, useState } from "react";
import { requestWorldCreationFromTemplate, enterWorld, getWorldTemplate, requestWorldImport } from "@/architextSDK";
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
import { ImportWorldOverlay } from "./import-world-overlay";
import { MissionsList } from "./missions_list";


export default function Home() {
  const socket = useStore((state) => state.socket)
  const router = useRouter()
  const [showCodeOverlay, setShowCodeOverlay] = useState(false)
  const [worldCode, setWorldCode] = useState('')
  const [worldByIdError, setWorldByIdError] = useState('')
  const [expandedItem, setExpandedItem] = useState<string>()
  const [showEditWorldOverlay, setShowEditWorldOverlay] = useState(false)
  const [showCreateTemplateOverlay, setShowCreateTemplateOverlay] = useState(false)
  // import state
  const [showImportOverlay, setShowImportOverlay] = useState(false)
  const [importName, setImportName] = useState('')
  const [importDescription, setImportDescription] = useState('')
  const [importText, setImportText] = useState('')
  const [importError, setImportError] = useState('')
  const authenticated = useStore((state) => state.authenticated)

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

  async function handleImportWorld(e: React.FormEvent<HTMLFormElement>){
    e.preventDefault();
    const requestImportResponse = await requestWorldImport(socket, {
      name: importName,
      description: importDescription,
      text_representation: importText,
      format: "plain",
    })
    console.log(requestImportResponse)
    // if(requestImportResponse.success) {
    //   router.push(`/world/${worldCode}`)
    //   return
    // }
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
      <Header className="mx-auto max-w-screen-md"/>
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
      {
        showImportOverlay &&
        <ImportWorldOverlay 
          error={importError}
          onClose={() => {
            setShowImportOverlay(false)
            setImportError("")
          }}
          onSubmit={handleImportWorld}
          name={importName}
          setName={setImportName}
          description={importDescription}
          setDescription={setImportDescription}
          textRepresentation={importText}
          setTextRepresentation={setImportText}
        />
      }
      <main className="flex flex-col gap-8 row-start-2 max-w-screen-md items-stretch">
        <Card>
        Welcome to Architext! This is a place where you can create and explore worlds made of words. <br/><br/> You might encounter some bugs and typos along the way. If you do, I’d really appreciate it if you could let me know. Thanks for playing!
        </Card>

        { authenticated &&  // should not try to load worlds until socket is authenticated
          <>
          <MissionsList router={router} />
          <WorldsList 
            router={router} 
            expandedItem={expandedItem} 
            onToggleExpanded={handleExpandedItem}
            onOpenCreateTemplate={handleOpenCreateTemplate}
            onOpenSettings={handleOpenSettings}
            right={
              <div className="flex gap-3 items-center">
                { false &&
                  <>
                  <button onClick={() => setShowImportOverlay(true)} className="transition hover:underline text-sm"> 
                    Import world
                  </button>
                  <div>-</div>
                  </>
                }
                <button onClick={() => setShowCodeOverlay(true)} className="transition hover:underline text-sm"> 
                 I have a Code 🔑
                </button>
              </div>
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

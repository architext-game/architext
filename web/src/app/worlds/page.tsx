// Versión refactorizada de `Home` con overlay único dinámico

"use client";

import { useEffect, useState } from "react";
import {
  requestWorldCreationFromTemplate,
  GetWorldsResponse,
  getWorlds,
  editWorld,
  getWorldTemplates,
  GetWorldTemplatesResponse,
  deleteWorld,
  editTemplate,
  deleteTemplate,
} from "@/architextSDK";
import { useStore } from "@/state";
import { useRouter } from "next/navigation";
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
import { WorldDetail } from "@/components/WorldDetail";
import { TemplateDetail } from "@/components/TemplateDetail";

export default function Home() {
  const socket = useStore((state) => state.socket);
  const router = useRouter();

  const [expandedItem, setExpandedItem] = useState<string>();
  const [editWorldMessage, setEditWorldMessage] = useState("");
  const [getWorldsResponse, setGetWorldsResponse] = useState<GetWorldsResponse>();
  const [getTemplatesResponse, setGetTemplatesResponse] = useState<GetWorldTemplatesResponse>();

  const [overlayContent, setOverlayContent] = useState<React.ReactNode>(null);
  const [isOverlayOpen, setIsOverlayOpen] = useState(false);

  function openOverlay(content: React.ReactNode) {
    setOverlayContent(content);
    setIsOverlayOpen(true);
  }

  function closeOverlay() {
    setIsOverlayOpen(false);
    setOverlayContent(null);
  }

  const authenticated = useStore((state) => state.authenticated);

  async function updateWorlds() {
    setGetWorldsResponse(await getWorlds(socket, {}));
  }

  async function updateTemplates(){
    setGetTemplatesResponse(await getWorldTemplates(socket, {}))
  }

  useEffect(() => {
    if (authenticated) {
      updateWorlds();
      updateTemplates();
    }
  }, [authenticated]);

  // async function handleEnterTemplate({ name, description, id }: { name: string; description: string; id: string }) {
  //   const response = await requestWorldCreationFromTemplate(socket, {
  //     name,
  //     description,
  //     template_id: id,
  //   });
  //   router.push(`/world/${response.data?.future_world_id}?future=true`);
  // }

  async function handleEnterTemplate(templateId: string){
    const template = getTemplatesResponse?.data?.templates.find((template) => template.id == templateId)
    if(!template){
      console.log(`handleEnterTemplate error: Template ${templateId} not found`)
      return
    }
    const response = await requestWorldCreationFromTemplate(socket, {
      name: template.name,
      description: template.description,
      template_id: template.id,
      // fixDuplicatedName: true
    })
    console.log(response)
    router.push(`/world/${response.data?.future_world_id}?future=true`)
  }

  async function handleEnterWorld(worldId: string) {
    router.push(`/world/${worldId}`);
  }

  function saveWorldChanges(id: string, newName: string, newDescription: string) {
    editWorld(socket, { world_id: id, name: newName, description: newDescription }).then((response) => {
      setEditWorldMessage(response.success ? "Changes saved." : "Error saving changes.");
      updateWorlds();
    });
  }

  function saveTemplateChanges(id: string, newName: string, newDescription: string) {
    editTemplate(socket, { template_id: id, name: newName, description: newDescription }).then((response) => {
      setEditWorldMessage(response.success ? "Changes saved." : "Error saving changes.");
      updateTemplates();
    });
  }

  function handleDeleteWorld(id: string) {
    deleteWorld(socket, { world_id: id }).then((response) => {
      updateWorlds();
    });
  }

  function handleDeleteTemplate(id: string) {
    deleteTemplate(socket, { template_id: id }).then((response) => {
      updateTemplates();
    });
  }

  function handleExpandedItem(key: string) {
    setExpandedItem(key === expandedItem ? "" : key);
  }

  return (
    <div className="flex flex-col items-center text-text font-mono text-lg pb-40 px-4 sm:px-6">
      <Header className="mx-auto max-w-screen-md mb-8 sm:mb-10" />

      <main className="flex flex-col gap-8 row-start-2 max-w-screen-md items-stretch">
        <Card className="text-sm">
          Welcome to Architext! This is a place where you can create and explore worlds made of words.
          <br />
          <br />
          You might encounter some bugs and typos along the way. If you do, I’d really appreciate it if you could let
          me know. Thanks for playing!
        </Card>

        {authenticated && (
          <>
            <MissionsList router={router} />
            {getWorldsResponse && (
              <WorldsList
                getWorldsResponse={getWorldsResponse}
                router={router}
                expandedItem={expandedItem}
                onToggleExpanded={handleExpandedItem}
                onOpenWorldDetail={() =>
                  openOverlay(
                    <WorldDetail
                      author={
                        getWorldsResponse?.data?.worlds.find((w) => w.id === expandedItem)?.owner_name || "Architext"
                      }
                      connectedPlayers={
                        getWorldsResponse?.data?.worlds.find((w) => w.id === expandedItem)?.connected_players_count || 0
                      }
                      name={getWorldsResponse?.data?.worlds.find((w) => w.id === expandedItem)?.name || ""}
                      description={getWorldsResponse?.data?.worlds.find((w) => w.id === expandedItem)?.description || ""}
                      worldShareCode={getWorldsResponse?.data?.worlds.find((w) => w.id === expandedItem)?.id || ""}
                      saveResultMessage={editWorldMessage}
                      onClose={closeOverlay}
                      onSaveChanges={(name, desc) => saveWorldChanges(expandedItem!, name, desc)}
                      onEnterWorld={() => handleEnterWorld(expandedItem!)}
                      onCreateTemplate={() =>
                        openOverlay(
                          <CreateTemplateForm
                            id={expandedItem!}
                            onClose={closeOverlay}
                            worldName={getWorldsResponse?.data?.worlds.find((w) => w.id === expandedItem)?.name || ""}
                            worldDescription={getWorldsResponse?.data?.worlds.find((w) => w.id === expandedItem)?.description || ""}
                            onCreateTemplate={(name, desc, templateId) => updateTemplates()}
                          />
                        )
                      }
                      onDeleteWorld={() => handleDeleteWorld(expandedItem!)}
                    />
                  )
                }
                onEnterWorld={handleEnterWorld}
                right={
                  <div className="flex gap-3 items-center">
                    <button onClick={() => openOverlay(
                      <ImportWorldOverlay 
                        error={""} 
                        onClose={closeOverlay} 
                        onSubmit={() => {}} 
                        name={""} 
                        setName={() => {}} 
                        description={""} 
                        setDescription={() => {}} 
                        textRepresentation={""} 
                        setTextRepresentation={() => {}} 
                      />
                    )} className="transition hover:underline text-sm">Import world</button>
                    <div>-</div>
                    <button onClick={() => openOverlay(
                      <WorldByCodeOverlay 
                        error={""} 
                        onClose={closeOverlay} 
                        onSubmit={() => {}} 
                        setWorldCode={() => {}} 
                        worldCode={""} 
                      />
                    )} className="transition hover:underline text-sm">
                      I have a Code 🔑
                    </button>
                  </div>
                }
              />
            )}
            { getTemplatesResponse &&
              <TemplatesList 
                router={router}
                expandedItem={expandedItem} 
                getTemplatesResponse={getTemplatesResponse}
                onEnterTemplate={handleEnterTemplate}
                onToggleExpanded={handleExpandedItem}
                onOpenTemplateDetail={() =>
                  openOverlay(
                    <TemplateDetail
                      author={
                        getTemplatesResponse?.data?.templates.find((w) => w.id === expandedItem)?.author_name || "Architext"
                      }
                      name={getTemplatesResponse?.data?.templates.find((w) => w.id === expandedItem)?.name || ""}
                      description={getTemplatesResponse?.data?.templates.find((w) => w.id === expandedItem)?.description || ""}
                      templateShareCode={getTemplatesResponse?.data?.templates.find((w) => w.id === expandedItem)?.id || ""}
                      saveResultMessage={editWorldMessage}
                      onClose={closeOverlay}
                      onSaveChanges={(name, desc) => saveTemplateChanges(expandedItem!, name, desc)}
                      onEnterTemplate={() => handleEnterTemplate(expandedItem!)}
                      onDeleteTemplate={() => handleDeleteTemplate(expandedItem!)}
                    />
                  )}
              />
            }
          </>
        )}
      </main>

      {isOverlayOpen && <Overlay onClose={closeOverlay}>{overlayContent}</Overlay>}
    </div>
  );
}

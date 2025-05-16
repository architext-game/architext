import { getWorldTemplates, GetWorldTemplatesResponse, requestWorldCreationFromTemplate } from "@/architextSDK";
import { useStore } from "@/state";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import { useEffect, useState } from "react";
import { WorldsListItem } from "./worlds-list-item";

interface WorldsListProps {
  router: AppRouterInstance,
  expandedItem?: string | null,
  onToggleExpanded: (key: string) => void,
}

export function TemplatesList({ router, expandedItem, onToggleExpanded }: WorldsListProps) {
  const socket = useStore((state) => state.socket)
  
  const [getTemplatesResponse, setGetTemplatesResponse] = useState<GetWorldTemplatesResponse>()

  async function updateTemplates(){
    setGetTemplatesResponse(await getWorldTemplates(socket, {}))
  }

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

  useEffect(() => {
    updateTemplates();
  }, [])
  
  return (
    <div className="flex flex-col">
      <div className="text-lg sm:text-xl py-2">Create a New World</div>
      {
        getTemplatesResponse?.data?.templates.map(template => (
          <WorldsListItem 
            author={template.author_name || "Architext"}
            description={template.description}
            isPublic={false}
            onEnter={handleEnterTemplate}
            onToggleOpen={onToggleExpanded}
            expanded={expandedItem === template.id}
            name={template.name}
            key={template.id}
            worldId={template.id}
          />
        ))
      }
    </div>
  );
}
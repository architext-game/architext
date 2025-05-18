import { getWorldTemplates, GetWorldTemplatesResponse, requestWorldCreationFromTemplate } from "@/architextSDK";
import { useStore } from "@/state";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import { useEffect, useState } from "react";
import { WorldsListItem } from "./worlds-list-item";

interface WorldsListProps {
  router: AppRouterInstance,
  expandedItem?: string | null,
  getTemplatesResponse: GetWorldTemplatesResponse,
  onToggleExpanded: (key: string) => void,
  onEnterTemplate: (templateId: string) => void,
}

export function TemplatesList({ 
  router,
  expandedItem,
  getTemplatesResponse,
  onToggleExpanded,
  onEnterTemplate,
}: WorldsListProps) {
  const socket = useStore((state) => state.socket)

  async function handleEnterTemplate(templateId: string){
    onEnterTemplate(templateId)
  }
  
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
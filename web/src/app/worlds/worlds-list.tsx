import { getWorlds, GetWorldsResponse } from "@/architextSDK";
import { useStore } from "@/state";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import { useEffect, useState } from "react";
import { WorldsListItem } from "./worlds-list-item";

interface WorldsListProps {
  getWorldsResponse: GetWorldsResponse,
  router: AppRouterInstance,
  right: React.ReactNode,
  expandedItem?: string | null,
  onToggleExpanded: (key: string) => void,
  onOpenWorldDetail: (key: string) => void,
  onEnterWorld: (worldId: string) => void,
}

export function WorldsList({ 
  getWorldsResponse,
  router,
  right,
  expandedItem,
  onToggleExpanded,
  onOpenWorldDetail,
  onEnterWorld,
}: WorldsListProps) {
  const socket = useStore((state) => state.socket)
  
  async function handleEnterWorld(worldId: string){
    onEnterWorld(worldId)
  }

  return (
    <div className="flex flex-col">
      <div className="flex justify-between">
        <div className="text-lg sm:text-xl py-2">Worlds</div>
        {right}
      </div>
      {
        getWorldsResponse?.data?.worlds.map(world => (
          <WorldsListItem 
            author={world.owner_name || "Architext"}
            connectedPlayers={world.connected_players_count}
            description={world.description}
            isPublic={world.visibility === "public"}
            onEnter={handleEnterWorld}
            onToggleOpen={onToggleExpanded}
            expanded={expandedItem === world.id}
            name={world.name}
            key={world.id}
            worldId={world.id}
            templateAuthorName={world.base_template_author}
            templateName={world.base_template_name}
            showOpenWorldDetail={world.you_authorized}
            onOpenWorldDetail={onOpenWorldDetail}
          />
        ))
      }
    </div>
  );
}
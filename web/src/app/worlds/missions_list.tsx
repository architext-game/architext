import { completeMission, getAvailableMissions, GetAvailableMissionsResponse, getWorldTemplates, GetWorldTemplatesResponse, requestWorldCreationFromTemplate } from "@/architextSDK";
import { useStore } from "@/state";
import { AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import { useEffect, useState } from "react";
import { WorldsListItem } from "./worlds-list-item";
import { Button } from "@/components/button";
import clsx from "clsx";

interface MissionsListProps {
  router: AppRouterInstance,
}

export function MissionsList({ router }: MissionsListProps) {
  const socket = useStore((state) => state.socket)
  
  const [getMissionsResponse, setGetMissionsResponse] = useState<GetAvailableMissionsResponse>()

  async function handleCompleteMission(missionId: string){
    console.log("handleCompleteMission", missionId)
    await completeMission(socket, { mission_id: missionId })
    updateMissions();
  }

  async function updateMissions(){
    const response = await getAvailableMissions(socket, {})
    console.log("getAvailableMissions", response)
    setGetMissionsResponse(response)
  }

  useEffect(() => {
    updateMissions();
  }, [])
  
  const missionsAvailable = getMissionsResponse?.data?.missions && getMissionsResponse?.data?.missions.length > 0

  return (
    missionsAvailable &&
    <div className="flex flex-col">
      <div className="text-xl py-2">What to do next?</div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
        {
          getMissionsResponse?.data?.missions.map(mission => (
            <MissionListItem 
              id={mission.id}
              name={mission.name}
              description={mission.description}
              key={mission.id}
              onMissionCompleted={handleCompleteMission}
            />
          ))
        }
      </div>
    </div>
  );
}

interface MissionListItemProps {
  id: string;
  name: string;
  description: string;
  onMissionCompleted: (missionId: string) => void;
  link?: string;
}

export function MissionListItem({ id, name, description, onMissionCompleted, link }: MissionListItemProps) {
  let defaultLink: string | undefined = undefined;
  // if(id == "tutorial"){
  //   defaultLink = "#outer"
  // }
  link = link || defaultLink;

  return (
    <div className={clsx("flex flex-col border rounded-lg p-4 w-full gap-4", link && "cursor-pointer hover:bg-backgroundHighlight")} onClick={link ? () => window.location.hash = link : undefined}>
      <div className="flex flex-col gap-2 flex-1">
        <div className="text-base sm:text-lg">{name}</div>
        <div className="text-sm">{description}</div>
      </div>
      <Button className="text-xs self-end" onPress={() => onMissionCompleted(id)}>
        Mark as Complete
      </Button>
    </div>
  );
}
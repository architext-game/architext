"use client";

import { Button } from "@/components/button";
import OSWindow from "./OSWindow";
import clsx from "clsx";

interface TopHeroProps {
  className?: string
}

export const TopHero: React.FC<TopHeroProps> = ({ className }) => {
  return (
    <div className={clsx(className, "flex gap-8")}>
      <div className="flex-1 flex flex-col gap-8">
        <div className="flex flex-col gap-8">
          <div className="text-6xl">Unleash the power of your imagination</div>
          <div className="text-base">Explore a multiplayer virtual reality text realm where you can build anything</div>
        </div>
        <div className="flex items-start">
          <Button>Play Now</Button>
        </div>
      </div>
      <div className="flex-1">
        <OSWindow>
          <img 
            src="/images/build_gameplay.gif" 
            alt="Gameplay Preview" 
            className="w-full h-auto" 
          />
        </OSWindow>
      </div>
    </div>
  )
};

import { useState } from "react";
import { Button } from "@/components/button";
import { motion, AnimatePresence } from "framer-motion";
import clsx from "clsx";

interface WorldsListItemProps {
  name: string;
  description: string;
  isPublic: boolean;
  author: string;
  connectedPlayers?: number;
  templateName?: string | null;
  templateAuthorName?: string | null;
  worldId: string;
  expanded?: boolean;
  showOpenWorldDetail?: boolean;
  onEnter: (worldId: string) => void;
  onToggleOpen: (key: string) => void;
  onOpenWorldDetail?: (key: string) => void;
}

export function WorldsListItem({ 
  name,
  description,
  isPublic,
  author,
  connectedPlayers,
  templateName,
  templateAuthorName,
  expanded,
  onEnter,
  onToggleOpen,
  worldId,
  onOpenWorldDetail,
  showOpenWorldDetail,
}: WorldsListItemProps) {
  const [copied, setCopied] = useState(false);

  function toggleOpen(){
    onToggleOpen(worldId);
  }

  function enterWorld(){
    onEnter(worldId);
  }

  function openWorldDetail(){
    if(onOpenWorldDetail){
      onOpenWorldDetail(worldId);
    }
  }

  async function codeToClipboard(){
    try {
      await navigator.clipboard.writeText(worldId);
      setCopied(true);
      setTimeout(() => setCopied(false), 1000); // Reset after 1s
    } catch (error) {
      console.error("Failed to copy:", error);
    }
  }

  return (
    <div id={worldId} onClick={toggleOpen} className={clsx("-mx-3 sm:mx-0 text-xs md:text-lg flex flex-col cursor-pointer px-2 sm:px-3 overflow-hidden rounded-md transition hover:bg-backgroundHighlight", expanded && "bg-backgroundHighlight")}>
      <div className="flex justify-between py-3 sm:px-3 w-full">
        <div className="flex gap-3 my-auto">
          <div>{isPublic ? "🌍" : "🔓"}</div>
          <div>{name}</div>
        </div>
        <div className="flex sm:gap-3 flex-col-reverse gap-1 sm:flex-row text-right">
          <div>{author}</div>
          { connectedPlayers !== undefined && <div>👤 {connectedPlayers}</div> }
        </div>
      </div>

      <AnimatePresence>
        {expanded && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <div className="flex flex-col gap-5 pb-4 pt-2 px-2 rounded-lg shadow-sm items-start">
              {templateName && (
                <div className="text-sm">Based on {templateName} by {templateAuthorName || "Architext"}</div>
              )}
              <div className="">{description}</div>
              <div className="flex gap-4 flex-wrap">
                <Button onPress={enterWorld}>🚪 Enter Now</Button>
                <Button onPress={codeToClipboard} className="relative">
                  <span className={clsx("transition-opacity", copied ? "opacity-0" : "opacity-100")}>
                  🔑 Copy Code
                  </span>
                  <span className={clsx("absolute inset-0 flex items-center justify-center transition-opacity", copied ? "opacity-100" : "opacity-0")}>
                    Copied!
                  </span>
                </Button>
                {showOpenWorldDetail &&
                  <Button onPress={openWorldDetail}>More...</Button>
                }
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

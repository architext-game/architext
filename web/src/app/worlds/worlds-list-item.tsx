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
  showSettings?: boolean;
  showCreateTemplate?: boolean;
  onEnter: (worldId: string) => void;
  onToggleOpen: (key: string) => void;
  onOpenSettings?: (key: string) => void;
  onOpenCreateTemplate?: (key: string) => void;
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
  onOpenCreateTemplate,
  onOpenSettings,
  showSettings,
  showCreateTemplate,
}: WorldsListItemProps) {
  const [copied, setCopied] = useState(false);

  function toggleOpen(){
    onToggleOpen(worldId);
  }

  function enterWorld(){
    onEnter(worldId);
  }

  function openSettings(){
    if(onOpenSettings){
      onOpenSettings(worldId);
    }
  }

  function openCreateTemplate(){
    if(onOpenCreateTemplate){
      onOpenCreateTemplate(worldId);
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
    <div id={worldId} onClick={toggleOpen} className={clsx("flex flex-col cursor-pointer px-3 overflow-hidden rounded-md transition hover:bg-backgroundHighlight", expanded && "bg-backgroundHighlight")}>
      <div className="flex justify-between p-3 w-full">
        <div className="flex gap-3">
          <div>{isPublic ? "🌍" : "🔒"}</div>
          <div>{name}</div>
        </div>
        <div className="flex gap-3">
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
              <div className="flex gap-4">
                <Button onPress={enterWorld}>Enter Now</Button>
                <Button onPress={codeToClipboard} className="relative">
                  <span className={clsx("transition-opacity", copied ? "opacity-0" : "opacity-100")}>
                    Copy Code
                  </span>
                  <span className={clsx("absolute inset-0 flex items-center justify-center transition-opacity", copied ? "opacity-100" : "opacity-0")}>
                    Copied!
                  </span>
                </Button>
                {showSettings && 
                  <Button onPress={openSettings}>Settings</Button>
                }
                {showCreateTemplate && 
                  <Button onPress={openCreateTemplate}>Create Template</Button>
                }
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

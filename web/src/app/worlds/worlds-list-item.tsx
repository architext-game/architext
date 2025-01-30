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
  onEnter: (worldId: string) => void;
  onToggleOpen: (key: string) => void;
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
}: WorldsListItemProps) {

  function toggleOpen(){
    onToggleOpen(worldId);
  }

  function enterWorld(){
    onEnter(worldId);
  }

  return (
    <div onClick={toggleOpen} className={clsx("flex flex-col cursor-pointer px-3 overflow-hidden rounded-md transition hover:bg-backgroundHighlight", expanded && "bg-backgroundHighlight")}>
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
              <div className="flex">
                <Button onPress={enterWorld}>Enter Now</Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

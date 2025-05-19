import { useState } from "react";
import { Pencil } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";

interface WorldDetailProps {
  name: string;
  description: string;
  worldShareCode: string;
  connectedPlayers: number;
  author: string;
  saveResultMessage: string;
  allowDelete: boolean;
  allowCreateTemplate: boolean;
  allowEdit: boolean;
  allowEnterWorld: boolean;
  showCloseButton: boolean;
  onClose: () => void;
  onSaveChanges: (name: string, description: string) => void;
  onEnterWorld: () => void;
  onCreateTemplate: () => void;
  onDeleteWorld: () => void;
}

export const WorldDetail = ({ 
  name,
  description,
  worldShareCode,
  connectedPlayers,
  author,
  saveResultMessage,
  allowDelete,
  allowCreateTemplate,
  allowEdit,
  allowEnterWorld,
  showCloseButton,
  onClose,
  onSaveChanges,
  onEnterWorld,
  onCreateTemplate,
  onDeleteWorld,
 }: WorldDetailProps) => {
  const [nameValue, setName] = useState(name);
  const [descriptionValue, setDescription] = useState(description);
  const [isEditingName, setIsEditingName] = useState(false);
  const [isEditingDescription, setIsEditingDescription] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteConfirmed, setDeleteConfirmed] = useState(false);

  function saveChanges(newName: string, newDescription: string) {
    onSaveChanges(newName, newDescription);
  }

  function handleConfirmDelete() {
    onDeleteWorld();
    setDeleteConfirmed(true);
  }

  return (
    <div className="flex flex-col gap-6 text-base sm:text-lg">
      {/* Título */}
      <div className="relative">
        {isEditingName ? (
          <input
            autoFocus
            className="bg-transparent border-b border-text focus:outline-none focus:border-primary w-full"
            value={nameValue}
            onChange={(e) => setName(e.target.value)}
            onBlur={() => {
              setIsEditingName(false);
              saveChanges(nameValue, descriptionValue);
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.currentTarget.blur();
              }
            }}
          />
        ) : (
          <h2
            className="text-xl font-bold cursor-pointer group inline-flex items-center gap-1"
            onClick={() => {
              if (!allowEdit) return
              setIsEditingName(true)
            }}
          >
            {nameValue || "No name"}
            {allowEdit && (
              <Pencil
                size={18}
                className="text-primary opacity-0 group-hover:opacity-70 transition-opacity"
              />
            )}
          </h2>
        )}
      </div>

      {/* Descripción */}
      <div className="relative">
        {isEditingDescription ? (
          <textarea
            autoFocus
            className="text-base bg-transparent border-b border-text focus:outline-none focus:border-primary w-full resize-none"
            value={descriptionValue}
            onChange={(e) => setDescription(e.target.value)}
            onBlur={() => {
              setIsEditingDescription(false);
              saveChanges(nameValue, descriptionValue);
            }}
            rows={3}
          />
        ) : (
          <span
            className="text-base cursor-pointer group whitespace-pre-wrap inline-block max-w-full break-words"
            onClick={() => {
              if(!allowEdit) return
              setIsEditingDescription(true)
            }}
          >
            <span>{descriptionValue || "No description"}</span>
            {allowEdit && (
              <Pencil
                size={16}
                className="ml-1 align-text-bottom inline text-primary opacity-0 group-hover:opacity-70 transition-opacity"
              />
            )}
          </span>
        )}
      </div>

      {saveResultMessage && (
        <div className="text-sm text-muted italic">{saveResultMessage}</div>
      )}

      <div className="text-base">
        World Share Code: {worldShareCode}<br/>
        Online players: {connectedPlayers}<br/>
        Author: {author}<br/>
      </div>

      { ( allowDelete || allowCreateTemplate || allowEnterWorld ) &&
        <>
        <div className="flex gap-2">
          Actions
          <div className="flex-1 border h-0 my-auto opacity-40"></div>
        </div>

        <div className="flex flex-col gap-4">
          <div className="flex flex-wrap gap-6 items-center">
            { allowEnterWorld &&
              <button
                onClick={onEnterWorld}
                className="self-start text-sm underline text-primary hover:text-primary/80"
              >
                Enter World
              </button>
            }

            { allowCreateTemplate && 
              <button
              onClick={onCreateTemplate}
              className="self-start text-sm underline text-primary hover:text-primary/80"
              >
                  Create Template
              </button>
            }

            { allowDelete && !showDeleteConfirm && !deleteConfirmed && (
              <button
                onClick={() => setShowDeleteConfirm(true)}
                className="self-start text-sm underline text-primary hover:text-primary/80"
              >
                Delete World
              </button>
            )}
          </div>

          <AnimatePresence>
            {showDeleteConfirm && !deleteConfirmed && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.2 }}
                className="flex flex-col gap-2"
              >
                <div className="text-sm text-red-600">
                  Are you sure you want to delete this world?
                </div>
                <div className="flex gap-4">
                  <button
                    onClick={handleConfirmDelete}
                    className="text-sm text-red-600 underline hover:text-red-500"
                  >
                    Confirm Delete
                  </button>
                  <button
                    onClick={() => setShowDeleteConfirm(false)}
                    className="text-sm text-primary underline hover:text-primary/80"
                  >
                    Cancel
                  </button>
                </div>
              </motion.div>
            )}

            {deleteConfirmed && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.2 }}
                className="text-sm text-green-500"
              >
                World deleted successfully.
              </motion.div>
            )}
          </AnimatePresence>
        </div>
        </>
      }

      { 
        showCloseButton &&
        <button
          onClick={onClose}
          className="self-end text-sm underline text-primary hover:text-primary/80"
        >
          Close
        </button>
      }
      
    </div>
  );
};

import { editWorld, getWorld } from "@/architextSDK";
import { useStore } from "@/state";
import { useEffect, useState } from "react";
import { Pencil } from "lucide-react";
import { Button } from "@/components/button";

interface WorldDetailProps {
  id: string;
  name: string;
  description: string;
  worldShareCode: string;
  connectedPlayers: number;
  author: string;
  saveResultMessage: string;
  onClose: () => void;
  onSaveChanges: (name: string, description: string) => void;
}

export const WorldDetail = ({ 
  id,
  name,
  description,
  worldShareCode,
  connectedPlayers,
  author,
  saveResultMessage,
  onClose,
  onSaveChanges,
 }: WorldDetailProps) => {
  const [nameValue, setName] = useState(name);
  const [descriptionValue, setDescription] = useState(description);
  const [isEditingName, setIsEditingName] = useState(false);
  const [isEditingDescription, setIsEditingDescription] = useState(false);

  function saveChanges(newName: string, newDescription: string) {
    onSaveChanges(newName, newDescription);
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
            onClick={() => setIsEditingName(true)}
          >
            {nameValue || "No name"}
            <Pencil
              size={18}
              className="text-primary opacity-0 group-hover:opacity-70 transition-opacity"
            />
          </h2>
        )}
      </div>

      {/* Descripción en línea */}
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
            onClick={() => setIsEditingDescription(true)}
          >
            <span>{descriptionValue || "No description"}</span>
            <Pencil
              size={16}
              className="ml-1 align-text-bottom inline text-primary opacity-0 group-hover:opacity-70 transition-opacity"
            />
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

      {/* <div className="flex gap-2">
        Actions
        <div className="flex-1 border h-0 my-auto opacity-40"></div>
      </div>

      <div className="flex flex-wrap gap-6 items-center">
        <button
          className="self-start text-sm underline text-primary hover:text-primary/80"
        >
          Enter World
        </button>

        <button
          className="self-start text-sm underline text-primary hover:text-primary/80"
        >
          Create Template
        </button>

        <button
          className="self-start text-sm underline text-primary hover:text-primary/80"
        >
          Delete World
        </button>
      </div> */}

      <button
        onClick={onClose}
        className="self-end text-sm underline text-primary hover:text-primary/80"
      >
        Close
      </button>
    </div>
  );
};

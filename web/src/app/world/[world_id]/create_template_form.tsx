import { createTemplate, editWorld, getWorld } from "@/architextSDK";
import { Button } from "@/components/button";
import { Input } from "@/components/input";
import { useStore } from "@/state";
import { useEffect, useState } from "react";

interface CreateTemplateFormProps {
  id: string;
  worldName: string;
  worldDescription: string;
  onClose: () => void;
  onCreateTemplate: (name: string, description: string, templateId: string) => void;
}

export const CreateTemplateForm = ({ 
  id,
  worldName,
  worldDescription,
  onCreateTemplate,
  onClose
}: CreateTemplateFormProps) => {
  const [nameInput, setNameInput] = useState(worldName);
  const [descriptionInput, setDescriptionInput] = useState(worldDescription);
  const [message, setMessage] = useState('');
  const socket = useStore((state) => state.socket)

  function handleSubmit(){
    setMessage('')
    createTemplate(socket, {
      base_world_id: id,
      name: nameInput,
      description: descriptionInput
    }).then(response => {
      if(response.success){
        setMessage("Success!")
        setDescriptionInput("")
        setNameInput("")
        onCreateTemplate(nameInput, descriptionInput, id)
      } else {
        setMessage("There was an error.")
      }
    })
  }

  function handleClose(){
    setNameInput('')
    onClose()
  }  

  return (
    <div className="flex flex-col items-stretch gap-4 text-base">
      A template allows you to create new copies of the original world. You can also share templates with other players.
      <Input value={nameInput} onChange={(e) => setNameInput(e.target.value)} placeholder="Name" label="Template Name" />
      <Input multiline value={descriptionInput} onChange={(e) => setDescriptionInput(e.target.value)} placeholder="Description" label="Template Description" />
      {
        message &&
        <div>{message}</div>
      }
      <div className="flex gap-4 pt-4 justify-between">
        <button
          onClick={handleSubmit}
          className="self-start text-sm underline text-primary hover:text-primary/80"
        >
          Create Template
        </button>
        <button
          onClick={handleClose}
          className="self-end text-sm underline text-primary hover:text-primary/80"
        >
          Close
        </button>
      </div>
    </div>
  );
};

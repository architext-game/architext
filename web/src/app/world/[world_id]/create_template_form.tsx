import { createTemplate, editWorld, getWorld } from "@/architextSDK";
import { Button } from "@/components/button";
import { Input } from "@/components/input";
import { useStore } from "@/state";
import { useEffect, useState } from "react";

interface CreateTemplateFormProps {
  id: string;
  onClose: () => void;
}

export const CreateTemplateForm = ({ id, onClose }: CreateTemplateFormProps) => {
  const [nameInput, setNameInput] = useState('');
  const [descriptionInput, setDescriptionInput] = useState('');
  const [message, setMessage] = useState('');
  const socket = useStore((state) => state.socket)

  useEffect(() => {
    getWorld(socket, { world_id: id}).then(response => {
      if(response.success && response.data){
        setNameInput(response.data.name)
        setDescriptionInput(response.data.description)
      }
    })
  }, [id]);

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
    <div className="flex flex-col items-stretch gap-4">
      <Input value={nameInput} onChange={(e) => setNameInput(e.target.value)} placeholder="Name" label="Name" />
      <Input value={descriptionInput} onChange={(e) => setDescriptionInput(e.target.value)} placeholder="Description" label="Description" />
      {
        message &&
        <div>{message}</div>
      }
      <div className="flex gap-4 pt-4">
        <Button onClick={handleSubmit}>Create Template</Button>
        <Button onClick={handleClose}>Close</Button>
      </div>
    </div>
  );
};

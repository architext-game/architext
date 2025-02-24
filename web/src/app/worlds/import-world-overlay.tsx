import { Button } from "@/components/button";
import { Overlay } from "@/components/overlay";

interface ImportWorldOverlayProps {
  onClose: () => void,
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void,
  error: string,
  name: string,
  setName: (code: string) => void,
  description: string,
  setDescription: (code: string) => void,
  textRepresentation: string,
  setTextRepresentation: (code: string) => void,
}

export function ImportWorldOverlay({ 
  onClose,
  onSubmit,
  error,
  name,
  setName,
  description,
  setDescription,
  textRepresentation,
  setTextRepresentation,
}: ImportWorldOverlayProps) {
  function close(){
    setName("")
    setDescription("")
    setTextRepresentation("")
    onClose()
  }

  return (
    <Overlay onClose={close} showCloseIcon >
      <form onSubmit={onSubmit} className="flex flex-col gap-4 w-full max-w-sm items-stretch">
        {
          error &&
          <div className="text-sm">{error}</div>
        }
        <label htmlFor="worldcode">Import a world</label>
        <input
          id="name"
          type="text"
          className="border border-gray-300 px-3 py-2 rounded bg-background"
          placeholder="World name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          id="description"
          type="text"
          className="border border-gray-300 px-3 py-2 rounded bg-background"
          placeholder="World description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <textarea
          id="textrepresentation"
          className="border border-gray-300 px-3 py-2 rounded bg-background"
          placeholder="Text representation"
          value={textRepresentation}
          onChange={(e) => setTextRepresentation(e.target.value)}
        />
        <Button
          type="submit"
        >
          Enter
        </Button>
      </form>
    </Overlay>
  );
}

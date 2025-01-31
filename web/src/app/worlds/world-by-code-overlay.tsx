import { Button } from "@/components/button";
import { Overlay } from "@/components/overlay";

interface WorldByCodeOverlayProps {
  onClose: () => void,
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void,
  error: string,
  worldCode: string,
  setWorldCode: (code: string) => void,
}

export function WorldByCodeOverlay({ 
  onClose,
  onSubmit,
  error,
  worldCode,
  setWorldCode,
}: WorldByCodeOverlayProps) {
  return (
    <Overlay onClose={onClose} showCloseIcon >
      <form onSubmit={onSubmit} className="flex flex-col gap-4 w-full max-w-sm items-stretch">
        {
          error &&
          <div className="text-sm">{error}</div>
        }
        <label htmlFor="worldcode">Enter a world by its code</label>
        <input
          id="worldcode"
          type="text"
          className="border border-gray-300 px-3 py-2 rounded bg-background"
          placeholder="0000-0000-0000-0000"
          value={worldCode}
          onChange={(e) => setWorldCode(e.target.value)}
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

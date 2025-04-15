'use client';

import { getMe, updateUserSettings } from "@/architextSDK";
import { Button } from "@/components/button";
import { Header } from "@/components/header";
import { Input } from "@/components/input";
import { useStore } from "@/state";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";


export default function Home() {
  const [error, setError] = useState<string | null>(null);
  const [username, setUsername] = useState<string>("");
  const socket = useStore((state) => state.socket);
  const router = useRouter();
  const authenticated = useStore((state) => state.authenticated);
  
  useEffect(() => {
    if (authenticated) {
      getMe(socket, {}).then(response => {
        if(response.data?.name){
          setUsername(response.data?.name);
        };
      });
    }
  }, [authenticated]);

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError(null)
    const response = await updateUserSettings(socket, {new_name: username})
    if(response.success) {
      router.push('/worlds')
    } else {
      setError(response.error)
    }
    console.log(response);
  }
  
  return (
    <div className="text-text text-lg font-mono flex flex-col items-center min-h-screen pb-20">
      <Header className='mx-auto max-w-screen-md'/>
      <main className="flex flex-col gap-8 row-start-2 items-stretch max-w-screen-md w-full">
        <div className="mx-auto">
          <form onSubmit={onSubmit} className="flex flex-col gap-4 w-full max-w-sm items-stretch">
            <label htmlFor="worldcode">Choose your name</label>
            <Input
              id="username"
              type="text"
              className="border border-gray-300 px-3 py-2 rounded bg-background"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            {
              error &&
              <div className="text-sm">{error}</div>
            }
            <Button
              type="submit"
            >
              Enter
            </Button>
          </form>
        </div>
      </main>
    </div>
  );
}

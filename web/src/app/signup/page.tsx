"use client"

import { useState } from "react";
import { signup } from "@/architextSDK";
import { useStore } from "@/state";
import Link from "next/link";
import { useRouter } from 'next/navigation'
import { Header } from "@/components/header";
import { Card } from "@/components/card";
import { Input } from "@/components/input";
import { Button } from "@/components/button";

export default function Home() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const socket = useStore((state) => state.socket)
  const router = useRouter()

  // Maneja el evento submit del formulario.
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Aquí podrías llamar a tu API o servicio de autenticación.
    console.log("Name:", name);
    console.log("Email:", email);
    console.log("Password:", password);
    const response = await signup(socket, { name: name, email, password: password })
    console.log(response)
    if(response.success) {
      router.push('login')
    } else {
      setError("Error: " + response.error)
    }
  };

  return (
    <div className="text-text text-lg font-mono flex flex-col items-center min-h-screen pb-20">
      <Header />
      <main className="flex flex-col gap-8 row-start-2 items-stretch max-w-screen-md w-full">
        <Card className="px-8 py-12 flex flex-col items-center">
          <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-sm">
            {
              error &&
              <div>{error}</div>
            }
            <label htmlFor="name">
              Username
            </label>
            <Input
              id="name"
              placeholder="Wade Watts"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <label htmlFor="email">
              Email
            </label>
            <Input
              id="email"
              type="email"
              placeholder="wade@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <label htmlFor="password">
              Password
            </label>
            <Input
              id="password"
              type="password"
              placeholder="********"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button
              type="submit"
            >
              Sign Up
            </Button>
            <div className="mx-auto">or</div>
            <Link href='/login'><Button className='w-full'>Login</Button></Link>
          </form>
        </Card>
      </main>
    </div>
  );
}

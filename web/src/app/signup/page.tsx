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
    <div className="text-text font-mono grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <Header />
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <Card className="px-16 py-8">
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
            or
            <Link href='/login'><Button className='w-full'>Login</Button></Link>
          </form>
        </Card>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        Welcome to Architext
      </footer>
    </div>
  );
}

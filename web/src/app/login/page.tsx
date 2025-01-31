"use client"; // Si estás usando app router en Next.js 13+

import { useState } from "react";
import { useStore } from "@/state";
import Link from "next/link";
import { useRouter } from 'next/navigation';
import { Button } from "@/components/button";
import { Header } from "@/components/header";
import { Card } from "@/components/card";
import { Input } from "@/components/input";

export default function Home() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const router = useRouter()
  const login = useStore((state) => state.login)

  // Maneja el evento submit del formulario.
  // TODO: El autocompletado de contraseñas no funciona,
  // no parece llamar al onChange de los inputs.
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Aquí podrías llamar a tu API o servicio de autenticación.
    console.log("Email:", email);
    console.log("Password:", password);
    const response = await login(email, password)
    if(response?.success) {
      router.push('/worlds')
    } else {
      setError("Error: " + response?.error)
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
            <label htmlFor="email">
              Email
            </label>
            <Input
              id="email"
              type="email"
              placeholder="email@example.com"
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

            <Button type="submit">
              Login
            </Button>
            <div className="mx-auto">or</div>
            <Link href='/signup'><Button className='w-full'>Create an account</Button></Link>
          </form>
        </Card>
        
      </main>
    </div>
  );
}

"use client"

import Link from 'next/link'
import { useStore } from '@/state';

export default function Home() {
  const jwt = useStore((s) => s.jwt)
  const socket = useStore((s) => s.socket)

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        ESTAS DENTRO DEL JUEGO
        {jwt}
        <div  className='text-blue-500 hover:underline'>Cierra sesión</div>
      </main>

      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center">
        Welcome to Architext
      </footer>
    </div>
  );
}

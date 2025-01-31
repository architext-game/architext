"use client"

import { useStore } from "@/state";
import Link from "next/link";

export function Header() {
  const me = useStore((state) => state.me)

  return (
    <div className="flex flex-row font-mono gap-10 justify-start max-w-screen-md w-full pb-11 pt-9">
      <h1 className="font-mono text-5xl hover:underline">
        <Link href="/">Architext</Link>
      </h1>
      <Link href='/worlds' className="text-lg hover:underline">
        Play
      </Link>
    </div>
  );
}
import Link from "next/link";

export function Header() {
  return (
    <div className="flex flex-row font-mono gap-10 justify-start max-w-screen-md w-full py-6 pt-9">
      <h1 className="font-mono text-5xl hover:underline">
        <Link href="/">Architext</Link>
      </h1>
      <Link href='/worlds' className="text-lg hover:underline">
        Play
      </Link>
    </div>
  );
}
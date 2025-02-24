import { Header } from "@/components/header";
import { SignIn } from "@clerk/nextjs";

export default function Home() {
  return (
    <div className="text-text text-lg font-mono flex flex-col items-center min-h-screen pb-20">
      <Header />
      <main className="flex flex-col gap-8 row-start-2 items-stretch max-w-screen-md w-full">
        <div className="mx-auto">
          <SignIn routing="hash" />
        </div>      
      </main>
    </div>
  );
}

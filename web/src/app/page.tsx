import { Header } from '@/components/header';
import { Card } from '@/components/card';

export default function Home() {
  return (
    <div className="flex flex-col items-center text-text font-mono  text-lg pb-40">
      <Header/>
      <main className="flex flex-col gap-8 row-start-2 w-full max-w-screen-md items-stretch py-5">
        <Card>
          Hello. This will be Architext's landing page. But it's not ready yet. Come back later :-)
        </Card>
      </main>
    </div>
  );
}

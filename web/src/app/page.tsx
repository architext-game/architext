import { Header } from '@/components/header';
import { TopHero } from './landing/TopHero';
import { FeatureRow, FeatureRowItem } from './landing/FeatureRow';
import GameplayTabs from './landing/GameplayTabs';
import { Benefit } from './landing/Benefit';
import { Faq } from './landing/faq';
import { CallToAction } from './landing/CallToAction';
import { Footer } from '@/components/footer';

export default function Home() {
  return (
    <div className="flex flex-col items-center text-text font-mono  text-lg px-4 sm:px-6 overflow-hidden">
      <Header className='max-w-screen-lg mb-10 sm:mb-20'/>
      <main className="flex flex-col gap-8 row-start-2 w-full max-w-screen-lg items-stretch">
        <TopHero className='mb-10 sm:mb-28'/>
        <div className="text-lg sm:text-2xl text-center px-2 sm:px-16 mb-6 sm:mb-24">
          Architext is a multiplayer virtual reality text game that allows you to explore and create worlds entirely made of words
        </div>
        <FeatureRow className=''>
          <FeatureRowItem 
            icon="🏝️"
            title="Visit worlds made by other players"
            description="Travel through detailed environments crafted by other players, each one offering a unique story, setting, and perspective to discover."
          />
          <FeatureRowItem 
            icon="🤝"
            title="Explore in real time with your friends"
            description="Share live adventures with your friends and uncover secrets together as you explore dynamic and ever-evolving narrative landscapes."
          />
          <FeatureRowItem 
            icon="🛠️"
            title="Create your own worlds in an intuitive way"
            description="Build immersive text-based worlds with simple commands designed to bring your imagination to life—no experience required."
          />
        </FeatureRow>
        <Benefit 
          className="hidden sm:flex pt-32"
          title="The Most Immersive VR Experience"
          subtitle="Discover the Boundless World of Your Imagination.  No headset needed – dive deep into the realms crafted by your own mind."
          visual={<div className="text-9xl h-fit text-center">🎮</div>}
        />
        <Benefit 
          className="hidden sm:flex pt-32"
          title="Slow Down Your Mind"
          subtitle="Escape the overload of social media, ads and notifications designed to stimulate the most primal side of your brain. Here you can give your mind a time to detox."
          visual={<div className="text-9xl h-fit text-center">🧠</div>}
          reverse
        />
        <GameplayTabs className='mt-8 sm:mt-10 sm:px-20'/>
        <Benefit 
          className="hidden sm:flex pt-32"
          title="Create Your Own Unique Space"
          subtitle="Where You and Your Friends Truly Belong. Design an environment that reflects who you are and share it with those who matter."
          visual={<div className="text-9xl h-fit text-center">🛋️</div>}
        />
        <Benefit 
          className="hidden sm:visible pt-32"
          title="Rediscover Your Creative Power"
          subtitle="Unleash the Infinite Potential of Your Imagination. Reconnect with the childlike wonder of creation and let your mind explore without limits."
          visual={<div className="text-9xl h-fit text-center">🎨</div>}
          reverse
        />

        <Faq className='mt-16 sm:mt-24' />

        <CallToAction className='mt-10 mb-20' />
      </main>
      <Footer />
    </div>
  );
}

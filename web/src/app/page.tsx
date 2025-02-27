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
    <div className="flex flex-col items-center text-text font-mono  text-lg">
      <Header className='max-w-screen-lg mb-16'/>
      <main className="flex flex-col gap-8 row-start-2 w-full max-w-screen-lg items-stretch">
        <TopHero className='mb-28'/>
        <div className="text-2xl text-center px-16 mb-24">
          Architext is a multiplayer virtual reality text game that allows you to explore and create worlds entirely made of words
        </div>
        <FeatureRow className=''>
          <FeatureRowItem 
            icon="🏝️"
            title="Visit worlds made by other players"
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
          />
          <FeatureRowItem 
            icon="🤝"
            title="Explore in real time with your friends"
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
          />
          <FeatureRowItem 
            icon="🛠️"
            title="Create your own worlds in an intuitive way"
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
          />
        </FeatureRow>
        <Benefit 
          className="pt-32"
          title="The Most Immersive VR Experience"
          subtitle="Discover the Boundless World of Your Imagination.  No headset needed – dive deep into the realms crafted by your own mind."
          visual={<div className="text-9xl h-fit text-center">🎮</div>}
        />
        <Benefit 
          className="pt-32"
          title="Slow Down Your Mind"
          subtitle="Escape the overload of social media, ads and notifications designed to stimulate the most primal side of your brain. Here you can give your mind a time to detox."
          visual={<div className="text-9xl h-fit text-center">🧠</div>}
          reverse
        />
        <GameplayTabs className='px-20'/>
        <Benefit 
          className="pt-32"
          title="Create Your Own Unique Space"
          subtitle="Where You and Your Friends Truly Belong. Design an environment that reflects who you are and share it with those who matter."
          visual={<div className="text-9xl h-fit text-center">🛋️</div>}
        />
        <Benefit 
          className="pt-32"
          title="Rediscover Your Creative Power"
          subtitle="Unleash the Infinite Potential of Your Imagination. Reconnect with the childlike wonder of creation and let your mind explore without limits."
          visual={<div className="text-9xl h-fit text-center">🎨</div>}
          reverse
        />

        <Faq className='pt-28' />

        <CallToAction />
      </main>
      <Footer />
    </div>
  );
}

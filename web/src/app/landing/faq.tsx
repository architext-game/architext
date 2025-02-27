"use client"

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from '@iconify/react';
import clsx from 'clsx';

interface FaqProps {
  className: string;
}

export const Faq: React.FC<FaqProps> = ({ className }) => {
  return (
    <div className={clsx("p-4 max-w-4xl w-full mx-auto", className)}>
      <h2 id="faq" className="text-3xl font-bold mb-6">Frecuently Asked Questions</h2>
      <FaqItem 
        question="How much does this cost?" 
        answer={(
          <>
            Absolutely free! <br />
            This is a passion project made out of love for the art. <br />
            No hidden fees, no premium versions—just pure creativity for everyone.
          </>
        )}
      />
      <FaqItem 
        question="Does anybody actually play this?" 
        answer={(
          <>
            You could be the first! <br />
            I just released this game after countless hours of work. You could be the pioneer, the legend, the one that 9,000,000 players will look up to once they discover this hidden gem. <br />
            Or… you could skip it, and no one would ever know about my cool game. Your choice.
          </>
        )}
      />
      <FaqItem 
        question="What features are coming soon?" 
        answer={(
          <>
            A lot! <br />
            We’re constantly working on exciting updates to enhance your experience. Stay tuned for new features and improvements!
          </>
        )}
      />
      <FaqItem 
        question="Can I export the worlds I create?" 
        answer={(
          <>
            Not yet, but very soon! <br />
            We’re working on it! Soon you’ll be able to export your creations and use them however you like. Hang tight!
          </>
        )}
      />
      <FaqItem 
        question="Can I submit feedback?" 
        answer={(
          <>
            Absolutely! Please do! <br />
            Your feedback is incredibly valuable. We’re eager to hear your thoughts and ideas to make the game even better. Don’t hesitate to reach out!
          </>
        )}
      />
    </div>
  )
};


interface FaqItemProps {
  question: React.JSX.Element | string;
  answer: React.JSX.Element | string;
}

const FaqItem: React.FC<FaqItemProps> = ({ question, answer }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleOpen = () => setIsOpen(!isOpen);

  return (
    <div className="border-b border-opacity-50 py-4">
      <button 
        onClick={toggleOpen} 
        className="w-full flex justify-between items-center text-left focus:outline-none"
      >
        <span className="text-lg font-semibold">{question}</span>
        <Icon 
          icon={isOpen ? "mdi:chevron-up" : "mdi:chevron-down"} 
          className="text-xl"
        />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <p className="mt-2 opacity-80">{answer}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};



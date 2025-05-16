"use client";

import React, { useState, useEffect, useRef } from 'react';
import classNames from 'classnames';
import clsx from 'clsx';
import OSWindow from './OSWindow';

// Example Components for the Tabs
const BuildComponent = () => (
  <OSWindow>
    <img 
      src="/images/build_gameplay.gif" 
      alt="Build Gameplay Preview" 
      className="w-full h-auto" 
    />
  </OSWindow>
);

const ExploreComponent = () => (
  <OSWindow>
    <img 
      src="/images/exploration_gameplay.gif" 
      alt="Exploration Gameplay Preview" 
      className="w-full h-auto" 
    />
  </OSWindow>
);

const CoolComponent = () => (
  <OSWindow>
    <img 
      src="/images/social_gameplay.gif" 
      alt="Social Gameplay Preview" 
      className="w-full h-auto" 
    />
  </OSWindow>
);

const tabs = [
  { id: 0, label: "Build", component: <BuildComponent /> },
  { id: 1, label: "Explore", component: <ExploreComponent /> },
  { id: 2, label: "With Friends", component: <CoolComponent /> }
];

const INTERVAL_TIME = 6000;
const TIME_WITH_FULL_PROGRESS = 1500;

function getBarProgress(progress: number) {
  
  const elapsedTime = INTERVAL_TIME*progress/100
  const ajustedTime = elapsedTime + TIME_WITH_FULL_PROGRESS*progress/100
  const adjustedProgress = ajustedTime / INTERVAL_TIME * 100
  console.log(progress, adjustedProgress)
  return Math.min(adjustedProgress, 100);
}

interface GameplayTabsPros {
  className?: string
}

const GameplayTabs: React.FC<GameplayTabsPros> = ({ className }) => {
  // Originally the tabs were set to cycle automatically
  // to recover that behavior, set the manualOverride to false
  // and progress to 0
  const [activeTab, setActiveTab] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [manualOverride, setManualOverride] = useState(true);
  const [progress, setProgress] = useState(100);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const progressRef = useRef<NodeJS.Timeout | null>(null);

  // Auto-switch tabs unless manually overridden
  useEffect(() => {
    if (manualOverride) return;

    if (!isPaused) {
      intervalRef.current = setInterval(() => {
        setActiveTab(prev => (prev + 1) % tabs.length);
        setProgress(0);
      }, INTERVAL_TIME);

      progressRef.current = setInterval(() => {
        setProgress(prev => (prev + 100 / (INTERVAL_TIME / 100)) % 100);
      }, 100);
    }

    return () => {
      clearInterval(intervalRef.current as NodeJS.Timeout);
      clearInterval(progressRef.current as NodeJS.Timeout);
    };
  }, [isPaused, manualOverride]);

  // Handle manual tab change
  const handleTabClick = (id: number) => {
    setActiveTab(id);
    setManualOverride(true);
    setProgress(100); // Complete the underline when clicked
  };

  return (
    <div 
      className={clsx("w-full mx-auto p-4 rounded-lg relative text-white", className)}
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      {/* Tab Bar */}
      <div className="flex justify-around border-b-2 text-white">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => handleTabClick(tab.id)}
            className={classNames(
              "py-2 px-4 transition-all duration-300 focus:outline-none relative text-sm sm:text-base",
              {
                "text-white font-semibold": activeTab === tab.id,
                "text-white opacity-50": activeTab !== tab.id
              }
            )}
          >
            {tab.label}
            <span
              className={classNames(
                "absolute left-0 bottom-0 h-1 bg-white opacity-20 duration-300 transition-none",
                {
                  "w-full": activeTab === tab.id,
                  "w-0": activeTab !== tab.id
                }
              )}
            ></span>
            {/* Underline Animation */}
            <span
              className={classNames(
                "absolute left-0 bottom-0 h-1 bg-white transition-all duration-300",
                {
                  "w-full transition-none": activeTab === tab.id && progress === 100,
                  "w-0 transition-none": activeTab !== tab.id
                }
              )}
              style={{
                width: activeTab === tab.id ? `${getBarProgress(progress)}%` : '0%'
              }}
            ></span>
          </button>
        ))}
      </div>

      <div className="text-center mt-12 sm:mt-20 max-w-lg mx-auto px-4">
        <div
          key={activeTab}
          className="text-6xl transition-transform duration-500 ease-in-out transform scale-125"
        >
          {tabs[activeTab].component}
        </div>
      </div>
    </div>
  );
};

export default GameplayTabs;

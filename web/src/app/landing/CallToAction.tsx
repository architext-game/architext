"use client";

import { Button } from "@/components/button";

interface CallToActionProps {
  className: string;
}

export const CallToAction = () => {
  return (
    <section className="py-20 px-4 text-center">
      <h4 className="text-base uppercase mb-4">Let's Get Started</h4>
      <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-12">
        Start your adventure with the five minute tutorial, <br className="hidden md:inline" />
        and become an arquitext
      </h2>
      <Button className="px-24 py-4">
        Sign Up
      </Button>
    </section>
  );
};

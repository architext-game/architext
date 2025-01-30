import React from "react";
import clsx from "clsx";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={clsx("border rounded-xl px-5 py-3", className)}>
      {children}
    </div>
  );
}
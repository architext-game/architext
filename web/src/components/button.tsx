import React from "react";
import clsx from "clsx";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  onPress?: React.MouseEventHandler<HTMLButtonElement>;
}

export function Button({ children, onPress, className, type="button", ...props }: ButtonProps) {
  return (
    <button
      type={type}
      onClick={(e) => {
        e.stopPropagation();
        if (onPress) {
          onPress(e);
        }
      }}
      className={clsx(
        "rounded-xl border px-4 py-2 text-center transition bg-background hover:bg-backgroundHighlight active:bg-gray-300",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}

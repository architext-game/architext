import React from "react";
import clsx from "clsx";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> { }

export function Input({
  className,
  type = "text",
  placeholder,
  value,
  onChange,
  ...props
}: InputProps) {
  return (
    <input
      type={type}
      className={clsx(
        "border border-gray-300 px-3 py-2 rounded bg-background hover:bg-backgroundHighlight",
        className
      )}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      {...props}
    />
  );
}

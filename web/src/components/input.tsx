import React from "react";
import clsx from "clsx";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function Input({
  className,
  type = "text",
  placeholder,
  value,
  onChange,
  id,
  label,
  ...props
}: InputProps) {
  return (
    <div className="flex flex-col gap-2">
      { label && 
        <label htmlFor={id}>
          {label}
        </label>
      }
      <input
        id={id}
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
    </div>
  );
}

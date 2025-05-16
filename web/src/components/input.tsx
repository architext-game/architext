import React from "react";
import clsx from "clsx";

type CommonProps = {
  label?: string;
  className?: string;
  id?: string;
  multiline?: boolean;
};

type InputProps =
  | (CommonProps &
      React.InputHTMLAttributes<HTMLInputElement> & {
        multiline?: false;
      })
  | (CommonProps &
      React.TextareaHTMLAttributes<HTMLTextAreaElement> & {
        multiline: true;
        rows?: number;
      });

export function Input(props: InputProps) {
  const {
    label,
    className,
    id,
    multiline,
    ...rest
  } = props;

  return (
    <div className="flex flex-col gap-2">
      {label && (
        <label htmlFor={id}>
          {label}
        </label>
      )}

      {multiline ? (
        <textarea
          id={id}
          className={clsx(
            "border border-gray-300 px-3 py-2 rounded bg-background hover:bg-backgroundHighlight resize-y",
            className
          )}
          {...(rest as React.TextareaHTMLAttributes<HTMLTextAreaElement>)}
        />
      ) : (
        <input
          id={id}
          className={clsx(
            "border border-gray-300 px-3 py-2 rounded bg-background hover:bg-backgroundHighlight",
            className
          )}
          {...(rest as React.InputHTMLAttributes<HTMLInputElement>)}
        />
      )}
    </div>
  );
}

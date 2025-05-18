import { Icon } from "@iconify/react";
import React from "react";

interface OverlayProps {
  children: React.ReactNode;
  onClose: () => void;
  showCloseIcon?: boolean;
}

export function Overlay({ children, onClose, showCloseIcon = false }: OverlayProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      {/* Clickable background to close */}
      <div className="absolute inset-0" onClick={onClose}></div>

      {/* Content inside the overlay with scrollable area */}
      <div
        className="relative bg-background p-6 rounded-lg shadow-lg max-w-md w-full z-10 max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()} // prevent click inside from closing overlay
      >
        {showCloseIcon && (
          <Icon
            onClick={onClose}
            icon="material-symbols-light:close-rounded"
            height={32}
            className="-ml-2 -mt-2 mb-2 cursor-pointer"
          />
        )}
        {children}
      </div>
    </div>
  );
}

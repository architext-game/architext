import React from 'react';

interface OSWindowProps {
  title?: string;
  children: React.ReactNode;
}

const OSWindow: React.FC<OSWindowProps> = ({ title = "", children }) => {
  return (
    <div className="max-w-3xl mx-auto shadow-lg rounded-md border border-gray-100 overflow-hidden">
      {/* Header with window controls */}
      <div className="p-2 flex items-center justify-between border-b border-gray-200">
        <div className="flex space-x-2 ml-2">
          <span className="w-3 h-3 bg-red-500 opacity-25 rounded-full cursor-pointer"></span>
          <span className="w-3 h-3 bg-yellow-400 opacity-25 rounded-full cursor-pointer"></span>
          <span className="w-3 h-3 bg-green-500 opacity-25 rounded-full cursor-pointer"></span>
        </div>
        <div className="text-sm text-gray-600">{title}</div>
        <div className="w-10"></div>
      </div>

      {/* Content */}
      <div className="">
        {children}
      </div>
    </div>
  );
};

export default OSWindow;

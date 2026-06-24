import React from 'react';

export default function ModelBadge({ modelUsed, timeMs }) {
  if (!modelUsed) return null;

  let bgColor = "bg-gray-500/20";
  let textColor = "text-gray-400";
  let borderColor = "border-gray-500/30";

  if (modelUsed.includes("Gemini")) {
    bgColor = "bg-blue-500/20";
    textColor = "text-blue-400";
    borderColor = "border-blue-500/30";
  } else if (modelUsed.includes("Groq")) {
    bgColor = "bg-orange-500/20";
    textColor = "text-orange-400";
    borderColor = "border-orange-500/30";
  } else if (modelUsed.includes("OpenRouter")) {
    bgColor = "bg-purple-500/20";
    textColor = "text-purple-400";
    borderColor = "border-purple-500/30";
  }

  return (
    <div className="flex items-center space-x-3 text-sm">
      <span className="text-gray-500">Analyzed using:</span>
      <span className={`px-3 py-1 rounded-full font-medium text-xs border ${bgColor} ${textColor} ${borderColor}`}>
        {modelUsed}
      </span>
      {timeMs && (
        <span className="text-gray-600 text-xs flex items-center">
          <svg className="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          {timeMs}ms
        </span>
      )}
    </div>
  );
}



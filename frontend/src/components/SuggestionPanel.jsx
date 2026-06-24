import React, { useState } from 'react';

export default function SuggestionPanel({ suggestions }) {
  const [openIndex, setOpenIndex] = useState(0);

  if (!suggestions || suggestions.length === 0) {
    return null;
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="bg-gray-800/50 rounded-xl border border-gray-700 overflow-hidden">
      <div className="p-5 border-b border-gray-700 bg-gray-800/80">
        <h3 className="text-lg font-semibold text-white">AI Rewrite Suggestions</h3>
        <p className="text-sm text-gray-400 mt-1">Enhance your bullet points to better match the job description.</p>
      </div>
      <div className="divide-y divide-gray-700">
        {suggestions.map((suggestion, index) => {
          const isOpen = openIndex === index;
          return (
            <div key={index} className="group">
              <button
                className="w-full px-5 py-4 flex items-center justify-between text-left focus:outline-none hover:bg-gray-700/30 transition-colors"
                onClick={() => setOpenIndex(isOpen ? -1 : index)}
              >
                <div className="flex items-center space-x-3">
                  <span className="bg-accent/20 text-accent text-xs font-bold px-2.5 py-1 rounded">
                    {suggestion.section}
                  </span>
                  <span className="text-gray-300 font-medium truncate max-w-md">
                    {suggestion.original.substring(0, 60)}...
                  </span>
                </div>
                <svg className={`w-5 h-5 text-gray-500 transform transition-transform ${isOpen ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {isOpen && (
                <div className="px-5 pb-5 pt-2 animate-fadeIn">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
                      <span className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 block">Before</span>
                      <p className="text-sm text-gray-400 whitespace-pre-wrap">{suggestion.original}</p>
                    </div>
                    <div className="bg-accent/5 rounded-lg p-4 border border-accent/20 relative">
                      <span className="text-xs font-bold text-accent uppercase tracking-wider mb-2 block">After (AI Improved)</span>
                      <p className="text-sm text-gray-200 whitespace-pre-wrap">{suggestion.improved}</p>
                      <button 
                        onClick={() => copyToClipboard(suggestion.improved)}
                        className="absolute top-3 right-3 text-gray-400 hover:text-white p-1 rounded-md hover:bg-gray-700 transition-colors"
                        title="Copy improved text"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                      </button>
                    </div>
                  </div>
                  <div className="mt-4 flex items-start space-x-2 text-sm text-gray-400 bg-gray-900/30 p-3 rounded-lg">
                    <svg className="w-5 h-5 text-accent flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <p><span className="font-semibold text-gray-300">Why:</span> {suggestion.reason}</p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}










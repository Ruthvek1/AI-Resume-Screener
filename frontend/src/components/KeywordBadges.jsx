import React, { useState } from 'react';

export default function KeywordBadges({ keywords }) {
  const [activeTooltip, setActiveTooltip] = useState(null);

  if (!keywords) return null;

  const found = keywords.found || [];
  const missing = keywords.missing || [];

  return (
    <div className="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
      <h3 className="text-lg font-semibold text-white mb-4">ATS Keywords</h3>
      
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-400 mb-2">Keywords Found</h4>
        <div className="flex flex-wrap gap-2">
          {found.map((kw, i) => (
            <div key={`found-${i}`} className="relative">
              <span 
                className="cursor-pointer inline-flex items-center px-3 py-1 rounded-md text-sm font-medium bg-green-500/10 text-green-400 border border-green-500/20 hover:bg-green-500/20 transition-colors"
                onClick={() => setActiveTooltip(activeTooltip === `found-${i}` ? null : `found-${i}`)}
              >
                {kw}
              </span>
              {activeTooltip === `found-${i}` && (
                <div className="absolute z-10 bottom-full mb-2 left-1/2 transform -translate-x-1/2 w-48 bg-gray-900 text-xs text-gray-200 p-2 rounded shadow-xl border border-gray-700">
                  This keyword was found in your resume and matches the ATS criteria.
                </div>
              )}
            </div>
          ))}
          {found.length === 0 && <span className="text-sm text-gray-500">None found.</span>}
        </div>
      </div>

      <div>
        <h4 className="text-sm font-medium text-gray-400 mb-2">Keywords Missing</h4>
        <div className="flex flex-wrap gap-2">
          {missing.map((kw, i) => (
            <div key={`missing-${i}`} className="relative">
              <span 
                className="cursor-pointer inline-flex items-center px-3 py-1 rounded-md text-sm font-medium bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20 transition-colors"
                onClick={() => setActiveTooltip(activeTooltip === `missing-${i}` ? null : `missing-${i}`)}
              >
                {kw}
              </span>
              {activeTooltip === `missing-${i}` && (
                <div className="absolute z-10 bottom-full mb-2 left-1/2 transform -translate-x-1/2 w-48 bg-gray-900 text-xs text-gray-200 p-2 rounded shadow-xl border border-gray-700">
                  This critical keyword is missing. Adding it can boost your ATS ranking.
                </div>
              )}
            </div>
          ))}
          {missing.length === 0 && <span className="text-sm text-gray-500">No missing keywords!</span>}
        </div>
      </div>
    </div>
  );
}








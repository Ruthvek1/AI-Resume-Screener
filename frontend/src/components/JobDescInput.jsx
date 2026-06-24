import React from 'react';

export default function JobDescInput({ value, onChange }) {
  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-300 mb-2">
        Job Description
      </label>
      <textarea
        className="w-full h-48 bg-gray-800/50 border border-gray-600 rounded-xl p-4 text-gray-200 placeholder-gray-500 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all resize-none"
        placeholder="Paste the target job description here..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

import React from 'react';

export default function SkillGapChart({ matching, missing, extra }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Matching Skills */}
      <div className="bg-gray-800/40 rounded-xl p-5 border border-green-900/30">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-green-400 uppercase tracking-wider">Matching</h3>
          <span className="bg-green-500/20 text-green-400 text-xs py-1 px-2 rounded-full font-bold">{matching?.length || 0}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {matching?.map((skill, i) => (
            <span key={i} className="inline-flex items-center px-2.5 py-1.5 rounded text-xs font-medium bg-green-500/10 text-green-300 border border-green-500/20">
              <svg className="w-3 h-3 mr-1 text-green-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path></svg>
              {skill}
            </span>
          ))}
          {(!matching || matching.length === 0) && <p className="text-gray-500 text-sm">No matching skills found.</p>}
        </div>
      </div>

      {/* Missing Skills */}
      <div className="bg-gray-800/40 rounded-xl p-5 border border-red-900/30">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-red-400 uppercase tracking-wider">Missing</h3>
          <span className="bg-red-500/20 text-red-400 text-xs py-1 px-2 rounded-full font-bold">{missing?.length || 0}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {missing?.map((skill, i) => (
            <span key={i} className="inline-flex items-center px-2.5 py-1.5 rounded text-xs font-medium bg-red-500/10 text-red-300 border border-red-500/20">
              <svg className="w-3 h-3 mr-1 text-red-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"></path></svg>
              {skill}
            </span>
          ))}
          {(!missing || missing.length === 0) && <p className="text-gray-500 text-sm">No missing skills.</p>}
        </div>
      </div>

      {/* Extra Skills */}
      <div className="bg-gray-800/40 rounded-xl p-5 border border-blue-900/30">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-blue-400 uppercase tracking-wider">Extra</h3>
          <span className="bg-blue-500/20 text-blue-400 text-xs py-1 px-2 rounded-full font-bold">{extra?.length || 0}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {extra?.map((skill, i) => (
            <span key={i} className="inline-flex items-center px-2.5 py-1.5 rounded text-xs font-medium bg-blue-500/10 text-blue-300 border border-blue-500/20">
              <svg className="w-3 h-3 mr-1 text-blue-400" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
              {skill}
            </span>
          ))}
          {(!extra || extra.length === 0) && <p className="text-gray-500 text-sm">No extra skills.</p>}
        </div>
      </div>
    </div>
  );
}









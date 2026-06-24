import React from 'react';
import { useNavigate } from 'react-router-dom';
import ScoreGauge from '../components/ScoreGauge';
import SkillGapChart from '../components/SkillGapChart';
import KeywordBadges from '../components/KeywordBadges';
import SuggestionPanel from '../components/SuggestionPanel';
import ModelBadge from '../components/ModelBadge';

export default function Results({ resultData }) {
  const navigate = useNavigate();

  // Redirect to home if no result data
  React.useEffect(() => {
    if (!resultData) {
      navigate('/');
    }
  }, [resultData, navigate]);

  if (!resultData) return null;

  const { result, model_used, processing_time_ms } = resultData;

  return (
    <div className="max-w-6xl mx-auto py-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 animate-fadeIn">
        <div>
          <button 
            onClick={() => navigate('/')}
            className="text-gray-400 hover:text-white flex items-center mb-4 transition-colors"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
            Back to Upload
          </button>
          <h1 className="text-3xl font-bold text-white mb-2">Analysis Results</h1>
          <ModelBadge modelUsed={model_used} timeMs={processing_time_ms} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Score & Summary */}
        <div className="lg:col-span-1 space-y-8 animate-slideUp">
          <div className="bg-gray-800/50 rounded-2xl p-8 border border-gray-700 text-center shadow-xl">
            <ScoreGauge score={result.match_score} />
            
            <div className="mt-8 text-left">
              <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-2">Executive Summary</h3>
              <p className="text-gray-300 text-sm leading-relaxed">{result.summary}</p>
            </div>

            {result.hire_likelihood && (
              <div className="mt-6 pt-6 border-t border-gray-700">
                <span className="text-sm text-gray-400">Hire Likelihood:</span>
                <span className="ml-2 font-bold text-lg text-white">{result.hire_likelihood}</span>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Details */}
        <div className="lg:col-span-2 space-y-8 animate-slideUp" style={{ animationDelay: '0.1s' }}>
          
          <div className="bg-gray-800/30 rounded-2xl p-6 border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-6">Skill Gap Analysis</h2>
            <SkillGapChart 
              matching={result.matching_skills} 
              missing={result.missing_skills} 
              extra={result.extra_skills} 
            />
          </div>

          <KeywordBadges keywords={result.ats_keywords} />

          <SuggestionPanel suggestions={result.improvement_suggestions} />

        </div>
      </div>
    </div>
  );
}







import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UploadZone from '../components/UploadZone';
import JobDescInput from '../components/JobDescInput';
import { useAnalyze } from '../hooks/useAnalyze';

export default function Home({ setAnalysisResult }) {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const { analyze, loading, error, result } = useAnalyze();
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    if (!file || !jobDescription) {
      alert("Please provide both a resume PDF and a job description.");
      return;
    }
    await analyze(file, jobDescription);
  };

  // If analysis is successful and result exists, navigate to Results
  React.useEffect(() => {
    if (result) {
      setAnalysisResult(result);
      navigate("/results");
    }
  }, [result, navigate, setAnalysisResult]);

  return (
    <div className="max-w-4xl mx-auto py-12">
      <div className="text-center mb-12 animate-fadeIn">
        <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-accent to-blue-500 mb-4 tracking-tight">
          AI Resume Screener
        </h1>
        <p className="text-lg text-gray-400 max-w-2xl mx-auto">
          Score your resume against any job description, find skill gaps, and get AI-powered improvement suggestions in seconds.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8 animate-slideUp">
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-white flex items-center">
            <span className="bg-accent/20 text-accent w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm">1</span>
            Upload Resume
          </h2>
          <UploadZone onFileSelect={setFile} />
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-white flex items-center">
            <span className="bg-accent/20 text-accent w-8 h-8 rounded-full flex items-center justify-center mr-3 text-sm">2</span>
            Target Job
          </h2>
          <JobDescInput value={jobDescription} onChange={setJobDescription} />
        </div>
      </div>

      {error && (
        <div className="mb-8 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-center animate-fadeIn">
          {error}
        </div>
      )}

      <div className="text-center animate-slideUp" style={{ animationDelay: '0.2s' }}>
        <button
          onClick={handleAnalyze}
          disabled={loading || !file || !jobDescription}
          className={`px-8 py-4 rounded-xl font-bold text-lg transition-all shadow-lg transform hover:-translate-y-1 ${
            loading 
              ? 'bg-gray-700 text-gray-400 cursor-not-allowed shadow-none hover:translate-y-0' 
              : !file || !jobDescription
                ? 'bg-accent/50 text-white/50 cursor-not-allowed'
                : 'bg-accent hover:bg-accent/80 text-white shadow-accent/25 hover:shadow-accent/40'
          }`}
        >
          {loading ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing Resume...
            </span>
          ) : (
            'Score My Resume'
          )}
        </button>
      </div>
    </div>
  );
}



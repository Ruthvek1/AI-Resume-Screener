import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Results from './pages/Results';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);

  return (
    <Router>
      <div className="min-h-screen bg-background text-gray-100 font-sans selection:bg-accent/30">
        {/* Navigation Bar */}
        <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <div className="flex items-center">
                <div className="w-8 h-8 rounded bg-gradient-to-br from-accent to-blue-500 flex items-center justify-center mr-3 shadow-lg shadow-accent/20">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                </div>
                <span className="font-bold text-xl tracking-tight">AI Resume Screener</span>
              </div>
              <div className="flex space-x-4">
                <a href="https://github.com/yourusername/ai-resume-screener" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white transition-colors">
                  GitHub
                </a>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="px-4 sm:px-6 lg:px-8 pb-12">
          <Routes>
            <Route path="/" element={<Home setAnalysisResult={setAnalysisResult} />} />
            <Route path="/results" element={<Results resultData={analysisResult} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;



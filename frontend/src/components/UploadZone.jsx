import React, { useState } from 'react';

export default function UploadZone({ onFileSelect }) {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === "application/pdf") {
        setFile(droppedFile);
        onFileSelect(droppedFile);
      } else {
        alert("Please upload a PDF file.");
      }
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.type === "application/pdf") {
        setFile(selectedFile);
        onFileSelect(selectedFile);
      } else {
        alert("Please upload a PDF file.");
      }
    }
  };

  return (
    <div 
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${dragActive ? 'border-accent bg-accent/10' : 'border-gray-600 bg-gray-800/50'}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input 
        type="file" 
        accept="application/pdf" 
        onChange={handleChange} 
        className="hidden" 
        id="file-upload" 
      />
      <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center justify-center space-y-3">
        <div className="w-16 h-16 bg-accent/20 rounded-full flex items-center justify-center text-accent">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
        </div>
        <div>
          <p className="text-lg font-medium text-gray-200">Drag & Drop your Resume (PDF)</p>
          <p className="text-sm text-gray-400 mt-1">or click to browse files</p>
        </div>
      </label>
      {file && (
        <div className="mt-4 p-3 bg-gray-900 rounded-lg flex items-center justify-between border border-gray-700">
          <span className="text-sm text-gray-300 truncate w-4/5 text-left">{file.name}</span>
          <span className="text-xs text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
        </div>
      )}
    </div>
  );
}








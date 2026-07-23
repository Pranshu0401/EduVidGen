"use client";
import { useEffect, useState } from "react";
import Navbar from "../../components/ui/Navbar";

interface PastVideo {
  title: string;
  video_url: string;
  scene_plan: string;
  manim_code: string;
}

export default function DashboardPage() {
  const [videos, setVideos] = useState<PastVideo[]>([]);
  const [error, setError] = useState("");
  const [expandedCard, setExpandedCard] = useState<number | null>(null);
  const [expandedCode, setExpandedCode] = useState<number | null>(null);
  const [videoErrors, setVideoErrors] = useState<{[key: number]: boolean}>({});

  const fetchVideos = async () => {
    const token = localStorage.getItem("token");

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/myvideos", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error("Failed to fetch videos");

      const data = await res.json();
      setVideos(data.reverse());
    } catch (err: any) {
      setError(err.message || "Failed to fetch videos.");
    }
  };

  useEffect(() => {
    fetchVideos();
  }, []);

  const toggleScenePlan = (idx: number) => {
    setExpandedCard(expandedCard === idx ? null : idx);
  };

  const toggleCode = (idx: number) => {
    setExpandedCode(expandedCode === idx ? null : idx);
  };

  const handleVideoError = (idx: number) => {
    setVideoErrors(prev => ({ ...prev, [idx]: true }));
  };

  const handleVideoLoad = (idx: number) => {
    setVideoErrors(prev => ({ ...prev, [idx]: false }));
  };

  return (
    <>
      
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950">
        <Navbar />
        {/* Hero Section */}
        <div className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/5 to-cyan-500/5"></div>
          <div className="relative max-w-7xl mx-auto px-6 py-16">
            <div className="text-center space-y-4">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-emerald-400 to-cyan-400 shadow-lg shadow-emerald-500/25 mb-6">
                <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z"/>
                </svg>
              </div>
              <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-50 via-gray-100 to-gray-200 bg-clip-text text-transparent">
                My Generated Videos
              </h1>
              <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                Explore your collection of AI-generated educational videos with their scene plans and source code
              </p>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-6 pb-12">
          {error && (
            <div className="mb-8 p-4 bg-red-500/5 border border-red-400/20 rounded-xl text-red-300 text-center backdrop-blur-sm">
              <div className="flex items-center justify-center space-x-2">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                </svg>
                <span>{error}</span>
              </div>
            </div>
          )}

          {videos.length === 0 ? (
            <div className="text-center py-16">
              <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gray-800/30 border border-gray-700/50 mb-6 backdrop-blur-sm">
                <svg className="w-12 h-12 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                </svg>
              </div>
              <h3 className="text-2xl font-semibold text-gray-300 mb-2">No videos yet</h3>
              <p className="text-gray-500 mb-6">Start creating your first educational video to see it here</p>
              <button className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-emerald-500 to-cyan-500 text-white font-medium rounded-xl hover:from-emerald-600 hover:to-cyan-600 transition-all duration-200 transform hover:scale-105 shadow-lg shadow-emerald-500/25">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4"/>
                </svg>
                Generate Video
              </button>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400/20 to-cyan-400/20 border border-emerald-400/30 flex items-center justify-center backdrop-blur-sm">
                    <span className="text-emerald-400 font-bold text-sm">{videos.length}</span>
                  </div>
                  <span className="text-gray-300 text-lg">
                    {videos.length === 1 ? '1 Video' : `${videos.length} Videos`}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
                {videos.map((video, idx) => (
                  <div
                    key={idx}
                    className="group bg-gray-900/40 backdrop-blur-xl rounded-2xl border border-gray-700/30 hover:border-emerald-400/30 shadow-xl hover:shadow-2xl hover:shadow-emerald-500/10 transition-all duration-500 transform hover:-translate-y-2 overflow-hidden"
                  >
                    {/* Video Section */}
                    <div className="relative group/video">
                      {!videoErrors[idx] ? (
                        <>
                          <video
                            src={video.video_url}
                            controls
                            preload="metadata"
                            className="w-full h-48 object-cover rounded-t-2xl bg-gray-800"
                            onError={() => handleVideoError(idx)}
                            onLoadedData={() => handleVideoLoad(idx)}
                            onLoadStart={() => console.log(`Video ${idx} loading started`)}
                          />
                          
                          {/* Play overlay for better UX */}
                          <div className="absolute inset-0 bg-gradient-to-t from-gray-900/40 to-transparent rounded-t-2xl opacity-0 group-hover/video:opacity-100 transition-opacity duration-300 flex items-center justify-center pointer-events-none">
                            <div className="w-16 h-16 bg-emerald-500/20 backdrop-blur-sm rounded-full flex items-center justify-center border border-emerald-400/30">
                              <svg className="w-8 h-8 text-emerald-300 ml-1" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M8 5v14l11-7z"/>
                              </svg>
                            </div>
                          </div>
                        </>
                      ) : (
                        /* Error fallback */
                        <div className="w-full h-48 bg-gray-800 rounded-t-2xl flex flex-col items-center justify-center text-gray-400 border-2 border-dashed border-gray-600">
                          <svg className="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                          </svg>
                          <p className="text-sm font-medium">Video Unavailable</p>
                          <p className="text-xs text-gray-500 mt-1 text-center px-4">Check if the video URL is accessible or try refreshing</p>
                          <button 
                            onClick={() => handleVideoLoad(idx)}
                            className="mt-2 px-3 py-1 bg-emerald-500/20 text-emerald-300 text-xs rounded-lg hover:bg-emerald-500/30 transition-colors"
                          >
                            Retry
                          </button>
                        </div>
                      )}
                    </div>

                    {/* Content Section */}
                    <div className="p-6 space-y-4">
                      <h3 className="text-xl font-bold text-gray-50 group-hover:text-emerald-300 transition-colors duration-300 line-clamp-2">
                        {video.title}
                      </h3>

                      {/* Scene Plan Section */}
                      <div className="space-y-2">
                        <button
                          onClick={() => toggleScenePlan(idx)}
                          className="flex items-center justify-between w-full p-3 bg-gray-800/20 border border-gray-700/30 hover:bg-gray-800/40 hover:border-gray-600/50 rounded-xl transition-all duration-300 group/btn backdrop-blur-sm"
                        >
                          <div className="flex items-center space-x-3">
                            <div className="w-6 h-6 rounded-lg bg-gradient-to-br from-blue-400/20 to-indigo-400/20 border border-blue-400/30 flex items-center justify-center">
                              <svg className="w-4 h-4 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                              </svg>
                            </div>
                            <span className="text-sm font-medium text-blue-300">Scene Plan</span>
                          </div>
                          <svg
                            className={`w-5 h-5 text-gray-400 transition-transform duration-300 ${
                              expandedCard === idx ? 'rotate-180' : ''
                            }`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7"/>
                          </svg>
                        </button>
                        
                        {expandedCard === idx && (
                          <div className="p-4 bg-gray-800/10 border border-gray-700/20 rounded-xl backdrop-blur-sm">
                            <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                              {video.scene_plan}
                            </p>
                          </div>
                        )}
                      </div>

                      {/* Manim Code Section */}
                      <div className="space-y-2">
                        <button
                          onClick={() => toggleCode(idx)}
                          className="flex items-center justify-between w-full p-3 bg-gray-800/20 border border-gray-700/30 hover:bg-gray-800/40 hover:border-gray-600/50 rounded-xl transition-all duration-300 group/btn backdrop-blur-sm"
                        >
                          <div className="flex items-center space-x-3">
                            <div className="w-6 h-6 rounded-lg bg-gradient-to-br from-emerald-400/20 to-teal-400/20 border border-emerald-400/30 flex items-center justify-center">
                              <svg className="w-4 h-4 text-emerald-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                              </svg>
                            </div>
                            <span className="text-sm font-medium text-emerald-300">Manim Code</span>
                          </div>
                          <svg
                            className={`w-5 h-5 text-gray-400 transition-transform duration-300 ${
                              expandedCode === idx ? 'rotate-180' : ''
                            }`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7"/>
                          </svg>
                        </button>
                        
                        {expandedCode === idx && (
                          <div className="relative">
                            <pre className="bg-gray-900/60 border border-gray-700/40 rounded-xl p-4 overflow-x-auto max-h-64 text-sm backdrop-blur-sm">
                              <code className="text-emerald-200 font-mono whitespace-pre-wrap">
                                {video.manim_code}
                              </code>
                            </pre>
                            <button
                              onClick={() => navigator.clipboard.writeText(video.manim_code)}
                              className="absolute top-3 right-3 p-2 bg-gray-800/60 hover:bg-gray-700/60 rounded-lg transition-colors duration-300 backdrop-blur-sm border border-gray-600/30"
                              title="Copy code"
                            >
                              <svg className="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                              </svg>
                            </button>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </main>
      </div>
    </>
  );
}   
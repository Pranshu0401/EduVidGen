"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";

interface PastVideo {
  title: string;
  video_url: string;
  scene_plan: string;
  manim_code: string;
}

export default function GeneratePage() {
  const [topic, setTopic] = useState("");
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [pastVideos, setPastVideos] = useState<PastVideo[]>([]);

  const fetchPastVideos = async () => {
    const token = localStorage.getItem("token");

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/myvideos", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error("Failed to load past videos");

      const data = await res.json();
      setPastVideos(data.reverse()); // latest first
    } catch (err: any) {
      console.error("Error fetching past videos:", err.message);
    }
  };

  useEffect(() => {
    fetchPastVideos();
  }, []);

  const handleGenerate = async () => {
    setError("");
    setVideoUrl(null);

    if (!topic.trim()) {
      setError("Please enter a topic.");
      return;
    }

    setLoading(true);

    try {
      const token = localStorage.getItem("token");

      const res = await fetch("http://localhost:8000/auth/generatetopic", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ topic }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to generate video");
      }

      const data = await res.json();
      setVideoUrl(data.video_url);
      fetchPastVideos(); // refresh list
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white py-10 px-4">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Top Section */}
        <div className="flex flex-col md:flex-row gap-10">
          {/* Left Panel */}
          <section className="flex flex-col flex-1 max-w-md space-y-5">
            <h1 className="text-4xl font-extrabold">🎬 Generate Video</h1>

            <textarea
              placeholder="Enter the topic for your video..."
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              rows={6}
              className="w-full rounded-lg bg-gray-800 p-4 text-white border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />

            {error && <p className="text-red-500 font-medium">{error}</p>}

            <Button
              onClick={handleGenerate}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-lg py-2"
            >
              {loading ? "Generating..." : "Generate Video"}
            </Button>
          </section>

          {/* Right Panel */}
          <section className="flex-1 bg-gray-900 rounded-xl shadow-xl overflow-hidden max-h-[420px] border border-gray-800">
            {videoUrl ? (
              <video
                src={videoUrl}
                controls
                autoPlay
                className="w-full h-full object-contain"
              />
            ) : (
              <div className="flex items-center justify-center h-full text-gray-400 text-lg p-8">
                <p>No video generated yet</p>
              </div>
            )}
          </section>
        </div>

        {/* Past Videos Section */}
        <section className="space-y-6">
          <h2 className="text-3xl font-bold">📜 Your Past Videos</h2>

          {pastVideos.length === 0 ? (
            <p className="text-gray-400">You haven't generated any videos yet.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {pastVideos.map((video, idx) => (
                <div
                  key={idx}
                  className="bg-gray-900 border border-gray-800 rounded-xl shadow-md hover:shadow-lg transition transform hover:-translate-y-1"
                >
                  <video
                    src={video.video_url}
                    controls
                    className="w-full h-48 object-cover rounded-t-xl"
                  />
                  <div className="p-4 space-y-2">
                    <h3 className="text-lg font-semibold truncate">{video.title}</h3>
                    <p className="text-sm text-gray-400 line-clamp-3">{video.scene_plan}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

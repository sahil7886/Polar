"use client";

import React, { useState, useEffect } from "react";
import { ChevronDown, ChevronLeft, ChevronRight, Star } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useUser } from '@auth0/nextjs-auth0';
import { auth0 } from "@/lib/auth0";

export default function Home() {
  const { user, error: userError, isLoading: userLoading } = useUser();
  
  const [videoSrc, setVideoSrc] = useState("");
  const [currentVideoId, setCurrentVideoId] = useState("");
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showSummary, setShowSummary] = useState(false);
  const [error, setError] = useState("");

  const fetchVideo = async () => {
    try {
      const response = await fetch(
        "http://localhost:5001/randomize_feed?user_id=67ba811352fcae1c36e18adc"
      );
      const data = await response.json();
      
      if (data && data.gridfs_id) {
        setVideoSrc(`http://localhost:5002/stream/${data.gridfs_id}`);
        setCurrentVideoId(data._id);
        setSummary(""); // Reset summary when new video loads
        setShowSummary(false); // Hide summary panel
      } else {
        setError("No valid video returned");
      }
    } catch (err) {
      setError("Failed to fetch video");
      console.error("Fetch error:", err);
    }
  };

  const fetchSummary = async () => {
    if (!currentVideoId) return;
    
    setIsLoading(true);
    setError("");
    
    try {
      const response = await fetch(
        `http://localhost:5001/summary/${currentVideoId}`
      );
      if (!response.ok) {
        throw new Error("Failed to fetch summary");
      }
      const data = await response.json();
      setSummary(data.summary || "No summary available");
      setShowSummary(true);
    } catch (err) {
      setError("Failed to fetch summary");
      console.error("Summary fetch error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchVideo();
    }
  }, [user]);

  // Show loading state while checking authentication
  if (userLoading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  // Show error if there's an authentication error
  if (userError) {
    console.log("USER UNAUTHENTICATED")
    return (
      <main className="flex items-center justify-center h-screen gap-4">
        <a href="/auth/login?screen_hint=signup" className="px-4 py-2 bg-gray-900 text-white rounded hover:bg-gray-700 transition-colors">
          Sign up
        </a>
        <a href="/auth/login" className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-400 transition-colors">
          Log in
        </a>
      </main>
    );
  }

  // If no user is authenticated, show sign-up and login buttons
  if (!user) {
    console.log("USER UNAUTHENTICATED")
    return (
      <main className="flex items-center justify-center h-screen gap-4">
        <a href="/auth/login?screen_hint=signup" className="px-4 py-2 bg-gray-800 text-white rounded hover:bg-gray-600 transition-colors">
          Sign up
        </a>
        <a href="/auth/login" className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-400 transition-colors">
          Log in
        </a>
      </main>
    );
  }

  if (!videoSrc) {
    return <div className="flex items-center justify-center h-screen">Loading video...</div>;
  }

  return (
    <div className="bg-white min-h-screen m-0 p-0">
      {/* Navigation Bar */}
      <nav className="bg-white p-4 text-center shadow-md">
        <h1 className="m-0 text-2xl font-bold">Polar</h1>
      </nav>

      {/* Main Content */}
      <main className="flex flex-col items-center min-h-[calc(100vh-70px)] p-4">
        {/* Video Container with Learn More Button */}
        <div className="relative">
          <video
            src={videoSrc}
            controls
            autoPlay
            muted
            className="rounded-lg max-h-[80vh] w-auto"
          />
          
          {/* Learn More Button */}
          <div
            className="absolute -right-12 top-0 flex items-center cursor-pointer group"
            onClick={fetchSummary}
          >
            <div className="flex items-center bg-white shadow-md rounded-full p-2 transition-all duration-300 hover:pr-4">
              <Star className="w-6 h-6 text-blue-500" />
              <span className="max-w-0 overflow-hidden whitespace-nowrap group-hover:max-w-xs transition-all duration-300 text-blue-500 ml-1">
                Learn more
              </span>
            </div>
          </div>
        </div>

        {/* Summary Panel */}
        {showSummary && (
          <div className="mt-4 w-full max-w-2xl bg-white rounded-lg shadow-lg p-4">
            <h3 className="text-lg font-semibold mb-2">Video Summary</h3>
            {isLoading ? (
              <p>Loading summary...</p>
            ) : (
              <p className="text-gray-700">{summary}</p>
            )}
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive" className="mt-4">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Navigation Buttons */}
        <div className="mt-4 flex gap-4">
          <ChevronLeft
            onClick={fetchVideo}
            className="w-8 h-8 cursor-pointer hover:text-blue-500 transition-colors"
            aria-label="Left Reel"
          />
          <ChevronDown
            onClick={fetchVideo}
            className="w-8 h-8 cursor-pointer hover:text-blue-500 transition-colors"
            aria-label="Next Reel"
          />
          <ChevronRight
            onClick={fetchVideo}
            className="w-8 h-8 cursor-pointer hover:text-blue-500 transition-colors"
            aria-label="Right Reel"
          />
        </div>
      </main>
    </div>
  );
}
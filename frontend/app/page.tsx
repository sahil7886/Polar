"use client";

import React, { useState, useEffect } from "react";
import { ChevronDown, ChevronLeft, ChevronRight } from "lucide-react";

export default function Home() {
  const [videoSrc, setVideoSrc] = useState("");

  // All three fetchers can point to the same logic for now, or you can
  // modify them independently later.
  const fetchNextVideo = () => {
    fetch("http://localhost:5001/randomize_feed?user_id=67ba811352fcae1c36e18adc")
      .then((res) => res.json())
      .then((data) => {
        if (data && data.gridfs_id) {
          setVideoSrc(`http://localhost:5002/stream/${data.gridfs_id}`);
        } else {
          console.error("No valid video returned:", data);
        }
      })
      .catch((err) => console.error("Fetch error:", err));
  };

  const fetchLeftVideo = () => {
    // Same logic for now
    fetch("http://localhost:5001/randomize_feed?user_id=67ba811352fcae1c36e18adc")
      .then((res) => res.json())
      .then((data) => {
        if (data && data.gridfs_id) {
          setVideoSrc(`http://localhost:5002/stream/${data.gridfs_id}`);
        } else {
          console.error("No valid video returned:", data);
        }
      })
      .catch((err) => console.error("Fetch error:", err));
  };

  const fetchRightVideo = () => {
    // Same logic for now
    fetch("http://localhost:5001/randomize_feed?user_id=67ba811352fcae1c36e18adc")
      .then((res) => res.json())
      .then((data) => {
        if (data && data.gridfs_id) {
          setVideoSrc(`http://localhost:5002/stream/${data.gridfs_id}`);
        } else {
          console.error("No valid video returned:", data);
        }
      })
      .catch((err) => console.error("Fetch error:", err));
  };

  // Fetch the initial video on mount
  useEffect(() => {
    fetchNextVideo();
  }, []);

  if (!videoSrc) {
    return <div>Loading video...</div>;
  }

  return (
    <div
      style={{
        background: "white",
        minHeight: "100vh",
        margin: 0,
        padding: 0,
      }}
    >
      {/* Navigation Bar */}
      <nav
        style={{
          backgroundColor: "white",
          padding: "1rem",
          textAlign: "center",
          boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
        }}
      >
        <h1 style={{ margin: 0 }}>Polar</h1>
      </nav>

      {/* Main Content */}
      <main
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          minHeight: "calc(100vh - 70px)", // subtract nav bar height + any padding
          padding: "1rem",
        }}
      >
        <video
          src={videoSrc}
          controls
          autoPlay
          muted
          style={{
            borderRadius: "10px",
            maxHeight: "80vh",
            width: "auto",
          }}
        />

        {/* Buttons Row */}
        <div style={{ marginTop: "1rem", display: "flex", gap: "1rem" }}>
          <ChevronLeft
            onClick={fetchLeftVideo}
            style={{
              fontSize: "2rem",
              cursor: "pointer",
            }}
            aria-label="Left Reel"
          />
          <ChevronDown
            onClick={fetchNextVideo}
            style={{
              fontSize: "2rem",
              cursor: "pointer",
            }}
            aria-label="Next Reel"
          />
          <ChevronRight
            onClick={fetchRightVideo}
            style={{
              fontSize: "2rem",
              cursor: "pointer",
            }}
            aria-label="Right Reel"
          />
        </div>
      </main>
    </div>
  );
}

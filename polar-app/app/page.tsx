"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"

const initialVideos = [
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
  // Add more video URLs as needed
]

export default function Home() {
  const [videos, setVideos] = useState(initialVideos)
  const containerRef = useRef<HTMLDivElement>(null)
  const observerRef = useRef<IntersectionObserver | null>(null)

  useEffect(() => {
    const options = {
      root: null,
      rootMargin: "0px",
      threshold: 0.5,
    }

    observerRef.current = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const video = entry.target as HTMLVideoElement
          video.play()
        } else {
          const video = entry.target as HTMLVideoElement
          video.pause()
        }
      })
    }, options)

    const videoElements = document.querySelectorAll("video")
    videoElements.forEach((video) => {
      observerRef.current?.observe(video)
    })

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect()
      }
    }
  }, [])

  useEffect(() => {
    const handleScroll = () => {
      if (containerRef.current) {
        const { scrollTop, clientHeight, scrollHeight } = containerRef.current
        if (scrollHeight - scrollTop <= clientHeight * 1.5) {
          setVideos((prevVideos) => [...prevVideos, ...initialVideos])
        }
      }
    }

    containerRef.current?.addEventListener("scroll", handleScroll)
    return () => containerRef.current?.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <main className="min-h-screen bg-white text-black">
      <header className="fixed top-0 left-0 right-0 bg-white z-10 p-4 shadow-md">
        <h1 className="text-2xl font-bold">Polar</h1>
      </header>
      <div ref={containerRef} className="pt-16 pb-8 h-screen overflow-y-scroll snap-y snap-mandatory">
        {videos.map((videoSrc, index) => (
          <VideoItem key={`${videoSrc}-${index}`} src={videoSrc} />
        ))}
      </div>
    </main>
  )
}

function VideoItem({ src }: { src: string }) {
  const [showInsights, setShowInsights] = useState(false)

  const handleLearnMore = () => {
    setShowInsights(!showInsights)
  }

  return (
    <div className="flex justify-center items-center h-[calc(100vh-4rem)] snap-start py-4">
      <div className="relative w-full max-w-[calc((100vh-4rem)*9/16)] h-[calc(100vh-6rem)]">
        <div className="absolute inset-0 rounded-2xl overflow-hidden">
          <video src={src} className="w-full h-full object-cover" loop muted playsInline />
        </div>
        <Button onClick={handleLearnMore} className="absolute bottom-4 right-4 bg-white text-black hover:bg-gray-200">
          Learn More
        </Button>
        {showInsights && (
          <div className="absolute bottom-16 right-4 bg-white p-4 rounded-md shadow-lg max-w-[200px]">
            <p className="text-sm">AI-generated insights about this video would appear here.</p>
          </div>
        )}
      </div>
    </div>
  )
}


"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { motion, AnimatePresence, type PanInfo } from "framer-motion"

// Create a larger pool of videos
const videoPool = [
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
  "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
]

// Initialize feed with first 3 videos
const initialFeed = videoPool.slice(0, 3)

export default function Home() {
  const [feed, setFeed] = useState(initialFeed)
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

  const handleSwapVideo = (index: number, direction: "next" | "prev") => {
    setFeed((currentFeed) => {
      const newFeed = [...currentFeed]
      const currentVideoIndex = videoPool.indexOf(currentFeed[index])
      let nextVideoIndex: number

      if (direction === "next") {
        nextVideoIndex = (currentVideoIndex + 1) % videoPool.length
      } else {
        nextVideoIndex = (currentVideoIndex - 1 + videoPool.length) % videoPool.length
      }

      newFeed[index] = videoPool[nextVideoIndex]
      return newFeed
    })
  }

  return (
    <main className="min-h-screen bg-white text-black">
      <header className="fixed top-0 left-0 right-0 bg-white z-10 p-4 shadow-md">
        <h1 className="text-2xl font-bold">Polar</h1>
      </header>
      <div ref={containerRef} className="pt-16 pb-8 h-screen overflow-y-scroll snap-y snap-mandatory">
        {feed.map((videoSrc, index) => (
          <VideoItem
            key={`${videoSrc}-${index}`}
            src={videoSrc}
            onNext={() => handleSwapVideo(index, "next")}
            onPrev={() => handleSwapVideo(index, "prev")}
          />
        ))}
      </div>
    </main>
  )
}

interface VideoItemProps {
  src: string
  onNext: () => void
  onPrev: () => void
}

function VideoItem({ src, onNext, onPrev }: VideoItemProps) {
  const [showInsights, setShowInsights] = useState(false)
  const [showControls, setShowControls] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)
  const [dragStart, setDragStart] = useState<number | null>(null)

  const handleLearnMore = () => {
    setShowInsights(!showInsights)
  }

  const handleDrag = (event: PanInfo) => {
    if (Math.abs(event.offset.x) > 100) {
      if (event.offset.x > 0) {
        onPrev()
      } else {
        onNext()
      }
    }
  }

  return (
    <div
      className="flex justify-center items-center h-[calc(100vh-4rem)] snap-start py-4 relative group"
      onMouseEnter={() => setShowControls(true)}
      onMouseLeave={() => setShowControls(false)}
      ref={containerRef}
    >
      <div className="absolute left-4 top-1/2 -translate-y-1/2 z-20 transition-opacity duration-200 opacity-0 group-hover:opacity-100">
        <Button
          onClick={onPrev}
          variant="outline"
          size="icon"
          className="rounded-full bg-white/80 backdrop-blur-sm hover:bg-white shadow-lg"
        >
          <ChevronLeft className="h-6 w-6" />
        </Button>
      </div>

      <motion.div
        className="relative w-full max-w-[calc((100vh-4rem)*9/16)] h-[calc(100vh-6rem)]"
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        onDragEnd={(_, info) => handleDrag(info)}
      >
        <AnimatePresence mode="wait">
          <motion.div
            key={src}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.3 }}
            className="absolute inset-0 rounded-2xl overflow-hidden bg-black"
          >
            <video src={src} className="w-full h-full object-cover" loop muted playsInline />
          </motion.div>
        </AnimatePresence>

        <Button
          onClick={handleLearnMore}
          className="absolute bottom-4 right-4 bg-white text-black hover:bg-gray-200 z-20"
        >
          Learn More
        </Button>

        {showInsights && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="absolute bottom-16 right-4 bg-white p-4 rounded-md shadow-lg max-w-[200px] z-20"
          >
            <p className="text-sm">AI-generated insights about this video would appear here.</p>
          </motion.div>
        )}
      </motion.div>

      <div className="absolute right-4 top-1/2 -translate-y-1/2 z-20 transition-opacity duration-200 opacity-0 group-hover:opacity-100">
        <Button
          onClick={onNext}
          variant="outline"
          size="icon"
          className="rounded-full bg-white/80 backdrop-blur-sm hover:bg-white shadow-lg"
        >
          <ChevronRight className="h-6 w-6" />
        </Button>
      </div>
    </div>
  )
}


'use client'

import { useState, useCallback } from 'react'
import type { StoryRequest, MediaContent, StoryChunk } from '@/lib/types'

export function useStoryGeneration() {
  const [storyContent, setStoryContent] = useState<MediaContent[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)

  const generateStory = useCallback(async (request: StoryRequest) => {
    setIsGenerating(true)
    setProgress(0)
    setError(null)
    setStoryContent([])

    try {
      const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'
      const ws = new WebSocket(`${wsUrl}/ws/story`)

      ws.onopen = () => {
        console.log('WebSocket connected')
        ws.send(JSON.stringify(request))
      }

      ws.onmessage = (event) => {
        const chunk: StoryChunk = JSON.parse(event.data)

        if (chunk.chunk_type === 'metadata') {
          // Update progress based on metadata
          const status = chunk.content?.status
          if (status === 'planning') setProgress(10)
          else if (status === 'planning_complete') setProgress(20)
          else if (status === 'style_defined') setProgress(30)
          else if (status === 'generating_scene') {
            const scene = chunk.content?.scene || 0
            const total = chunk.content?.total || 1
            setProgress(30 + (scene / total) * 60)
          }
          else if (status === 'complete') setProgress(100)
        }

        // Add content to story
        const mediaContent: MediaContent = {
          type: chunk.chunk_type as any,
          content: chunk.content,
          metadata: chunk.content?.metadata,
          timestamp: chunk.timestamp,
        }

        setStoryContent((prev) => [...prev, mediaContent])

        if (chunk.is_final) {
          setIsGenerating(false)
          ws.close()
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setError('Connection error occurred')
        setIsGenerating(false)
      }

      ws.onclose = () => {
        console.log('WebSocket closed')
        setIsGenerating(false)
      }

    } catch (err) {
      console.error('Story generation failed:', err)
      setError(err instanceof Error ? err.message : 'An error occurred')
      setIsGenerating(false)
    }
  }, [])

  return {
    storyContent,
    isGenerating,
    progress,
    error,
    generateStory,
  }
}

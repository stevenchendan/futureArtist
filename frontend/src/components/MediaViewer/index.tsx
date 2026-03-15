'use client'

import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import type { MediaContent } from '@/lib/types'

const TONE_SETTINGS: Record<string, { rate: number; pitch: number; label: string }> = {
  playful:      { rate: 1.15, pitch: 1.4,  label: 'Playful' },
  neutral:      { rate: 1.0,  pitch: 1.0,  label: 'Neutral' },
  professional: { rate: 0.95, pitch: 0.85, label: 'Professional' },
  inspiring:    { rate: 1.05, pitch: 1.15, label: 'Inspiring' },
  suspenseful:  { rate: 0.9,  pitch: 0.75, label: 'Suspenseful' },
  serious:      { rate: 0.88, pitch: 0.8,  label: 'Serious' },
}

interface MediaViewerProps {
  content: MediaContent[]
  isGenerating: boolean
  tone?: string
}

function AudioPlayer({ text, tone }: { text: string; tone?: string }) {
  const [speaking, setSpeaking] = useState(false)
  const toneConfig = TONE_SETTINGS[tone ?? 'neutral'] ?? TONE_SETTINGS.neutral

  const play = useCallback(() => {
    if (!text) return
    window.speechSynthesis.cancel()
    const utterance = new SpeechSynthesisUtterance(text)
    utterance.rate = toneConfig.rate
    utterance.pitch = toneConfig.pitch
    utterance.onstart = () => setSpeaking(true)
    utterance.onend = () => setSpeaking(false)
    utterance.onerror = () => setSpeaking(false)
    window.speechSynthesis.speak(utterance)
  }, [text, toneConfig])

  const stop = useCallback(() => {
    window.speechSynthesis.cancel()
    setSpeaking(false)
  }, [])

  return (
    <div className="bg-gray-100 rounded-lg p-4">
      <p className="text-sm font-medium text-gray-700 mb-3">Audio Narration</p>
      <div className="flex items-center space-x-3">
        {!speaking ? (
          <button
            onClick={play}
            className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium px-4 py-2 rounded-full transition-colors"
          >
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M8 5v14l11-7z" />
            </svg>
            <span>Play</span>
          </button>
        ) : (
          <button
            onClick={stop}
            className="flex items-center space-x-2 bg-red-500 hover:bg-red-600 text-white text-sm font-medium px-4 py-2 rounded-full transition-colors"
          >
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6 6h12v12H6z" />
            </svg>
            <span>Stop</span>
          </button>
        )}
        {speaking && (
          <div className="flex space-x-1 items-center">
            <div className="w-1 h-4 bg-purple-500 rounded animate-bounce" style={{ animationDelay: '0s' }} />
            <div className="w-1 h-6 bg-purple-500 rounded animate-bounce" style={{ animationDelay: '0.1s' }} />
            <div className="w-1 h-3 bg-purple-500 rounded animate-bounce" style={{ animationDelay: '0.2s' }} />
            <div className="w-1 h-5 bg-purple-500 rounded animate-bounce" style={{ animationDelay: '0.3s' }} />
          </div>
        )}
      </div>
      <p className="text-xs text-gray-500 mt-2 italic">Tone: {toneConfig.label} · Reads the story text above</p>
    </div>
  )
}

export default function MediaViewer({ content, isGenerating, tone }: MediaViewerProps) {
  return (
    <div className="space-y-6">
      <AnimatePresence>
        {content.map((item, index) => (
          <motion.div
            key={`${item.type}-${index}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="border-l-4 border-purple-500 pl-4"
          >
            {item.type === 'text' && (
              <div className="prose max-w-none">
                <ReactMarkdown>{typeof item.content === 'string' ? item.content : item.content?.text ?? ''}</ReactMarkdown>
              </div>
            )}

            {item.type === 'image' && (
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="aspect-video bg-gradient-to-br from-purple-200 to-blue-200 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    {item.content?.generated_data && (
                      <img src={`data:image/png;base64,${item.content.generated_data}`} alt="Generated Image" className="mt-2 rounded-lg shadow-md" />
                    )}
                  </div>
                </div>
              </div>
            )}

            {item.type === 'audio' && (() => {
              const prevText = content
                .slice(0, index)
                .reverse()
                .find((c) => c.type === 'text')
              const fullText = typeof prevText?.content === 'string'
                ? prevText.content
                : prevText?.content?.text ?? item.content?.narration_text ?? ''
              return <AudioPlayer text={fullText} tone={tone} />
            })()}

            {item.type === 'video' && (
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="aspect-video bg-gradient-to-br from-blue-200 to-purple-200 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <svg
                      className="mx-auto h-16 w-16 text-gray-400 mb-2"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1}
                        d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                      />
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1}
                        d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <p className="text-sm text-gray-600">Video Preview</p>
                    {item.metadata?.duration && (
                      <p className="text-xs text-gray-500 mt-1">
                        Duration: {item.metadata.duration}s
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {item.type === 'metadata' && item.metadata?.status && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <p className="text-sm text-blue-800">
                  Status: {item.metadata.status}
                </p>
              </div>
            )}
          </motion.div>
        ))}
      </AnimatePresence>

      {isGenerating && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex items-center justify-center py-8"
        >
          <div className="flex space-x-2">
            <div className="w-3 h-3 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
            <div className="w-3 h-3 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
            <div className="w-3 h-3 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
          </div>
        </motion.div>
      )}
    </div>
  )
}

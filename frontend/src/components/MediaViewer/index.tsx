'use client'

import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import type { MediaContent } from '@/lib/types'

interface MediaViewerProps {
  content: MediaContent[]
  isGenerating: boolean
}

export default function MediaViewer({ content, isGenerating }: MediaViewerProps) {
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
                <ReactMarkdown>{item.content as string}</ReactMarkdown>
              </div>
            )}

            {item.type === 'image' && (
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="aspect-video bg-gradient-to-br from-purple-200 to-blue-200 rounded-lg flex items-center justify-center">
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
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    <p className="text-sm text-gray-600">Image Preview</p>
                    {item.metadata?.prompt && (
                      <p className="text-xs text-gray-500 mt-1 max-w-md mx-auto">
                        {item.metadata.prompt}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {item.type === 'audio' && (
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="flex items-center space-x-4">
                  <svg
                    className="h-12 w-12 text-purple-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
                    />
                  </svg>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-700">Audio Preview</p>
                    {item.metadata?.narration_text && (
                      <p className="text-xs text-gray-500 mt-1">
                        {item.metadata.narration_text.substring(0, 100)}...
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}

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

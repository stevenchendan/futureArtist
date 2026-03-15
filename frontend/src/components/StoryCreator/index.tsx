'use client'

import { useState, useEffect } from 'react'
import ControlPanel from '../ControlPanel'
import MediaViewer from '../MediaViewer'
import ExportTools from '../ExportTools'
import { useStoryGeneration } from '@/hooks/useStoryGeneration'
import type { StoryRequest } from '@/lib/types'

export default function StoryCreator() {
  const [storyRequest, setStoryRequest] = useState<StoryRequest | null>(null)
  const [readingMode, setReadingMode] = useState(false)
  const { storyContent, isGenerating, progress, generateStory } = useStoryGeneration()

  const handleGenerate = async (request: StoryRequest) => {
    setStoryRequest(request)
    await generateStory(request)
  }

  useEffect(() => {
    if (!readingMode) return
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setReadingMode(false) }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [readingMode])

  return (
    <>
      {/* Reading Mode Overlay */}
      {readingMode && (
        <div className="fixed inset-0 z-50 bg-amber-50 overflow-y-auto">
          <div className="max-w-5xl mx-auto px-12 py-12">
            <div className="flex justify-end mb-8">
              <button
                onClick={() => setReadingMode(false)}
                className="flex items-center space-x-2 bg-gray-200 hover:bg-gray-300 text-gray-600 text-sm font-medium px-4 py-2 rounded-full transition-colors"
              >
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span>Exit Reading Mode</span>
              </button>
            </div>
            <div className="prose prose-xl max-w-none text-gray-900 prose-headings:text-gray-900 prose-p:leading-relaxed prose-p:text-gray-800">
              <MediaViewer content={storyContent} isGenerating={false} tone={storyRequest?.tone} />
            </div>
            <p className="text-center text-gray-400 text-xs mt-12">Press ESC to exit</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Control Panel - Left Column */}
        <div className="lg:col-span-1">
          <ControlPanel onGenerate={handleGenerate} isGenerating={isGenerating} />
        </div>

        {/* Media Viewer - Middle Column */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Your Story</h2>
              <div className="flex items-center space-x-2">
                {storyContent.length > 0 && (
                  <button
                    onClick={() => setReadingMode(true)}
                    className="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium px-4 py-2 rounded-full transition-colors"
                  >
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                    <span>Reading Mode</span>
                  </button>
                )}
                {storyContent.length > 0 && <ExportTools storyContent={storyContent} />}
              </div>
            </div>

            {isGenerating && (
              <div className="mb-4">
                <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                  <span>Generating...</span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-purple-600 to-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            )}

            <MediaViewer content={storyContent} isGenerating={isGenerating} tone={storyRequest?.tone} />

            {!isGenerating && storyContent.length === 0 && (
              <div className="text-center py-20 text-gray-400">
                <svg
                  className="mx-auto h-24 w-24 mb-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1}
                    d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"
                  />
                </svg>
                <p className="text-lg">Start creating your story</p>
                <p className="text-sm mt-2">Configure your settings and click Generate</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

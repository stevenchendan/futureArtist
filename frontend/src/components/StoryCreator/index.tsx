'use client'

import { useState } from 'react'
import ControlPanel from '../ControlPanel'
import MediaViewer from '../MediaViewer'
import ExportTools from '../ExportTools'
import { useStoryGeneration } from '@/hooks/useStoryGeneration'
import type { StoryRequest } from '@/lib/types'

export default function StoryCreator() {
  const [storyRequest, setStoryRequest] = useState<StoryRequest | null>(null)
  const { storyContent, isGenerating, progress, generateStory } = useStoryGeneration()

  const handleGenerate = async (request: StoryRequest) => {
    setStoryRequest(request)
    await generateStory(request)
  }

  return (
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
            {storyContent.length > 0 && <ExportTools storyContent={storyContent} />}
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

          <MediaViewer content={storyContent} isGenerating={isGenerating} />

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
  )
}

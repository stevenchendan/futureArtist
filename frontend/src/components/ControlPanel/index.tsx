'use client'

import { useState } from 'react'
import type { StoryRequest } from '@/lib/types'

interface ControlPanelProps {
  onGenerate: (request: StoryRequest) => void
  isGenerating: boolean
}

export default function ControlPanel({ onGenerate, isGenerating }: ControlPanelProps) {
  const [prompt, setPrompt] = useState('')
  const [storyType, setStoryType] = useState<StoryRequest['story_type']>('storybook')
  const [targetAudience, setTargetAudience] = useState('general')
  const [tone, setTone] = useState('neutral')
  const [length, setLength] = useState<StoryRequest['length']>('medium')
  const [style, setStyle] = useState('modern')
  const [includeMedia, setIncludeMedia] = useState<StoryRequest['include_media']>(['text', 'images'])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    onGenerate({
      prompt,
      story_type: storyType,
      target_audience: targetAudience,
      tone,
      length,
      style,
      include_media: includeMedia,
      interleaved: true,
    })
  }

  const toggleMedia = (media: string) => {
    setIncludeMedia(prev =>
      prev.includes(media as any)
        ? prev.filter(m => m !== media)
        : [...prev, media as any]
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Story Configuration</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Prompt */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Story Prompt
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            rows={4}
            placeholder="Describe your story idea..."
            disabled={isGenerating}
          />
        </div>

        {/* Story Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Story Type
          </label>
          <select
            value={storyType}
            onChange={(e) => setStoryType(e.target.value as any)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
            disabled={isGenerating}
          >
            <option value="storybook">Interactive Storybook</option>
            <option value="marketing">Marketing Assets</option>
            <option value="educational">Educational Content</option>
            <option value="social">Social Media</option>
          </select>
        </div>

        {/* Target Audience */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target Audience
          </label>
          <select
            value={targetAudience}
            onChange={(e) => setTargetAudience(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
            disabled={isGenerating}
          >
            <option value="children">Children</option>
            <option value="adults">Adults</option>
            <option value="professionals">Professionals</option>
            <option value="general">General</option>
          </select>
        </div>

        {/* Tone */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tone
          </label>
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
            disabled={isGenerating}
          >
            <option value="playful">Playful</option>
            <option value="professional">Professional</option>
            <option value="inspiring">Inspiring</option>
            <option value="neutral">Neutral</option>
          </select>
        </div>

        {/* Length */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Length
          </label>
          <div className="flex gap-2">
            {['short', 'medium', 'long'].map((l) => (
              <button
                key={l}
                type="button"
                onClick={() => setLength(l as any)}
                className={`flex-1 py-2 px-4 rounded-lg border transition-colors ${
                  length === l
                    ? 'bg-purple-600 text-white border-purple-600'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-purple-400'
                }`}
                disabled={isGenerating}
              >
                {l.charAt(0).toUpperCase() + l.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Visual Style */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Visual Style
          </label>
          <select
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
            disabled={isGenerating}
          >
            <option value="cartoon">Cartoon</option>
            <option value="realistic">Realistic</option>
            <option value="minimalist">Minimalist</option>
            <option value="modern">Modern</option>
          </select>
        </div>

        {/* Media Types */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Include Media
          </label>
          <div className="space-y-2">
            {[
              { value: 'text', label: 'Text' },
              { value: 'images', label: 'Images' },
              { value: 'audio', label: 'Audio' },
            ].map((media) => (
              <label key={media.value} className="flex items-center">
                <input
                  type="checkbox"
                  checked={includeMedia.includes(media.value as any)}
                  onChange={() => toggleMedia(media.value)}
                  className="mr-2 h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
                  disabled={isGenerating}
                />
                <span className="text-sm text-gray-700">{media.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Generate Button */}
        <button
          type="submit"
          disabled={isGenerating || !prompt.trim()}
          className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isGenerating ? 'Generating...' : 'Generate Story'}
        </button>
      </form>
    </div>
  )
}

'use client'

import StoryCreator from '@/components/StoryCreator'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-4">
            Future Artist
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create stunning multimodal stories with AI
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Powered by Gemini 2.0 with Interleaved Output
          </p>
        </header>

        <StoryCreator />
      </div>
    </main>
  )
}

/**
 * Shared types for story generation (aligned with backend models).
 */

export type StoryType = 'storybook' | 'marketing' | 'educational' | 'social'
export type StoryLength = 'short' | 'medium' | 'long'
export type MediaKind = 'text' | 'images' | 'audio' | 'video'
export type MediaContentType = 'text' | 'image' | 'audio' | 'video' | 'metadata'
export type ChunkType = 'text' | 'image' | 'audio' | 'video' | 'metadata'

export interface StoryRequest {
  prompt: string
  story_type: StoryType
  target_audience?: string
  tone?: string
  length: StoryLength
  style?: string
  include_media: MediaKind[]
  interleaved?: boolean
  color_palette?: string[] | null
  additional_instructions?: string | null
}

export interface MediaContent {
  type: MediaContentType
  content: any
  metadata?: Record<string, any> | null
  timestamp?: string
}

export interface StoryChunk {
  chunk_id: string
  chunk_type: ChunkType
  content: any
  sequence: number
  is_final?: boolean
  timestamp?: string
}

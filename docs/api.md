# API Documentation

## Base URL

```
Production: https://your-backend-url.run.app
Development: http://localhost:8000
```

## Authentication

Currently, the API uses unauthenticated access for hackathon purposes. For production, implement OAuth 2.0 or API key authentication.

## Endpoints

### Health Check

#### GET `/`

Returns basic service information.

**Response:**
```json
{
  "status": "online",
  "service": "Future Artist",
  "version": "0.1.0",
  "gemini_model": "gemini-2.0-flash-exp"
}
```

#### GET `/health`

Returns detailed health status.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "gemini": "connected",
    "storage": "connected"
  }
}
```

### Story Generation

#### POST `/api/v1/story/generate`

Generate a multimodal story with streaming response.

**Request Body:**
```json
{
  "prompt": "A robot learning to paint in a futuristic art studio",
  "story_type": "storybook",
  "target_audience": "children",
  "tone": "playful",
  "length": "medium",
  "style": "cartoon",
  "include_media": ["text", "images", "audio"],
  "interleaved": true,
  "color_palette": ["#FF6B9D", "#C44569", "#FFD93D"],
  "additional_instructions": "Make it educational about colors"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prompt | string | Yes | Main story prompt or theme |
| story_type | enum | Yes | One of: `storybook`, `marketing`, `educational`, `social` |
| target_audience | string | No | Target audience (default: "general") |
| tone | string | No | Story tone (default: "neutral") |
| length | enum | Yes | One of: `short`, `medium`, `long` |
| style | string | No | Visual style (default: "modern") |
| include_media | array | Yes | Array of media types to include |
| interleaved | boolean | No | Enable interleaved output (default: true) |
| color_palette | array | No | Array of hex color codes |
| additional_instructions | string | No | Additional creative instructions |

**Story Types:**
- `storybook`: Interactive children's stories with illustrations
- `marketing`: Marketing campaign materials
- `educational`: Educational content with explanations
- `social`: Social media content packages

**Media Types:**
- `text`: Narrative text and dialogue
- `images`: Generated illustrations
- `audio`: Narration and sound effects
- `video`: Video sequences and animations

**Length Options:**
- `short`: 3-5 scenes
- `medium`: 6-10 scenes
- `long`: 11-15 scenes

**Response:**

Streaming NDJSON (Newline Delimited JSON):

```json
{"story_id": "abc123", "chunk_type": "metadata", "content": {"status": "planning"}, "sequence": 0}
{"story_id": "abc123", "chunk_type": "text", "content": {"text": "Once upon a time..."}, "sequence": 1}
{"story_id": "abc123", "chunk_type": "image", "content": {"prompt": "Robot with paintbrush"}, "sequence": 2}
{"story_id": "abc123", "chunk_type": "metadata", "content": {"status": "complete"}, "sequence": 10, "is_final": true}
```

**Chunk Types:**

- `metadata`: Status updates and progress information
- `text`: Text content with narrative
- `image`: Image data or prompts
- `audio`: Audio configuration and data
- `video`: Video specifications and data

#### WebSocket `/ws/story`

Real-time story generation with WebSocket connection.

**Connect:**
```javascript
const ws = new WebSocket('wss://your-backend-url.run.app/ws/story')
```

**Send Request:**
```json
{
  "prompt": "A brave little mouse on an adventure",
  "story_type": "storybook",
  "length": "short",
  "include_media": ["text", "images"]
}
```

**Receive Messages:**

Same format as HTTP streaming endpoint, but via WebSocket messages.

**Connection Events:**

- `open`: Connection established, send story request
- `message`: Receive story chunks
- `close`: Story generation complete
- `error`: Connection error occurred

**Example Usage:**

```javascript
const ws = new WebSocket('wss://your-backend-url.run.app/ws/story')

ws.onopen = () => {
  ws.send(JSON.stringify({
    prompt: "A robot learning to paint",
    story_type: "storybook",
    length: "medium",
    include_media: ["text", "images"]
  }))
}

ws.onmessage = (event) => {
  const chunk = JSON.parse(event.data)
  console.log('Received chunk:', chunk)

  if (chunk.is_final) {
    console.log('Story generation complete!')
    ws.close()
  }
}

ws.onerror = (error) => {
  console.error('WebSocket error:', error)
}
```

### Story Export

#### POST `/api/v1/story/export`

Export generated story to various formats.

**Request:**
```json
{
  "story_id": "abc123",
  "format": "pdf"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| story_id | string | Yes | ID of generated story |
| format | enum | Yes | Export format: `pdf`, `html`, `video`, `social` |

**Response:**
```json
{
  "story_id": "abc123",
  "format": "pdf",
  "status": "processing",
  "download_url": "https://storage.googleapis.com/..."
}
```

**Export Formats:**
- `pdf`: Formatted PDF document
- `html`: Interactive web page
- `video`: Compiled video file
- `social`: Social media posts package

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid story type provided",
    "details": {
      "field": "story_type",
      "allowed_values": ["storybook", "marketing", "educational", "social"]
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_REQUEST | 400 | Request validation failed |
| UNAUTHORIZED | 401 | Authentication required |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| GENERATION_FAILED | 500 | Story generation error |
| SERVICE_UNAVAILABLE | 503 | Gemini API unavailable |

## Rate Limits

- **Story Generation**: 10 requests per minute per IP
- **WebSocket Connections**: 5 concurrent per IP
- **Export Requests**: 20 per minute per IP

Exceeding rate limits returns `429 Too Many Requests`.

## Data Models

### StoryChunk

```typescript
interface StoryChunk {
  story_id: string
  chunk_id: string
  chunk_type: 'text' | 'image' | 'audio' | 'video' | 'metadata'
  content: any
  sequence: number
  is_final: boolean
  timestamp: string
}
```

### MediaContent

```typescript
interface MediaContent {
  type: 'text' | 'image' | 'audio' | 'video' | 'metadata'
  content: any
  metadata?: Record<string, any>
  timestamp?: string
}
```

### StoryPlan

```typescript
interface StoryPlan {
  title: string
  outline: string[]
  scenes: Scene[]
  character_descriptions?: string[]
  visual_style: string
  narrative_arc: {
    setup: string
    conflict: string
    climax: string
    resolution: string
  }
}
```

## Webhooks

Future enhancement: Support for webhooks to notify when story generation completes.

## SDKs

### Python SDK (Example)

```python
import requests

def generate_story(prompt: str):
    response = requests.post(
        "https://your-backend-url.run.app/api/v1/story/generate",
        json={
            "prompt": prompt,
            "story_type": "storybook",
            "length": "medium",
            "include_media": ["text", "images"]
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            print(chunk)
```

### JavaScript SDK (Example)

```javascript
async function generateStory(prompt) {
  const response = await fetch(
    'https://your-backend-url.run.app/api/v1/story/generate',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt,
        story_type: 'storybook',
        length: 'medium',
        include_media: ['text', 'images']
      })
    }
  )

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { value, done } = await reader.read()
    if (done) break

    const chunk = JSON.parse(decoder.decode(value))
    console.log(chunk)
  }
}
```

## Best Practices

1. **Use WebSocket for real-time**: Better for interactive experiences
2. **Handle streaming properly**: Process chunks as they arrive
3. **Implement retry logic**: For transient failures
4. **Respect rate limits**: Implement client-side throttling
5. **Validate requests**: Check parameters before sending
6. **Handle errors gracefully**: Show user-friendly messages

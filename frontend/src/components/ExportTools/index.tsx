'use client'

import { useState } from 'react'
import type { MediaContent } from '@/lib/types'

interface ExportToolsProps {
  storyContent: MediaContent[]
}

export default function ExportTools({ storyContent }: ExportToolsProps) {
  const [isExporting, setIsExporting] = useState(false)
  const [exportFormat, setExportFormat] = useState<'pdf' | 'html' | 'json'>('pdf')

  const handleExport = async () => {
    setIsExporting(true)
    try {
      // TODO: Implement actual export functionality
      console.log('Exporting as', exportFormat, storyContent)
      alert(`Export as ${exportFormat.toUpperCase()} coming soon!`)
    } catch (error) {
      console.error('Export failed:', error)
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <div className="flex items-center space-x-2">
      <select
        value={exportFormat}
        onChange={(e) => setExportFormat(e.target.value as any)}
        className="px-3 py-1 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
        disabled={isExporting}
      >
        <option value="pdf">PDF</option>
        <option value="html">HTML</option>
        <option value="json">JSON</option>
      </select>

      <button
        onClick={handleExport}
        disabled={isExporting}
        className="px-4 py-1 text-sm bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
      >
        {isExporting ? 'Exporting...' : 'Export'}
      </button>
    </div>
  )
}

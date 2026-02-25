/**
 * Copy Injection Agent API
 */

import { api } from '@/api'

export interface TemplateSummary {
  id: string
  name: string
}

export interface CopyInjectionInput {
  template_id: string
  raw_copy: string
  product_name?: string
  product_category?: string
}

export interface PlacementSummary {
  placeholder: string
  content_preview: string
  filled: boolean
}

export interface CopyInjectionOutput {
  html: string
  placeholders_found: string[]
  placements: PlacementSummary[]
  success: boolean
  error_message?: string
}

export interface ExtractPlaceholdersInput {
  html_template: string
}

export interface ExtractPlaceholdersOutput {
  placeholders: string[]
  count: number
}

export const copyInjectionApi = {
  /**
   * Fetch all available templates for the dropdown
   */
  async getTemplates(): Promise<TemplateSummary[]> {
    return api.get<TemplateSummary[]>('/agents/copyinjection/templates')
  },

  /** Fetch the raw CSS string for a template (called once on template select). */
  async getTemplateCss(templateId: string): Promise<string> {
    const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'
    const response = await fetch(`${API_BASE_URL}/agents/copyinjection/templates/${templateId}/css`)
    if (!response.ok) throw new Error(`Failed to fetch CSS for ${templateId}`)
    return response.text()
  },

  /**
   * Extract placeholders from an HTML template (for preview/debugging)
   */
  async extractPlaceholders(input: ExtractPlaceholdersInput): Promise<ExtractPlaceholdersOutput> {
    return api.post<ExtractPlaceholdersOutput>('/agents/copyinjection/extract-placeholders', input)
  },

  /**
   * Process template and copy, returns JSON response with metadata
   */
  async process(input: CopyInjectionInput): Promise<CopyInjectionOutput> {
    return api.post<CopyInjectionOutput>('/agents/copyinjection', input)
  },
}

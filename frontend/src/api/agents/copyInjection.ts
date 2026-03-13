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
  images_generated: number
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


  /**
   * Process template and copy, returns JSON response with metadata
   */
  async process(input: CopyInjectionInput): Promise<CopyInjectionOutput> {
    return api.post<CopyInjectionOutput>('/agents/copyinjection', input)
  },
}

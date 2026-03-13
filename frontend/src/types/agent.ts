export interface AgentField {
  name: string
  label: string
  type: 'textarea' | 'text' | 'select'
  placeholder: string
  options?: { value: string; label: string }[]
}

export interface AgentConfig {
  id: string
  name: string
  description: string
  route: string
  icon: string
  fields: AgentField[]
}

export const agents: AgentConfig[] = [
  {
    id: 'copyinjection',
    name: 'Page Generator',
    description: 'Transform raw marketing copy into complete, beautiful landing pages with AI-generated images.',
    route: '/copyinjection',
    icon: '✨',
    fields: [
      {
        name: 'template',
        label: 'HTML Template',
        type: 'textarea',
        placeholder: 'Paste your HTML template with placeholders...',
      },
      {
        name: 'copy',
        label: 'Marketing Copy',
        type: 'textarea',
        placeholder: 'Paste your raw marketing copy (headline, hook, body, testimonials, CTA)...',
      },
    ],
  },
]

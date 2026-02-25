
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
    name: 'Copy & Image Injection',
    description: 'Generate complete landing pages by filling HTML templates with marketing copy and images.',
    route: '/copyinjection',
    icon: '📝',
    fields: [
      {
        name: 'template',
        label: 'HTML Template',
        type: 'textarea',
        placeholder: 'Paste your HTML template with placeholders...',
      },
      {
        name: 'copy',
        label: 'Advertorial Copy',
        type: 'textarea',
        placeholder: 'Paste your raw advertorial copy (headline, hook, body, testimonials, CTA, legal)...',
      },
    ],
  },
  {
    id: 'translation',
    name: 'Translation & Localisation',
    description: 'Translate landing pages into other languages while keeping HTML structure identical.',
    route: '/translation',
    icon: '🌍',
    fields: [
      {
        name: 'html',
        label: 'HTML Content',
        type: 'textarea',
        placeholder: 'Paste the full HTML of your landing page...',
      },
      {
        name: 'targetLanguage',
        label: 'Target Language',
        type: 'select',
        placeholder: 'Select target language',
        options: [
          { value: 'de', label: 'German' },
          { value: 'fr', label: 'French' },
          { value: 'es', label: 'Spanish' },
          { value: 'it', label: 'Italian' },
          { value: 'nl', label: 'Dutch' },
        ],
      },
    ],
  },
  {
    id: 'compliance',
    name: 'Policy & Compliance',
    description: 'Scan landing pages for ad policy violations and fix only the violating copy.',
    route: '/compliance',
    icon: '✅',
    fields: [
      {
        name: 'html',
        label: 'HTML Content',
        type: 'textarea',
        placeholder: 'Paste the full HTML of your landing page...',
      },
      {
        name: 'policyRules',
        label: 'Policy Instructions',
        type: 'textarea',
        placeholder: 'Enter policy rules (e.g., "Remove medical cure claims", "Avoid guaranteed results", "Remove before/after implications")...',
      },
    ],
  },
  {
    id: 'optimization',
    name: 'Funnel Optimization',
    description: 'Analyze pages for missing conversion elements and add trust, authority, and proof elements.',
    route: '/optimization',
    icon: '📈',
    fields: [
      {
        name: 'html',
        label: 'HTML + CSS Content',
        type: 'textarea',
        placeholder: 'Paste the full HTML + CSS of your landing page...',
      },
      {
        name: 'productType',
        label: 'Product Type',
        type: 'text',
        placeholder: 'e.g., health device, supplement, beauty tool...',
      },
      {
        name: 'market',
        label: 'Target Market',
        type: 'select',
        placeholder: 'Select target market',
        options: [
          { value: 'de', label: 'Germany' },
          { value: 'us', label: 'USA' },
          { value: 'uk', label: 'UK' },
          { value: 'fr', label: 'France' },
        ],
      },
      {
        name: 'trafficSource',
        label: 'Traffic Source',
        type: 'select',
        placeholder: 'Select traffic source',
        options: [
          { value: 'native', label: 'Native Ads' },
          { value: 'social', label: 'Social Media' },
          { value: 'search', label: 'Search' },
        ],
      },
    ],
  },
  {
    id: 'research',
    name: 'Product Research',
    description: 'Guided assistant for discovering winning products from ad libraries and spy tools.',
    route: '/research',
    icon: '🔍',
    fields: [
      {
        name: 'keywords',
        label: 'Keywords',
        type: 'text',
        placeholder: 'e.g., pain relief, posture, sleep, foot pain...',
      },
      {
        name: 'productCategory',
        label: 'Product Category',
        type: 'text',
        placeholder: 'e.g., health devices, supplements, beauty tools...',
      },
      {
        name: 'targetMarkets',
        label: 'Target Markets',
        type: 'text',
        placeholder: 'e.g., Germany, USA, UK...',
      },
      {
        name: 'rawData',
        label: 'Raw Data from Ad Library',
        type: 'textarea',
        placeholder: 'Paste the raw data you copied from Facebook Ad Library or spy tools...',
      },
    ],
  },
]


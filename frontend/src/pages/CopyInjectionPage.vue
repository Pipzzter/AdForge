<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import JSZip from 'jszip'
import { copyInjectionApi, type CopyInjectionOutput, type TemplateSummary } from '@/api'
import { agents } from '@/types/agent'

const agent = agents.find((a) => a.id === 'copyinjection')!

// Templates dropdown
const templates = ref<TemplateSummary[]>([])
const selectedTemplateId = ref('')
const templatesLoading = ref(false)

// CSS cached for the selected template
const templateCss = ref('')

// Form inputs
const rawCopy = ref('')

// State
const isLoading = ref(false)
const error = ref<string | null>(null)

// Results
const result = ref<CopyInjectionOutput | null>(null)

onMounted(async () => {
  templatesLoading.value = true
  try {
    templates.value = await copyInjectionApi.getTemplates()
    if (templates.value.length > 0 && templates.value[0]) {
      selectedTemplateId.value = templates.value[0].id
    }
  } catch {
    error.value = 'Failed to load templates'
  } finally {
    templatesLoading.value = false
  }
})

// Fetch CSS whenever the selected template changes
watch(selectedTemplateId, async (id) => {
  if (!id) return
  try {
    templateCss.value = await copyInjectionApi.getTemplateCss(id)
  } catch {
    templateCss.value = ''
  }
})

async function handleSubmit() {
  if (!selectedTemplateId.value || !rawCopy.value.trim()) {
    error.value = 'Please select a template and paste your advertorial copy'
    return
  }

  isLoading.value = true
  error.value = null
  result.value = null

  try {
    const response = await copyInjectionApi.process({
      template_id: selectedTemplateId.value,
      raw_copy: rawCopy.value,
    })
    result.value = response
    if (!response.success) {
      error.value = response.error_message || 'An error occurred'
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'An error occurred'
  } finally {
    isLoading.value = false
  }
}

function injectCssIntoHtml(html: string, css: string, asLink = false): string {
  if (!css) return html
  const tag = asLink
    ? '<link rel="stylesheet" href="style.css">'
    : `<style>\n${css}\n</style>`
  return html.includes('</head>')
    ? html.replace('</head>', `${tag}\n</head>`)
    : `${tag}\n${html}`
}

function openPreview() {
  if (!result.value?.html) return
  const html = injectCssIntoHtml(result.value.html, templateCss.value)
  const blob = new Blob([html], { type: 'text/html' })
  const url = URL.createObjectURL(blob)
  window.open(url, '_blank')
  setTimeout(() => URL.revokeObjectURL(url), 5000)
}

async function downloadZip() {
  if (!result.value?.html) return
  const html = injectCssIntoHtml(result.value.html, templateCss.value, true)
  const zip = new JSZip()
  zip.file('index.html', html)
  zip.file('style.css', templateCss.value)
  const blob = await zip.generateAsync({ type: 'blob', compression: 'DEFLATE' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `landing-page-${selectedTemplateId.value}.zip`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="bg-slate-900 rounded-xl border border-slate-800 p-8">
    <!-- Header -->
    <div class="flex items-center gap-4 mb-6">
      <span class="text-4xl">{{ agent.icon }}</span>
      <div>
        <h1 class="text-2xl font-bold text-white">{{ agent.name }}</h1>
        <p class="text-slate-400">{{ agent.description }}</p>
      </div>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Template Dropdown -->
      <div>
        <label class="block text-sm font-medium text-slate-300 mb-2">Template</label>
        <select
          v-model="selectedTemplateId"
          :disabled="templatesLoading"
          class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
        >
          <option v-if="templatesLoading" value="">Loading templates...</option>
          <option v-else-if="templates.length === 0" value="">No templates available</option>
          <option v-for="template in templates" :key="template.id" :value="template.id">
            {{ template.name }}
          </option>
        </select>
      </div>

      <!-- Advertorial Copy -->
      <div>
        <label class="block text-sm font-medium text-slate-300 mb-2">Advertorial Copy</label>
        <textarea
          v-model="rawCopy"
          placeholder="Paste your raw advertorial copy (headline, hook, body, testimonials, CTA, legal)..."
          class="w-full h-64 px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <!-- Error Message -->
      <div v-if="error" class="p-4 bg-red-900/50 border border-red-700 rounded-lg text-red-300">
        {{ error }}
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="isLoading || templatesLoading || !selectedTemplateId"
        class="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
      >
        <span v-if="isLoading">Processing...</span>
        <span v-else>Generate Landing Page</span>
      </button>
    </form>

    <!-- Results Section -->
    <div v-if="result" class="mt-8 pt-8 border-t border-slate-700">
      <h2 class="text-xl font-bold text-white mb-4">
        <span v-if="result.success">✅ Generation Complete</span>
        <span v-else>❌ Generation Failed</span>
      </h2>

      <!-- Placeholders Found -->
      <div v-if="result.placeholders_found.length > 0" class="mb-4">
        <h3 class="text-sm font-medium text-slate-400 mb-2">
          Placeholders Found: {{ result.placeholders_found.length }}
        </h3>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="placeholder in result.placeholders_found"
            :key="placeholder"
            class="px-2 py-1 bg-slate-700 rounded text-xs text-slate-300 font-mono"
          >
            {{ placeholder }}
          </span>
        </div>
      </div>

      <!-- Placements Summary -->
      <div v-if="result.placements.length > 0" class="mb-6">
        <h3 class="text-sm font-medium text-slate-400 mb-3">Placements Summary:</h3>
        <div class="space-y-2 max-h-64 overflow-y-auto">
          <div
            v-for="placement in result.placements"
            :key="placement.placeholder"
            class="p-3 bg-slate-800 rounded-lg"
          >
            <div class="flex items-center gap-2 mb-1">
              <span :class="placement.filled ? 'text-green-400' : 'text-red-400'">
                {{ placement.filled ? '✓' : '✗' }}
              </span>
              <span class="font-mono text-sm text-slate-300">{{ placement.placeholder }}</span>
            </div>
            <p class="text-sm text-slate-400 pl-6">{{ placement.content_preview }}</p>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div v-if="result.success" class="flex gap-4">
        <button
          @click="openPreview"
          class="flex-1 px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
        >
          🔍 Preview in New Tab
        </button>
        <button
          @click="downloadZip"
          class="flex-1 px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors"
        >
          ⬇️ Download ZIP
        </button>
      </div>
    </div>
  </div>
</template>


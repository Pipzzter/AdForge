<script setup lang="ts">
import type { AgentField } from '@/types/agent'

defineProps<{
  title: string
  description: string
  icon: string
  fields: AgentField[]
}>()
</script>

<template>
  <div class="bg-slate-900 rounded-xl border border-slate-800 p-8">
    <div class="flex items-center gap-4 mb-6">
      <span class="text-4xl">{{ icon }}</span>
      <div>
        <h1 class="text-2xl font-bold text-white">{{ title }}</h1>
        <p class="text-slate-400">{{ description }}</p>
      </div>
    </div>

    <div class="space-y-4">
      <div v-for="field in fields" :key="field.name">
        <label class="block text-sm font-medium text-slate-300 mb-2">{{ field.label }}</label>

        <textarea
          v-if="field.type === 'textarea'"
          disabled
          :placeholder="field.placeholder"
          class="w-full h-32 px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-400 placeholder-slate-500 resize-none cursor-not-allowed"
        />

        <input
          v-else-if="field.type === 'text'"
          type="text"
          disabled
          :placeholder="field.placeholder"
          class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-400 placeholder-slate-500 cursor-not-allowed"
        />

        <select
          v-else-if="field.type === 'select'"
          disabled
          class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-500 cursor-not-allowed"
        >
          <option value="">{{ field.placeholder }}</option>
          <option v-for="option in field.options" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <button
        disabled
        class="px-6 py-3 bg-slate-700 text-slate-400 rounded-lg cursor-not-allowed"
      >
        Coming Soon
      </button>
    </div>
  </div>
</template>


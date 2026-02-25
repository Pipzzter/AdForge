<script setup lang="ts">
import AgentPlaceholder from '@/components/features/agents/AgentPlaceholder.vue'
import { agents } from '@/types/agent'

const agent = agents.find((a) => a.id === 'research')!
</script>

<template>
  <AgentPlaceholder
    :title="agent.name"
    :description="agent.description"
    :icon="agent.icon"
    :fields="agent.fields"
  />
</template>


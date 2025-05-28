<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold text-center mb-4">USA Scrapes</h1>

    <div v-if="configs.length === 0" class="text-center">Loading USA screener configs...</div>

    <table v-else class="table-auto mx-auto border text-sm">
      <thead>
        <tr class="bg-gray-100">
          <th class="p-2 border">Label</th>
          <th class="p-2 border">Market Cap</th>
          <th class="p-2 border">Active</th>
          <th class="p-2 border">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="config in configs" :key="config.id">
          <td class="p-2 border">{{ config.label }}</td>
          <td class="p-2 border">{{ config.market_cap }}</td>
          <td class="p-2 border">{{ config.is_active ? 'Yes' : 'No' }}</td>
          <td class="p-2 border text-center">
            <button
              class="px-3 py-1 border border-black rounded hover:bg-black hover:text-white transition"
              @click="triggerScrape(config.id)"
            >
              Scrape
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../lib/axios'

const configs = ref([])

const fetchConfigs = async () => {
  const res = await axios.get('/screener-configs')
  configs.value = res.data.filter(c => c.region === 'USA')
}

const triggerScrape = async (configId) => {
  alert(`TODO: Trigger scrape for config ID ${configId}`)
  // Future: axios.post('/scrapes', { config_id: configId })
}

onMounted(fetchConfigs)
</script>

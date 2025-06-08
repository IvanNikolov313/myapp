<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4 text-center">USA Screener Configs</h1>

    <div class="flex flex-col items-center space-y-2 mb-6">
      <input v-model="form.label" placeholder="Label" class="border p-1" />
      <select v-model="form.region" class="border p-1">
        <option value="Canada">Canada</option>
        <option value="USA">USA</option>
      </select>
      <input v-model="form.market_cap" placeholder="Market Cap (e.g. 10M–1B)" class="border p-1" />
      <label class="flex items-center space-x-2">
        <input type="checkbox" v-model="form.is_active" />
        <span>Active</span>
      </label>
      <button @click="submitForm" class="px-4 py-1 bg-white border border-black rounded hover:bg-black hover:text-white transition">
        {{ form.id ? 'Update' : 'Create' }}
      </button>
    </div>

<table class="table-auto border text-sm" style="margin-left: auto; margin-right: auto;">
      <thead>
        <tr class="bg-gray-100">
          <th class="p-2 border">Label</th>
          <th class="p-2 border">Region</th>
          <th class="p-2 border">Market Cap</th>
          <th class="p-2 border">Active</th>
          <th class="p-2 border">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="config in configs" :key="config.id">
          <td class="p-2 border">{{ config.label }}</td>
          <td class="p-2 border">{{ config.region }}</td>
          <td class="p-2 border">{{ config.market_cap }}</td>
          <td class="p-2 border">{{ config.is_active ? 'Yes' : 'No' }}</td>
          <td class="p-2 border">
            <button @click="editConfig(config)" class="text-blue-600 hover:underline mr-2">Edit</button>
            <button @click="deleteConfig(config.id)" class="text-red-600 hover:underline">Delete</button>
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
const form = ref({
  id: null,
  label: '',
  region: 'Canada',
  market_cap: '',
  is_active: true,
})

const fetchConfigs = async () => {
  const response = await axios.get('/screener-configs')
  configs.value = response.data
}

const resetForm = () => {
  form.value = {
    id: null,
    label: '',
    region: 'Canada',
    market_cap: '',
    is_active: true,
  }
}

const submitForm = async () => {
  if (!form.value.label.trim()) {
    alert('Label is required.')
    return
  }

  if (form.value.id) {
    await axios.put(`/screener-configs/${form.value.id}`, form.value)
  } else {
    await axios.post('/screener-configs', form.value)
  }

  resetForm()
  fetchConfigs()
}

const editConfig = (config) => {
  form.value = { ...config }
}

const deleteConfig = async (id) => {
  if (confirm('Are you sure you want to delete this config?')) {
    await axios.delete(`/screener-configs/${id}`)
    fetchConfigs()
  }
}

onMounted(fetchConfigs)
</script>

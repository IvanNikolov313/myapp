<template>
  <div>
    <h2>USA Small & Micro Cap Summary</h2>
    <table>
      <thead>
        <tr>
          <th>Dataset</th>
          <th>Number of Companies</th>
          <th>Number of Employees</th>
          <th>Preview</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="masterData">
          <td>Master Dataset</td>
          <td>{{ masterData.companies }}</td>
          <td>{{ masterData.employees }}</td>
          <td><button disabled>Preview</button></td>
        </tr>
        <tr v-for="scrape in scrapes" :key="scrape.id">
          <td>{{ scrape.name }}</td>
          <td>{{ scrape.total_companies }}</td>
          <td>{{ scrape.total_employees }}</td>
          <td><button disabled>Preview</button></td>
        </tr>
      </tbody>
    </table>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../lib/axios'

const masterData = ref(null)
const scrapes = ref([])

const fetchSummary = async () => {
  try {
    // Fetch master dataset summary (URL matches backend route)
    const masterRes = await axios.get('/usa/master-summary')
    masterData.value = masterRes.data

    // Fetch scrapes summary (URL matches backend route)
    const scrapesRes = await axios.get('/usa/scrapes-summary')
    scrapes.value = scrapesRes.data
  } catch (error) {
    console.error('Failed to fetch summary data:', error)
  }
}

onMounted(() => {
  fetchSummary()
})

</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
  margin-top: 1rem;
}
th, td {
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  text-align: left;
}
button {
  padding: 0.25rem 0.5rem;
  cursor: not-allowed;
  opacity: 0.5;
}
</style>

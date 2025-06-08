<template>
  <div>
    <h2>USA Small & Micro Cap Summary</h2>
    <table>
      <thead>
        <tr>
          <th>Dataset</th>
          <th>Number of Companies</th>
          <th>Companies Scraped & Executives</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="masterData">
          <td>Master Dataset</td>
          <td>{{ masterData.companies }} /</td>
          <td></td>
          <td><button disabled>Preview</button></td>
        </tr>
        <tr v-for="scrape in scrapes" :key="scrape.id">
          <td>
            <strong>Scrape</strong><br />
            {{ formatDate(scrape.created_at) }}
          </td>
          <td>{{ scrape.unique_companies }} / {{ scrape.total_scraped }}</td>
          <td>{{ scrape.companies_scraped }} / {{ scrape.unique_companies }} — {{ scrape.executive_count }} execs</td>
          <td>
            <button @click="scrapeExecutives(scrape.id)">Scrape Executives</button>
            <button @click="downloadCompanyCSV(scrape.id)">Companies CSV</button>
            <button @click="downloadExecCSV(scrape.id)">Executives CSV</button>
            <button @click="deleteScrape(scrape.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../lib/axios'

const backendBase = 'http://localhost:8000'

const masterData = ref(null)
const scrapes = ref([])

const fetchSummary = async () => {
  try {
    const masterRes = await axios.get('/usa/master-summary')
    masterData.value = masterRes.data

    const scrapesRes = await axios.get('/usa/scrapes-summary')
    scrapes.value = scrapesRes.data
  } catch (error) {
    console.error('Failed to fetch summary data:', error)
  }
}

const formatDate = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleString()
}

const scrapeExecutives = async (scrapeId) => {
  try {
    const response = await axios.post(`/executives/scrape/${scrapeId}`)
    alert(response.data.message || 'Scraping started.')
    fetchSummary()
  } catch (error) {
    console.error('Failed to start scraping executives:', error)
    alert(error.response?.data?.detail || 'Failed to start scraping executives.')
  }
}

const downloadCompanyCSV = (scrapeId) => {
  window.open(`${backendBase}/api/scrapes/${scrapeId}/export-companies`, '_blank')
}

const downloadExecCSV = (scrapeId) => {
  window.open(`${backendBase}/api/scrapes/${scrapeId}/export-executives`, '_blank')
}

const deleteScrape = async (scrapeId) => {
  if (!confirm('Are you sure you want to delete this scrape?')) return
  try {
    await axios.delete(`/scrapes/${scrapeId}`)
    fetchSummary()
  } catch (error) {
    console.error('Failed to delete scrape:', error)
    alert('Failed to delete scrape.')
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
  vertical-align: top;
}
button {
  margin: 0.25rem 0.25rem 0 0;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  opacity: 1;
}
button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>

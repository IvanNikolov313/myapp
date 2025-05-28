<template>
  <div class="p-4 relative">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">Admin Menu</h2>
      <button @click="logout" class="text-sm text-red-600 hover:underline">Logout</button>
    </div>

    <nav class="space-x-4 mb-6">
  <router-link to="/admin/dashboard" class="text-blue-600 hover:underline">📊 Dashboard</router-link>
  <router-link to="/admin/settings" class="text-blue-600 hover:underline">⚙️ Settings</router-link>
  <router-link to="/admin/usa-dashboard">USA Dashboard</router-link>
  <router-link to="/admin/usa-screener-configs">USA Screener Configs</router-link>
  <router-link to="/admin/usa-scrapes">USA Scrapes</router-link>
</nav>


    <router-view />
  </div>
</template>
<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('token') // clear the stored auth token
  router.push('/login')            // redirect to login page
}
</script>

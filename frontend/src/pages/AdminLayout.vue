<template>

  <div class="flex" style="height: 100vh">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 text-white p-4 flex flex-col">
      <h2 class="text-xl font-bold mb-6">Admin Menu</h2>
      <nav class="space-y-4">
        <router-link to="/admin/dashboard" class="block hover:underline">📊 Dashboard</router-link>
        <router-link to="/admin/settings" class="block hover:underline">⚙️ Settings</router-link>
      </nav>
    </aside>

    <!-- Main content -->
    <main class="flex-1 p-8 bg-gray-100 overflow-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

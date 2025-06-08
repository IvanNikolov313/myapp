<template>
  <div style="min-height: 100vh; background: white; color: #111;">
    <!-- Full-width Navigation Bar -->
    <nav style="width: 100vw; padding: 12px 24px; border-bottom: 1px solid #ddd; box-shadow: 0 1px 2px rgba(0,0,0,0.05); position: relative; z-index: 10;">
      <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; width: 100%;">
        <!-- Left: Menu -->
        <ul style="display: flex; flex-wrap: wrap; gap: 24px; list-style: none; margin: 0; padding: 0;">
          <li>
            <router-link to="/admin/dashboard" style="text-decoration: none; color: #333;" @mouseover="hover($event)" @mouseleave="unhover($event)">Dashboard</router-link>
          </li>

          <!-- USA Dropdown -->
          <li style="position: relative;">
            <span style="cursor: pointer; color: #333;" @mouseover="showUSA = true" @mouseleave="showUSA = false">
              USA ▾
              <ul v-show="showUSA" style="position: absolute; top: 100%; left: 0; background: white; border: 1px solid #ddd; padding: 8px 0; margin: 0; width: 180px; list-style: none;">
                <li>
                  <router-link to="/admin/usa-dashboard" style="display: block; padding: 6px 16px; text-decoration: none; color: #333;" @mouseover="hover($event)" @mouseleave="unhover($event)">Overview</router-link>
                </li>
                <li>
                  <router-link to="/admin/usa-scrapes" style="display: block; padding: 6px 16px; text-decoration: none; color: #333;" @mouseover="hover($event)" @mouseleave="unhover($event)">Scrape</router-link>
                </li>
              </ul>
            </span>
          </li>

          <!-- Canada Dropdown -->
          <li style="position: relative;">
            <span style="cursor: pointer; color: #333;" @mouseover="showCanada = true" @mouseleave="showCanada = false">
              Canada ▾
              <ul v-show="showCanada" style="position: absolute; top: 100%; left: 0; background: white; border: 1px solid #ddd; padding: 8px 0; margin: 0; width: 180px; list-style: none;">
                <li>
                  <span style="display: block; padding: 6px 16px; color: #aaa;">Coming soon...</span>
                </li>
              </ul>
            </span>
          </li>

          <!-- Configs -->
          <li>
            <router-link to="/admin/usa-screener-configs" style="text-decoration: none; color: #333;" @mouseover="hover($event)" @mouseleave="unhover($event)">Yahoo Screener Configs</router-link>
          </li>

          <!-- Settings -->
          <li>
            <router-link to="/admin/settings" style="text-decoration: none; color: #333;" @mouseover="hover($event)" @mouseleave="unhover($event)">Settings</router-link>
          </li>
        </ul>

        <!-- Logout Button -->
        <button @click="logout" style="color: #e00; font-size: 14px; text-decoration: underline; background: none; border: none; cursor: pointer;">
          Logout
        </button>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main style="padding: 24px; max-width: 1200px; margin: 0 auto;">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showUSA = ref(false)
const showCanada = ref(false)

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const hover = (e) => {
  e.target.style.color = '#1d4ed8'
}
const unhover = (e) => {
  e.target.style.color = '#333'
}
</script>

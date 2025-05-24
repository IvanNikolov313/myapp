<template>
  <form @submit.prevent="handleLogin" class="login-form">
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Password" required />
    <button type="submit">Login</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </form>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import axios from 'axios'

const emits = defineEmits(['login-success'])

const email = ref('admin@example.com')   // default correct email for easy testing
const password = ref('adminpass')        // default correct password for easy testing
const errorMessage = ref('')

async function handleLogin() {
  try {
    const response = await axios.post('http://localhost:8000/login', new URLSearchParams({
      username: email.value,
      password: password.value
    }))
    const token = response.data.access_token
    localStorage.setItem('token', token)
    errorMessage.value = ''
    emits('login-success')  // Emit event to parent that login succeeded
  } catch (error) {
    console.error("Login error:", error.response || error)  // Detailed error log
    errorMessage.value = 'Login failed. Check your credentials.'
  }
}
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.error {
  color: red;
}
</style>

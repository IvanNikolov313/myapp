<template>
  <div>
    <LoginForm v-if="!isLoggedIn" @login-success="handleLoginSuccess" />
    <MainContent v-else />
  </div>
</template>

<script>
import LoginForm from './components/LoginForm.vue'
import MainContent from './components/MainContent.vue'

export default {
  components: { LoginForm, MainContent },
  data() {
    return {
      isLoggedIn: false,
    }
  },
  methods: {
    handleLoginSuccess() {
      this.isLoggedIn = true
    },
  },
}
</script>

<template>
  <login></login>
</template>

<script>
import Login from '@/components/containers/Login'

export default {
  components: {
    Login,
  },
  fetch({ store, redirect }) {
    const authToken = store.getters['authentication/authToken']
    if (authToken) {
      redirect('/languages')
    }
  },
  head() {
    return {
      title: 'ログイン',
    }
  },
}
</script>

<template>
  <user-creation-form></user-creation-form>
</template>

<script>
import UserCreationForm from '../components/containers/UserCreationForm.vue'

export default {
  components: {
    UserCreationForm
  },
  fetch({ store, redirect }) {
    const authToken = store.getters['authentication/authToken']
    if (authToken) {
      redirect('/languages')
    }
  },
}
</script>

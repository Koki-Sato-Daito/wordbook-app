<template>
  <div>
    <div class="d-flex justify-content-center mb-3">
      <b-spinner label="Loading..."></b-spinner>
    </div>
  </div>
</template>

<script>
export default {
  fetch({ store, redirect }) {;
      store.dispatch('authentication/logout')
      .then(() => {
        store.commit('authentication/deleteAuthData')
        redirect('/')
      })
  },
  head() {
    return {
      title: "ログアウト"
    }
  }
}
</script>
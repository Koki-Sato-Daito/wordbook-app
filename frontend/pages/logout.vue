<template>
  <div>
    <p>ログアウトしました。リダイレクトします。</p>
  </div>
</template>

<script>
export default {
  fetch({ store, redirect }) {
    const authToken =  store.getters['authentication/authToken'];
    if (authToken) {
      store.dispatch('authentication/logout').then(() => {
        store.commit('authentication/deleteAuthData')
      })
    }
    redirect('/');
  },
}
</script>
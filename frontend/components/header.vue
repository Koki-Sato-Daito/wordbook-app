<template>
  <header id="header">
    <b-navbar toggleable="md" type="dark" variant="dark" class="px-3 py-3">
      <b-navbar-toggle target="nav-text-collapse"></b-navbar-toggle>

      <b-navbar-brand
        ><a class="link-button" href="">app_name</a></b-navbar-brand
      >

      <b-collapse id="nav-text-collapse" is-nav>
        <b-navbar-nav>
          <div v-if="authToken">
            <b-nav-text class="mx-3">{{ username }} さん</b-nav-text>
            <b-nav-text
              ><i class="link-button"
                ><nuxt-link to="/logout">ログアウト</nuxt-link></i
              ></b-nav-text
            >
          </div>
          <div v-else>
            <b-nav-text class="mx-3"
              ><a class="link-button" href="">サインアップ</a></b-nav-text
            >
            <b-nav-text
              ><i class="link-button"
                ><nuxt-link to="/login">ログイン</nuxt-link></i
              ></b-nav-text
            >
          </div>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </header>
</template>
<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState({
      authToken: (state) => state.authentication.authToken,
      userId: (state) => state.authentication.userData.id,
      username: (state) => state.authentication.userData.username,
      email: (state) => state.authentication.userData.email,
    }),
  }
}
</script>
<style>
</style>

<template>
  <header id="header">
    <b-navbar toggleable="md" type="dark" variant="dark" class="px-3 py-3">
      <b-navbar-toggle target="nav-text-collapse"></b-navbar-toggle>

      <b-navbar-brand
        ><a class="link-button" href="">{{ appname }}</a></b-navbar-brand
      >

      <b-collapse id="nav-text-collapse" is-nav>
        <b-navbar-nav>
          <div v-if="authtoken">
            <b-nav-text class="mx-3">{{ username }} さん</b-nav-text>
            <b-nav-text
              ><i class="link-button"
                ><nuxt-link to="/logout">ログアウト</nuxt-link></i
              ></b-nav-text
            >
          </div>
          <div v-else>
            <b-nav-text class="mx-3"
              ><i class="link-button"
                ><nuxt-link to="/signup">サインアップ</nuxt-link></i
              ></b-nav-text
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
export default {
  props: {
    appname: {
      type: String,
      required: true,
      default: 'アプリ名',
    },
    authtoken: {
      type: null,
      required: true,
      default: '',
    },
    userid: {
      type: String,
      required: true,
      default: '',
    },
    username: {
      type: String,
      required: true,
      default: '名無し',
    },
    email: {
      type: String,
      required: true,
      default: '',
    },
  },
}
</script>
<style>
</style>

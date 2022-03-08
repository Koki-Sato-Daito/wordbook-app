<template>
  <b-row class="justify-content-center">
    <b-col lg="9">
      <b-form class="login-form" @submit.prevent="onSubmit">
        <h2>ログイン用紙</h2>
        <br />
        <b-form-group label="メールアドレス:" label-for="email">
          <b-form-input
            id="email"
            v-model="localEmail"
            type="email"
            placeholder="メールアドレスを入力してください。"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group label="パスワード:" label-for="password">
          <b-form-input
            id="password"
            v-model="localPassword"
            type="password"
            placeholder="パスワードを入力してください。"
            required
          ></b-form-input>
        </b-form-group>

        <b-button type="submit" squared variant="primary">提出</b-button>
        <b-button
          type="submit"
          squared
          variant="success"
          @click.prevent="guestLogin"
          >ゲストアカウントでログインする</b-button
        >
      </b-form>
    </b-col>
  </b-row>
</template>

<script>
export default {
  props: {
    email: {
      type: String,
      required: true,
    },
    password: {
      type: String,
      required: true,
    },
  },
  computed: {
    localEmail: {
      get() {
        return this.email
      },
      set(val) {
        this.$emit('update:email', val)
      },
    },
    localPassword: {
      get() {
        return this.password
      },
      set(val) {
        this.$emit('update:password', val)
      },
    },
  },
  methods: {
    onSubmit(event) {
      this.$emit('login', event)
    },
    guestLogin(event) {
      this.$emit('guest-login', event)
    }
  },
}
</script>

<style scoped>
.login-form {
  background: linear-gradient(#dfdfdf 1px, transparent 1px) #fffbf2;
  background-size: auto 2em;
  padding: 64px;
  min-height: 100vh;
}
</style>
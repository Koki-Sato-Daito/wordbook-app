<template>
  <div class="container">
    <b-form @submit.prevent="onSubmit" class="signup-form">
      <h2>ユーザ登録用紙</h2>
      <br>
      <b-form-group label="ユーザ名:" label-for="username">
        <b-form-input
          id="username"
          v-model="localUsername"
          type="text"
          placeholder="ユーザ名を入力してください。"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group label="メールアドレス:" label-for="email">
        <b-form-input
          id="email"
          v-model="localEmail"
          type="email"
          placeholder="メールアドレスを入力してください。"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group label="パスワード:" label-for="password1">
        <b-form-input
          id="password1"
          v-model="localPassword1"
          type="password"
          placeholder="パスワードを入力してください。"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group label="パスワード(確認用):" label-for="password2">
        <b-form-input
          id="password2"
          v-model="localPassword2"
          type="password"
          placeholder="もう一度パスワードを入力してください"
          required
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" squared variant="success">サインアップ</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  props: {
    username: {
        type: String,
        required: true
    },
    email: {
      type: String,
      required: true,
    },
    password1: {
      type: String,
      required: true,
    },
    password2: {
      type: String,
      required: true,
    },
  },
  computed: {
    localUsername: {
      get() {
        return this.username
      },
      set(val) {
        this.$emit('update:username', val)
      },
    },
    localEmail: {
      get() {
        return this.email
      },
      set(val) {
        this.$emit('update:email', val)
      },
    },
    localPassword1: {
      get() {
        return this.password1
      },
      set(val) {
        this.$emit('update:password1', val)
      },
    },
    localPassword2: {
      get() {
        return this.password2
      },
      set(val) {
        this.$emit('update:password2', val)
      },
    },
  },
  methods: {
    onSubmit(event) {
      this.$emit('submit', event);
    }
  }
}
</script>

<style scoped>
.signup-form {
    background: linear-gradient(#dfdfdf 1px, transparent 1px) #fffbf2;
    background-size: auto 2em;
    padding: 64px;
    min-height:120vh;
}
</style>
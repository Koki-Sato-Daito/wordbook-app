<template>
  <div class="container mt-5 p-5">
    <b-form @submit="onSubmit">

      <div v-if="errors.length != 0">
        <div class="alert alert-danger" role="alert">
          <div v-for="error in errors" :key="error">
            <i class="error">{{ error }}</i><br>
          </div>
        </div>
      </div>

      <b-form-group
        id="input-group-1"
        label="メールアドレス:"
        label-for="input-1"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="メールアドレスを入力してください。"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="パスワード:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.password"
          type="password"
          placeholder="パスワードを入力してください。"
          required
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">ログイン</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errors: [],
    }
  },
  fetch({ store, redirect }) {
    const authToken = store.getters['authentication/authToken'];
    if (authToken) {
      redirect('/languages');
    }
  },
  methods: {
    onSubmit(event) {
      event.preventDefault()
      this.$store
        .dispatch('authentication/login', {
          email: this.form.email,
          password: this.form.password,
        })
        .catch((error) => {
          this.errors = error.response.data.non_field_errors
          this.form.password = ''
        })
        .then((response) => {
          this.$store.commit('authentication/setAuthData', response.data);
          this.$router.push('/languages');
        })
    },
  },
}
</script>
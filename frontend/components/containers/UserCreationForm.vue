<template>
  <div>
    <br />
    <api-error :errors="errors"></api-error>

    <user-creation-form
      :username.sync="form.username"
      :email.sync="form.email"
      :password1.sync="form.password1"
      :password2.sync="form.password2"
      @submit.prevent.stop="signUp"
    ></user-creation-form>
  </div>
</template>

<script>
import UserCreationForm from '@/components/presentationals/UserCreationForm'
import ApiError from '@/components/containers/ApiError'

export default {
  components: {
    ApiError,
    UserCreationForm,
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password1: '',
        password2: '',
      },
      errors: {},
    }
  },
  methods: {
    signUp(event) {
      event.preventDefault()
      if (this.form.password1 !== this.form.password2) {
        alert('password が一致しません。')
        this.form.password1 = ''
        this.form.password2 = ''
        return null
      }
      const body = {
        username: this.form.username,
        email: this.form.email,
        password: this.form.password1,
      }
      this.$axios
        .post('/api/v1/auth/users/', JSON.stringify(body))
        .then((response) => {
          this.$store
            .dispatch('authentication/login', {
              email: this.form.email,
              password: this.form.password1,
            })
            .then((response) => {
              this.$store.commit('authentication/setAuthData', response.data)
              this.$router.push('/languages')
            })
            .catch((error) => {
              for (const property in error.response.data) {
                this.$set(this.errors, property, error.response.data[property])
              }
              this.form.password = ''
            })
        })
        .catch((error) => {
          for (const property in error.response.data) {
            this.$set(this.errors, property, error.response.data[property])
          }
          this.form.email = ''
          this.form.password = ''
        })
    },
  },
}
</script>
<template>
<div>
  <br>
  <api-error
     :errors="errors"
  ></api-error>

  <login
    :email.sync="form.email"
    :password.sync="form.password"
    @login="login"
    @guest-login="guestLogin"
  ></login>
</div>
</template>

<script>
import Login from '@/components/presentationals/Login'
import ApiError from '@/components/containers/ApiError'

export default {
  components: {
    Login,
    ApiError
  },
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errors: {}
    }
  },
  methods: {
    login(event) {
      event.preventDefault()
      this.$store
        .dispatch('authentication/login', {
          email: this.form.email,
          password: this.form.password,
        })
        .then((response) => {
          this.$store.commit('authentication/setAuthData', response.data)
          this.$router.push('/languages')
        })
        .catch((error) => {
          for (const property in error.response.data){
              this.$set(this.errors, property, error.response.data[property])
          }
          this.form.password = ''
        })
    },
    guestLogin(event) {
      event.preventDefault()
      this.$axios.post('/api/v1/auth/guest_login/')
      .then((response) => {
        this.$store.commit('authentication/setAuthData', response.data)
        this.$router.push('/languages')
      })
    }
  },
}
</script>

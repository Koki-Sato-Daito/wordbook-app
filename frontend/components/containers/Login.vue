<template>
<div>
  <br>
  <api-error
     :errors-array="errors"
  ></api-error>

  <login
    :email.sync="form.email"
    :password.sync="form.password"
    @login.prevent.stop="login"
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
      errors: []
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
        .catch((error) => {
          this.errors = error.response.data.non_field_errors
          this.form.password = ''
        })
        .then((response) => {
          this.$store.commit('authentication/setAuthData', response.data)
          this.$router.push('/languages')
        })
    },
  },
}
</script>

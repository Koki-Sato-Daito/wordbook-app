<template>
  <presentational-header
    appname="ITエンジニアの英単語"
    :authtoken="authToken"
    :userid="userData.id"
    :username="userData.username"
    :email="userData.email"
  ></presentational-header>
</template>
  
<script>
import { mapGetters } from 'vuex'
import presentationalHeader from '@/components/presentationals/Header'

export default {
  components: {
    presentationalHeader,
  },
  computed: {
    ...mapGetters({
      authToken: 'authentication/authToken',
      userData: 'authentication/userData'
    }),
  },
}
</script>

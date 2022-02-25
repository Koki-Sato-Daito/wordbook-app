import createPersistedState from 'vuex-persistedstate'
import authentication from '~/store/authentication'

export default ({ store }) => {
  window.onNuxtReady(() => {
    createPersistedState({
      modules: {
        authentication
      },
      key: 'wordbook',
      paths: [
        'authentication.authToken',
        'authentication.userData'
      ]
    })(store)
  })
}
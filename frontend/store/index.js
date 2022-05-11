const actions = {
    nuxtClientInit({ commit }, context) {
        const keys = JSON.parse(localStorage.getItem("wordbook"));
        const payload = {}
        payload.auth_token = keys.authentication.authToken;
        
        payload.user = {}
        payload.user.id = keys.authentication.userData.id;
        payload.user.username  = keys.authentication.userData.username;
        payload.user.email = keys.authentication.userData.email;
        commit('authentication/setAuthData', payload);
      }
}

export default {
    namespaced: true,
    actions
}
const actions = {
    nuxtClientInit({ commit }, context) {
        try{
            const keys = JSON.parse(localStorage.getItem("wordbook"));
            const payload = {}
            payload.authToken = keys.authentication.authToken;
            
            payload.user = {}
            payload.user.id = keys.authentication.userData.id;
            payload.user.username  = keys.authentication.userData.username;
            payload.user.email = keys.authentication.userData.email;
            commit('authentication/setAuthData', payload);
        }catch(error) {
            console.log(error);
        }
      }
}

export default {
    namespaced: true,
    actions
}
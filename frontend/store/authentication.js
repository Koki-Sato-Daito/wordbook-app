const state = () => ({
    userData: {
        id: '',
        username: '',
        email: '',
    },
    authToken: '',
})

// getters
const getters = {
    userData: (state, getters) => {
        return state.userData;
    },

    authToken: (state, getters) => {
        return state.authToken || null;
    }
}

// actions
const actions = {
    login({ commit, state }, payload) {
        return  this.$axios.post('api/v1/auth/token/login/', {
                email: payload.email,
                password: payload.password
            })
    },

    logout({ commit, state }) {
        return this.$axios.post('api/v1/auth/token/logout/', {},
            { headers: { "Authorization": "Token " + state.authToken } })
    }
}

// mutations
const mutations = {
    setAuthData(state, payload) {
        state.authToken = payload.auth_token;
        state.userData.id = payload.user.id;
        state.userData.username = payload.user.username;
        state.userData.email = payload.user.email;
    },
    deleteAuthData(state) {
        state.authToken = '';
        state.userData = {};
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
}
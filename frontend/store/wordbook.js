const state = () => ({
    words: [],
    MistakeWords: [],
    progressData: []
})

// getters
const getters = {
    progressData: (state, getters) => {
        return state.processData;
    },
}

// actions
const actions = {
    fetchWords({state, commit}, payload) {
        const params = {
            language: payload.language,
            pos: payload.pos,
        }
        if (payload.userId) {
            params.users = payload.userId;
        }
        console.log(params)
        return  this.$axios.get('api/v1/words/', {
            params,
            headers: {
                "Authorization": "Token " + payload.authToken
            }
        })
    }

    // saveMistakeWords関数を実装
        // axiosで /api/v1/users/id/words/にstate.mistakeWordsをpost
        // state.mistakeWordsを空にする
}

// mutations
const mutations = {
    setWords(state, words) {
        state.words = words
    },
    // setMistakeWords関数を実装
        // state.mistakeWordsに値を入れる
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
}
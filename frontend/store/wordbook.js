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
        return  this.$axios.get('api/v1/words/', {
            params: {
                language: payload.language,
                pos: payload.pos
            },
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
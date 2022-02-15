const state = () => ({
    wordbookMeta: {
        language: '',
        pos: ''
    },
    items: [
        {
            id: 1,
            name: 'Python',
            language: 'python',
            pos: {
                '名詞': 'noun',
                '動詞': 'verb',
                '形容詞': 'adjective',
                '副詞': 'adverb'
            },
            imgUrl: '/images/python-logo.png',
            officialUrl: 'https://www.python.org/',
        }
    ]
})

// getters
const getters = {
    wordbookMeta: (state, getters) => {
        return state.wordbookMeta;
    },
    items: (state, getters) => {
        return state.items;
    },
    itemsLength: (state, getters) => {
        return state.items.length;
    },
}

// actions
const actions = {
    setWordbookMeta({ state, commit }, { id, pos }) {
        const item = state.items.find(item => item.id === parseInt(id));
        commit('pushLanguage', {item})
        commit('pushPos', {item, pos})
    }
}

// mutations
const mutations = {
    pushLanguage(state, {item}) {
        state.wordbookMeta.language = item.language;
    },
    pushPos(state, {item, pos}) {
        state.wordbookMeta.pos = String(pos);
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
}
const state = () => ({
    items: [
        {
            id: 1,
            name: 'お試し厳選10問',
            language: 'trial',
            pos: {
                '問題': 'any',
            },
            imgUrl: '/images/trial.png',
            officialUrl: '',
        },
        {
            id: 2,
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
        },
        {
            id: 3,
            name: 'Java',
            language: 'java',
            pos: {
                '名詞': 'noun',
                '動詞': 'verb',
                '形容詞': 'adjective',
                '副詞': 'adverb'
            },
            imgUrl: '/images/java-logo-icon.png',
            officialUrl: 'https://www.oracle.com/en/java/',
        }
    ]
})

// getters
const getters = {
    items: (state, getters) => {
        return state.items;
    },
}

// actions
const actions = {}

// mutations
const mutations = {}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
}
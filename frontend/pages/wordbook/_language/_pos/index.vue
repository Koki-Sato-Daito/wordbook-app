<template>
  <containers-wordbook
    :words="words"
    :word-index="wordIndex"
    @increment-word-index="incrementWordIndex"
    @check-answer="storeUpMistakeWords"
    @finish="finish"
    @stop-studying="saveProgress"
  ></containers-wordbook>
</template>

<script>
import ContainersWordbook from '@/components/containers/Wordbook'

export default {
  components: {
    ContainersWordbook,
  },
  data() {
    return {
      language: this.$route.params.language,
      pos: this.$route.params.pos,

      user: this.$store.getters['authentication/userData'],
      authToken: this.$store.getters['authentication/authToken'],

      wordIndex: 0,
      words: [],
      mistakenWords: [],
    }
  },
  created() {
    // get用のクエリパラメータを用意
    const q = {
      language: this.language,
      pos: this.pos,
      user: this.user.id,
    }
    this.$axios
      .get('api/v1/init_wordbook_page/', {
        params: q,
        headers: {
          Authorization: 'Token ' + this.authToken,
        },
      })
      .then((response) => {
        this.words = response.data.words
        if (response.data.progress) {
          this.wordIndex = response.data.progress.index
          this.deleteProgress(response.data.progress.id)
        }
      })
  },
  methods: {
    incrementWordIndex() {
      this.wordIndex++
    },
    storeUpMistakeWords(localIndex, isCorrect) {
      if (!isCorrect) {
        this.mistakenWords.push(this.words[localIndex].id)
      }
    },
    finish() {
      this.saveMistakenWords()
      this.wordIndex=0
    },
    saveMistakenWords() {
      const data = {
        mistakes: this.mistakenWords,
      }
      this.$axios
        .post(`/api/v1/users/${this.user.id}/mistake/`, JSON.stringify(data), {
          headers: {
            Authorization: 'Token ' + this.authToken,
          },
        })
        .then(() => {
          this.mistakenWords.splice(0, this.mistakenWords.length)
        })
    },
    saveProgress() {
      this.saveMistakenWords()
      const data = {
        language: this.language,
        pos: this.pos,
        mistake: false,
        user: this.user.id,
        index: this.wordIndex,
      }
      this.$axios.post('/api/v1/progress/', data, {
        headers: {
          Authorization: 'Token ' + this.authToken,
        },
      })
    },
    deleteProgress(progressId) {
      this.$axios.delete(`/api/v1/progress/${progressId}/`, {
        headers: {
          Authorization: 'Token ' + this.authToken,
        },
      })
    },
  },
}
</script>

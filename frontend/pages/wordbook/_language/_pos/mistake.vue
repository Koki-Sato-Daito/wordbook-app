<template>
  <containers-wordbook
    :before-fetch="beforeFetch"
    :word-index="wordIndex"
    :words="words"
    @increment-word-index="incrementWordIndex"
    @check-answer="storeUpCorrectWords"
    @finish="finish"
    @stop-studying="stopStudying"
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

      beforeFetch: true,
      wordIndex: 0,
      words: [],
      correctWords: [],
    }
  },
  head() {
    return {
      title: "復習ページ"
    }
  },
  created() {
    const q = {
      language: this.language,
      pos: this.pos,
      user: this.user.id,
      mistake: true
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
        this.beforeFetch=false
      })
  },
  methods: {
    incrementWordIndex() {
      this.wordIndex++
    },
    storeUpCorrectWords(localIndex, isCorrect) {
      if (isCorrect) {
        this.correctWords.push(this.words[localIndex].id)
      }
    },
    stopStudying() {
      this.saveCorrectWords()
    },
    finish() {
      this.saveCorrectWords()
      alert('お疲れ様です！すべての問題が解き終わりました！！')
      this.$router.push('/languages')
    },
    saveCorrectWords() {
      const data = {
        mistakes: this.correctWords,
      }
      this.$axios
        .patch(`/api/v1/users/${this.user.id}/mistake/`, JSON.stringify(data), {
          headers: {
            Authorization: 'Token ' + this.authToken,
          },
        })
        .then(() => {
          this.correctWords.splice(0, this.correctWords.length)
        })
    },
  }
}

</script>
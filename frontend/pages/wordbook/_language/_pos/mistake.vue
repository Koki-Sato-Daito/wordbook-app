<template>
  <containers-wordbook
    :words="words"
    @check-answer="storeUpCorrectWords"
    @finish="finish"
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

      words: [],
      correctWords: [],
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
      })
  },
  methods: {
    storeUpCorrectWords(localIndex, isCorrect) {
      if (isCorrect) {
        this.correctWords.push(this.words[localIndex].id)
      }
    },
    finish() {
      this.saveCorrectWords()
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
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
      mistake: true
    }
    this.$axios
      .get('api/v1/exam_page_data/', {
        params: q,
        headers: {
          Authorization: 'Token ' + this.authToken,
        },
      })
      .then((response) => {
        this.words = response.data.words
        this.beforeFetch=false
      })
      .catch(() => {
        this.$router.push("/");
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
        correctWords: this.correctWords,
      }
      this.$axios
        .post(`/api/v1/correct_words/`, JSON.stringify(data), {
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
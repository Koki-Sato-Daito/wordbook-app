<template>
  <div>
    <containers-wordbook
      :before-fetch="beforeFetch"
      :words="words"
      :word-index="wordIndex"
      @increment-word-index="incrementWordIndex"
      @check-answer="checkAnswer"
      @finish="finish"
      @stop-studying="saveProgress"
    ></containers-wordbook>

    <b-modal id="finish-modal" centered modal-cancell title="結果発表">
      <div class="text-center py-4">
        <div v-if="score >= 60">
          <h1 class="result">合格</h1>
        </div>
        <div v-else>
          <h1 class="result">不合格</h1>
        </div>
        <br>
        <p>正答率は</p>
        <h3 class="score">{{ score }} %</h3>
        <p>{{ words.length }}問中 {{ correctAnswerCounter }}問正解でした。</p>
      </div>
      <template #modal-footer="">
        <b-button size="sm" variant="success" @click="confirmResult"> 確認しました </b-button>
      </template>
    </b-modal>
  </div>
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
      mistakenWords: [],
      correctAnswerCounter: 0,
    }
  },
  computed: {
    score() {
      return Math.round((this.correctAnswerCounter / this.words.length) * 100)
    },
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
          this.correctAnswerCounter =
            response.data.progress.correctAnswerCounter
          this.deleteProgress(response.data.progress.id)
        }
        this.beforeFetch=false
      })
  },
  methods: {
    incrementWordIndex() {
      this.wordIndex++
    },
    checkAnswer(localIndex, isCorrect) {
      if (isCorrect) {
        this.correctAnswerCounter++
      } else {
        this.mistakenWords.push(this.words[localIndex].id)
      }
    },
    finish() {
      this.saveMistakenWords()
      this.wordIndex = 0
      this.$bvModal.show('finish-modal')
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
      this.incrementWordIndex()
      const data = {
        language: this.language,
        pos: this.pos,
        mistake: false,
        user: this.user.id,
        index: this.wordIndex,
        correctAnswerCounter: this.correctAnswerCounter,
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
    confirmResult() {
      this.$router.push('/languages')
    }
  },
}
</script>

<style>
.result {
  font-weight: bold;
  font-size: 2rem;
}
</style>
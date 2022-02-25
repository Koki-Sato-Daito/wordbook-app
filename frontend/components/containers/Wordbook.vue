<template>
  <presentational-wordbook
    :word-index="wordIndex"
    :words="words"
    :is-correct.sync="isCorrect"
    @move-onto-next-word="moveOntoNextWord"
  ></presentational-wordbook>
</template>

<script>
import PresentationalWordbook from '@/components/presentationals/Wordbook'

export default {
  components: {
    PresentationalWordbook,
  },
  props: {
    words: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      isCorrect: false,
      wordIndex: 0
    }
  },
  methods: {
    moveOntoNextWord() {
      this.$emit('check-answer', this.wordIndex, this.isCorrect);
      this.isCorrect = false
      this.wordIndex++
      if (this.wordIndex >= this.words.length) {
        this.wordIndex=0
        this.finish()
      }
    },
    finish() {
      this.$emit('finish')
      alert('お疲れ様です！すべての問題が解き終わりました！！')
      this.$router.push('/languages')
    },
  },
}
</script>
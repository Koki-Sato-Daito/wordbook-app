<template>
  <presentational-wordbook
    :word-index="wordIndex"
    :words="words"
    :is-correct.sync="isCorrect"
    @correct="correct"
    @incorrect="incorrect"
    @move-onto-next-word="moveOntoNextWord"
    @stop-studying="stopStudying"
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
    wordIndex: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      isCorrect: false,
    }
  },
  methods: {
    incrementWordIndex() {
      this.$emit('increment-word-index')
    },
    correct() {
      this.isCorrect=true
      this.moveOntoNextWord()
    },
    incorrect() {
      this.isCorrect=false
      this.moveOntoNextWord()
    },
    moveOntoNextWord() {
      this.$emit('check-answer', this.wordIndex, this.isCorrect);
      this.isCorrect = false
      this.incrementWordIndex()
      if (this.wordIndex === this.words.length-1) {
        this.finish()
      }
    },
    finish() {
      this.$emit('finish')
    },
    stopStudying() {
      this.$emit('check-answer', this.wordIndex, this.isCorrect);
      this.$emit('stop-studying')
      this.$router.push('/languages')
    }
  },
}
</script>
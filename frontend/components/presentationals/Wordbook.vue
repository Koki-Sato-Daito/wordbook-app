<template>
  <div id="wordbook">
    <br />
    <div class="wordcard">
      <div v-if="beforeFetch" class="text-center mt-5 pt-5">
        <div class="spinner-border text-light"></div>
      </div>
      <div v-else-if="words.length && wordIndex < words.length" class="text-center py-5 mb-5">
        <div>{{ wordIndex+1 }}/{{ words.length }}</div>
        <div class="mt-3 mb-5">
          <span>出現回数: {{ words[wordIndex]['freq'] }}</span>
        </div>
        <h2>{{ words[wordIndex]['wordname'] }}</h2>
        <div v-if="isRevealed">
          <h3 class="answer">{{ words[wordIndex]['meaning'] }}</h3>
          <div class="mt-5">
            <b-button class="mr-4" variant="outline-light" @click.prevent.stop="stopStudying">セーブ</b-button>   
            <b-button variant="outline-light" @click.prevent.stop="incorrect">不正解</b-button>
            <b-button variant="light" @click.prevent.stop="correct">正解</b-button>
          </div>
        </div>
        <div v-else>
          <b-button variant="outline-light" @click="toggleIsRevealed"
            >答えを見る</b-button
          >
        </div>
      </div>
      <div v-else class="text-center pt-5">
        問題が見つかりませんでした。
        <nuxt-link class="black-borad-link" to="/languages">戻る</nuxt-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    beforeFetch: {
      type: Boolean,
      required: true
    },
    wordIndex: {
      type: Number,
      required: true,
    },
    words: {
      type: Array,
      required: true,
    },
    isCorrect: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      isRevealed: false,
    }
  },
  computed: {
    localCorrect: {
      get() {
        return this.isCorrect
      },
      set() {
        this.$emit('update:is-correct', !this.isCorrect)
      },
    },
  },
  methods: {
    toggleIsRevealed() {
      this.isRevealed = !this.isRevealed
    },
    correct() {
      this.toggleIsRevealed()
      this.$emit('correct')
    },
    incorrect() {
      this.toggleIsRevealed()
      this.$emit('incorrect')
    },
    stopStudying() {
      this.$emit("stop-studying")
    }
  },
}
</script>


<style>
.wordcard {
  background-image: url('/images/black-board.png');
  background-repeat: no-repeat;
  background-size: cover;
  height: 90vh;
  box-sizing: border-box;
  border: 4mm ridge hsl(36, 100%, 50%);
  color: aliceblue;
}

.answer {
  color: hsl(351, 100%, 75%);
}

.black-borad-link {
  color: white;
}
.black-borad-link:hover {
  color: white;
  opacity: 0.7;
}
</style>
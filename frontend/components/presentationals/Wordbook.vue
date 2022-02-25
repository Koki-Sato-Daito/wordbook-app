<template>
  <div id="wordbook">
    <br />
    <div class="wordcard">
      <div v-if="words.length && wordIndex < words.length" class="text-center py-5 mb-5">
        <div>{{ wordIndex+1 }}/{{ words.length }}</div>
        <div class="mt-3 mb-5">
          <span>出現回数: {{ words[wordIndex]['freq'] }}</span>
        </div>
        <h2>{{ words[wordIndex]['wordname'] }}</h2>
        <div v-if="isRevealed">
          <h1 class="answer">{{ words[wordIndex]['meaning'] }}</h1>
          <div class="mt-5">
            <b-form-checkbox v-model="localCorrect"> 正解</b-form-checkbox>
            <br />
            <b-button variant="outline-light" @click.prevent.stop="stopStudying">進捗を保存して戻る</b-button>
            <b-button variant="outline-light" @click.prevent.stop="moveOntoNextWord"
              >次の単語へ</b-button
            >
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
    moveOntoNextWord() {
      this.toggleIsRevealed()
      this.$emit('move-onto-next-word')
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
  height: 70vh;
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
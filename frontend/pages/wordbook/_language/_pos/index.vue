<template>
  <div id="wordbook">
    <br />
    <div class="wordcard">
      <div v-if="words.length" class="text-center py-5 mb-5">
        <div class="mt-3 mb-5">
          <span>出現回数: {{ words[index]['freq'] }}</span>
        </div>
        <h2>{{ words[index]['wordname'] }}</h2>
        <div v-if="isRevealed">
          <h1 class="answer">{{ words[index]['meaning'] }}</h1>
          <div class="mt-5">
            <b-form-checkbox v-model="correct"> 正解</b-form-checkbox>
            <br />
            <b-button variant="outline-light" @click="saveProgress"
              >進捗を保存して戻る</b-button
            >
            <b-button variant="outline-light" @click="moveOntoNextWord"
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
  data() {
    return {
      language: this.$route.params.language,
      pos: this.$route.params.pos,
      index: 0,
      isRevealed: false,
      correct: false,
      mistakenWords: [],
    }
  },

  fetch({ store, params, redirect }) {
    const language = params.language;
    const pos = params.pos;
    const authToken = store.getters['authentication/authToken'];
    if (!authToken) {
      redirect('/login');
    }
    store
      .dispatch('wordbook/fetchWords', { language, pos, authToken })
      .then((response) => {
        if (response.data.length) {
          store.commit('wordbook/setWords', response.data);
        }else{
          store.commit('wordbook/setWords', []);
        }
      })
  },

  // mounted(){
  //     const vm = this;

  //     const progress = localStorage.getItem(vm.getStorageKey);
  //     if (progress){
  //         vm.index = progress
  //         localStorage.removeItem(vm.getStorageKey)
  //     }
  // },

  computed: {
    words() {
      return this.$store.state.wordbook.words;
    },
    //     getMistakeParam: function(){
    //         const mistakeParam = "{{ mistake }}";
    //         if (mistakeParam == "True"){
    //             return true
    //         }
    //         return false
    //     },
    //     getStorageKey: function(){
    //         if (this.getMistakeParam){
    //             return 'progress-{{ language }}-{{ pos }}-mistake'
    //         }else{
    //             return 'progress-{{ language }}-{{ pos }}'
    //         }
    //     },
  },
  methods: {
    // 出力系
    toggleIsRevealed() {
      this.isRevealed = !this.isRevealed
    },
    moveOntoNextWord() {
      if (!this.correct) {
        this.addMistakenWord()
      }
      this.toggleIsRevealed()
      this.correct = false
      this.index++
      if (this.index >= this.words.length) {
        this.saveMistakenWords()
        this.index = 0
        alert('お疲れ様です！すべての問題が解き終わりました！！')
        this.$router.push('/languages');
      }
    },

    // 間違えた問題の処理
    addMistakenWord() {
      this.mistakenWords.push(this.words[this.index].id);
    },
    saveMistakenWords() {
      const user = this.$store.getters['authentication/userData'];
      const data = {
        "mistakes": this.mistakenWords 
      }
      this.$axios.post(`/api/v1/users/${user.id}/mistake/`, 
        JSON.stringify(data), 
        {
           headers: { "Authorization": "Token " + this.$store.getters['authentication/authToken'] }
        }).then(() => {
          this.mistakenWords.splice(0, this.mistakenWords.length);
        })
    }
    //     saveProgress: function() {
    //         localStorage.removeItem(this.getStorageKey);
    //         localStorage.setItem(this.getStorageKey, this.index);
    //         this.postMistakenWords();
    //         window.location.href = "{% url 'languages' %}";
    //     },
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
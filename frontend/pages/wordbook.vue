<template>
  <div id="wordbook">
    <p class="mt-3 mb-5">language / pos</p>
    <div class="wordcard">
      <div v-if="true" class="text-center py-5 mb-5">
        <div class="mt-3 mb-5">
          <span>出現回数: 1</span>
        </div>
        <h2>study</h2>
        <div v-if="isRevealed">
          <h1 class="answer">勉強する</h1>
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
        問題が見つかりませんでした。<a
          class="black-borad-link"
          href="{% url 'languages' %}"
          >戻る</a
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      words: [],
      index: 0,
      isRevealed: false,
      correct: false,
      mistakenWords: [],
    }
  },
  // mounted(){
  //     const vm = this;

  //     const progress = localStorage.getItem(vm.getStorageKey);
  //     if (progress){
  //         vm.index = progress
  //         localStorage.removeItem(vm.getStorageKey)
  //     }

  //     const fetchUrl = this.getFetchUrl;
  //     axios.get(fetchUrl).then(function(response) {
  //         vm.words = response.data.data
  //         vm.words.splice()
  //     }).catch(function(e){
  //         console.log(e)
  //     })
  // },
  // computed: {
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
  //     getFetchUrl: function() {
  //         if (this.getMistakeParam){
  //             return "{% url 'vocabulary_data' language pos %}?mistake=True"
  //         }else{
  //             return "{% url 'vocabulary_data' language pos %}"
  //         }
  //     }
  // },
  // methods: {
  //     toggleIsRevealed: function() {
  //         this.isRevealed = !this.isRevealed
  //     },
  //     resetCorrect: function() {
  //         this.correct = false
  //     },
  //     moveOntoNextWord: function(){
  //         if (!this.correct){
  //             this.saveMistakenWords();
  //         }
  //         this.toggleIsRevealed();
  //         this.resetCorrect();
  //         this.index++;
  //         if (this.index >= this.words.length){
  //             this.postMistakenWords();
  //             alert('終了！');
  //             window.location.href = "{% url 'languages' %}";
  //         }
  //     },
  //     saveProgress: function() {
  //         localStorage.removeItem(this.getStorageKey);
  //         localStorage.setItem(this.getStorageKey, this.index);
  //         this.postMistakenWords();
  //         window.location.href = "{% url 'languages' %}";
  //     },
  //     saveMistakenWords: function() {
  //         this.mistakenWords.push(this.words[this.index].id);
  //     },
  // postMistakenWords: function() {
  //     const vm = this
  //     const postUrl = "{% url 'mistake' %}";
  //     const data = JSON.stringify({'words': vm.mistakenWords});
  //     axios.defaults.xsrfCookieName = 'csrftoken';
  //     axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  //     axios.post(postUrl, data).then(function(response) {
  //         console.log(response)
  //     }).catch(function(e){
  //         console.log(e)
  //     })
  // }
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
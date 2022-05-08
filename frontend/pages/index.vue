<template>
    <b-row class="justify-content-center">
      <b-col id="top" lg="9">
      <div class="title-box">
          <h5 class="fw-bold">☆ITエンジニア編☆</h5>
          <h1 class="text-center fw-bold title-text">英語</h1>
      </div>
      <div class="mt-4">
          <p class="text-center fw-bold">受験の際の注意</p>
          <ul class="explain-text-box">
              <li class="mb-3">
                  本試験は各種プログラミング言語の公式ドキュメントで出現した単語を独自に集計したものを出題しています。
              </li>
              <li class="mb-3">
                  間違えた問題は後に復習することができます。試験の後もご活用ください。
              </li>
              <li class="mb-3">
                  英語が苦手な方はもちろん、
                  得意な方もどんな英単語が頻出するのかという点で楽しんでもらえるとうれしいです。
              </li>
          </ul>
          <b-button class="my-3" variant="outline-danger" to="/login">学習を始める</b-button>
      </div>
    <br>
      <p>現在、
          <ul>
              <li>Python</li>
              <li>Java</li>
          </ul>
          以上の言語に対応しております。</p>
  </b-col>
    </b-row>
</template>

<script>
export default {
  head() {
    return {
      title: "トップページ"
    }
  }
}
</script>


<style>
#top {
  background: linear-gradient(#dfdfdf 1px, transparent 1px) #fffbf2;
  background-size: auto 2em;
  margin-top: 50px;
  padding: 64px;
  min-height: 130vh;
}

.title-box {
  padding: 40px;
}
.title-text {
  font-size: 6rem;
}

.explain-text-box {
  border: 3px solid black;
  padding: 40px;
  list-style-type: square;
  font-size: 1.1rem;
}
</style>




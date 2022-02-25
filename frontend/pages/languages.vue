<template>
  <div id="language" class="pt-5">
    <h4>学習する言語と品詞を選択してください</h4>
    <div class="row">
      <select-language v-for="item in items" :key="item.id" :item="item" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SelectLanguage from '~/components/containers/SelectLanguage'

export default {
  components: {
    SelectLanguage,
  },
  computed: {
    ...mapGetters({ items: 'wordbookMeta/items' }),
  },
}
</script>

<style>
.card {
  border: 0.5px solid black;
  background: linear-gradient(#dfdfdf 1px, transparent 1px) #fffbf2;
  background-size: auto 2em;
}
</style>
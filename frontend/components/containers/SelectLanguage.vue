<template>
  <presentational-select-language
    :item="item"
    @moveToWordbookPage="moveToWordbookPage"
  ></presentational-select-language>
</template>

<script>
import PresentationalSelectLanguage from '@/components/presentationals/SelectLanguage'

export default {
  components: {
    PresentationalSelectLanguage,
  },
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  methods: {
    moveToWordbookPage(pos, mistake) {
      let url = `wordbook/${this.item.language}/${pos}/`
      url += mistake ? "mistake=true" : ""
      this.$router.push(url)
    },
  },
}
</script>

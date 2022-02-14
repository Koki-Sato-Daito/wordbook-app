<template>
  <div class="col-lg-6">
    <b-card
      :img-src="item.imgUrl"
      img-alt="Image"
      img-top
      tag="article"
      class="my-3 py-4 card"
      :title="item.name"
    >
      <div v-for="(value, key) in item.pos" :key="key">
        <b-button
          variant="link"
          @click.stop.prevent="wordbookPage(item.id, value)"
        >
          {{ key }}
        </b-button>
        <b-button
          variant="link"
          @click.prevent="wordbookPageWithMistake(item.id, value)"
        >
          間違った{{ key }}
        </b-button>
      </div>
      <b-card-text class="mt-5"
        ><a :href="item.officialUrl">公式ページリンク</a></b-card-text
      >
    </b-card>
  </div>
</template>

<script>
export default {
  props: {
    item: Object,
  },
  methods: {
    wordbookPage(id, pos) {
      this.$store.dispatch('wordbookMeta/setWordbookMeta', { id, pos })
    },
    wordbookPageWithMistake(id, pos) {
      // mistake用のフラグを作る
      this.$store.dispatch('wordbookMeta/setWordbookMeta', { id, pos })
    },
  },
}
</script>

<style>
.card {
  max-width: 30rem;
}
</style>
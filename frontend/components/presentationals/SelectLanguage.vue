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
        <b-button variant="link" @click.prevent="clickLink(value, false)">
          {{ key }}
        </b-button>
        <b-button variant="link" @click.prevent="clickLink(value, true)">
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
    item: {
      type: Object,
      required: true,
    },
  },
  methods: {
      clickLink(pos, mistake) {
          this.$emit('moveToWordbookPage', pos, mistake)
      }
  }
}
</script>

<style>
.card {
  max-width: 30rem;
}
</style>
<template>
  <b-col lg="4" md="5" sm="6">
    <b-container class="mb-5">
      <b-row class="justify-content-center">
        <b-card
          :img-src="item.imgUrl"
          img-alt="Image"
          img-top
          tag="article"
          class="my-3"
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
          <br />
        </b-card>
      </b-row>
    </b-container>
  </b-col>
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
    },
  },
}
</script>

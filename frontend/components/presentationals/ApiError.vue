<template>
  <div v-if="Object.keys(errors).length">
    <div class="alert alert-danger" role="alert">
      <div v-for="error in errors" :key="error">
        <div v-for="message in error" :key="message">
          <i class="error">{{ message }}</i
          ><br />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    errors: {
      type: Object,
      required: true
    },
  },
}
</script>

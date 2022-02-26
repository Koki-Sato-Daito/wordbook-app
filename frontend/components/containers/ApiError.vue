<template>
  <container-api-error
     :errors="errors"></container-api-error>
</template>

<script>
import ContainerApiError from '@/components/presentationals/ApiError'

export default {
  components: {
    ContainerApiError,
  },
  props: {
    errors: {
      type: Object,
      required: true
    },
  },
}
</script>
  
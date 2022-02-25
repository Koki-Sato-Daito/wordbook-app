<template>
  <container-api-error
     :errors-array="errorsArray"></container-api-error>
</template>

<script>
import ContainerApiError from '@/components/presentationals/ApiError'

export default {
  components: {
    ContainerApiError,
  },
  props: {
    errorsArray: {
      type: Array,
      required: true
    },
  },
}
</script>
  
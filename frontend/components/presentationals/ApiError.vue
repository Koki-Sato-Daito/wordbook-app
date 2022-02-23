<template>
    <div v-if="errorsArray.length">
        <div class="alert alert-danger" role="alert">
          <div v-for="error in errorsArray" :key="error">
            <i class="error">{{ error }}</i
            ><br />
          </div>
        </div>
      </div>
</template>

<script>
export default {
    props: {
        errorsArray: {
            type: Array,
            required: true,
        }
    }
}
</script>

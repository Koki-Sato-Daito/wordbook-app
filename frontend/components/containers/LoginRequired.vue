<script>
export default {
  fetch({ store, redirect }) {
    const authToken =  store.getters['authentication/authToken'];
    if (!authToken) {
      redirect('/');
    }
  },
}
</script>

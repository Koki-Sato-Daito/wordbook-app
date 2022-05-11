<template>
    <div>
        <p>リダイレクトします。</p>
    </div>
</template>

<script>
export default {
    created() {
        this.$router.push('/');
    }
}
</script>
<template>
    <body>
        <main>
            <Header />
            <b-container>
                <nuxt />
            </b-container>
        </main>
    </body>
</template>

<script>
    import Header from "@/components/containers/Header.vue";
    export default {
		components: {
			Header
		}
	};
</script>

<style>
body {
    background-image: url('/images/wood-texture.jpg');
    background-repeat: no-repeat;
    background-size: cover;
    min-height:100vh;
    padding-bottom: 50px;
    font-family: "M Plus 1p";
}

.link-button {
    text-decoration: none;
    color: white;
}

.link-button:hover {
    opacity: 0.7;
    color: white;
}
</style>
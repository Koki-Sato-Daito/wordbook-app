<template>
    <body>
        <main>
            <Header />
            <div class='container'>
                <nuxt />
            </div>
        </main>
    </body>
</template>

<script>
    import Header from "@/components/header.vue";
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
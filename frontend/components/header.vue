<template>
    <header id="header">
        <b-navbar toggleable="md" type="dark" variant="dark" class="px-3 py-3">
            <b-navbar-toggle target="nav-text-collapse"></b-navbar-toggle>

            <b-navbar-brand><a class="link-button" href="">app_name</a></b-navbar-brand>

            <b-collapse id="nav-text-collapse" is-nav>
            <b-navbar-nav>
                <!-- {% if user.is_authenticated %} -->
                    <b-nav-text class='mx-3'>username さん</b-nav-text>
                    <b-nav-text><a class="link-button" href="">ログアウト</a></b-nav-text>
                <!-- {% else %} -->
                    <b-nav-text class='mx-3'><a class="link-button" href="">サインアップ</a></b-nav-text>
                    <b-nav-text><a class="link-button" href="">ログイン</a></b-nav-text>
                <!-- {% endif %} -->
            </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </header>
</template>
<script>

</script>
<style>

</style>

<template>
    <v-app id="inspire">
        <app-nav :drawer="drawer"/>
        <v-app-bar
                app
                color="indigo"
                dark
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>Сетка Вещания Cinegy</v-toolbar-title>
        </v-app-bar>
        <v-content>
            <router-view/>
        </v-content>
        <AppFooter/>
    </v-app>
</template>

<script>
    import AppNav from './components/AppNav'
    import AppFooter from './components/AppFooter'

    export default {
        components: {
            AppNav,
            AppFooter
        },
        data: () => ({
            drawer: true
        }),

        created() {
            document.title = "Сетка Вещания Cinegy";
        }
    }
</script>
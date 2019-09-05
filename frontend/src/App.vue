<template>
    <v-app id="inspire">
        <app-nav :drawer="drawer"/>
        <v-app-bar
                app
                color="indigo"
                dark
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>{{APP_TITLE}}</v-toolbar-title>
        </v-app-bar>
        <v-content>
            <v-slide-y-transition mode="out-in">
                <router-view/>
            </v-slide-y-transition>
        </v-content>
        <AppFooter/>
    </v-app>
</template>

<script>
    import AppNav from './components/AppNav'
    import AppFooter from './components/AppFooter'

    import {mapGetters} from 'vuex'

    export default {
        components: {
            AppNav,
            AppFooter
        },
        data: () => ({
            drawer: true,

        }),
        computed: {
            ...mapGetters(['APP_TITLE'])
        },
        created() {
            document.title = 'Cinegy Log Parser';
        }
    }
</script>
<template>
    <v-navigation-drawer
            v-model="drawer"
            app
    >
        <v-list dense>
            <v-list-item v-for="route in routes" @click="$router.push(route.path)">
                <v-list-item-action>
                    <v-icon>{{route.icon}}</v-icon>
                </v-list-item-action>
                <v-list-item-content>
                    <v-list-item-title>{{route.name}}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>

        </v-list>
    </v-navigation-drawer>
</template>

<script>
    export default {
        name: "AppNav",
        props: ['drawer',],
        computed: {
            routes: function () {
                //Last one is default route
                return this.$router.options.routes.slice(0, -1)
            }
        }
    }
</script>

<style scoped>

</style>
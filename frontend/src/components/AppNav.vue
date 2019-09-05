<template>

    <v-navigation-drawer app v-model="drawer">
        <v-list
                dense
                nav
        >
            <v-list-item
                    v-for="route in routes" :to="route.path"
                    link
            >
                <v-list-item-icon>
                    <v-icon>{{ route.icon }}</v-icon>
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title>{{ route.name }}</v-list-item-title>
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
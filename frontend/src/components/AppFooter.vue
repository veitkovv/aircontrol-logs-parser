<template>
    <v-footer color="indigo white--text" app>
        <v-spacer></v-spacer>
        <v-layout align-center>
            <a class="subheading white--text" href="mailto:it@yamal-region.tv">Задавайте вопросы по электронной почте</a>
        </v-layout>
        <span class="mr-4">ver. 1.1</span>
        <div>&copy; {{ new Date().getFullYear() }} by Veytko V.V.</div>
    </v-footer>
</template>

<script>
    export default {
        name: "AppFooter"
    }
</script>


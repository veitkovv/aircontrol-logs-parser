<template>
    <v-container fluid>
        <p class="display-2">Создание эфирной справки по логам Cinegy</p>
        <p>Приложение сканирует логи Cinegy, и создает отчеты на основании заданных параметров поиска</p>
        <p>В целях оптипизации производительности создано ограничение в 5000 роликов на один запрос, поэтому выбирайте
            не
            очень широкий диапазон дат в поиске</p>
        <p>Приложение сканирует логи каждое утро в 6:15, сканирование продолжается около 5 минут, в это время данные
            могут
            быть недоступны</p>
    </v-container>
</template>

<script>
    import {mapMutations} from 'vuex'

    export default {
        name: "About",
        methods: {
            ...mapMutations([
                'SET_TITLE',
            ]),
        },
        beforeMount() {
            this.SET_TITLE('О приложении')
        }
    }
</script>

<style scoped>

</style>
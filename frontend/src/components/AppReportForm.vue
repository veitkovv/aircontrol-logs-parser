<template>
    <v-container fluid>
        <v-row justify="center" align="start">
            <v-col cols="10">
                <v-row><span>Отчет по роликам за период:</span></v-row>
                <v-row justify="start">
                    <v-col cols="12" lg="3">
                        <v-menu
                                ref="dateStartMenu"
                                v-model="dateStartMenu"
                                :close-on-content-click="false"
                                transition="scale-transition"
                                offset-y
                                full-width
                                max-width="290px"
                                min-width="290px"
                        >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                        v-model="dateStartFormatted"
                                        label="Дата начала"
                                        persistent-hint
                                        prepend-icon="event"
                                        @blur="dateStart = parseDate(dateStartFormatted)"
                                        v-on="on"
                                        :rules="dateStartRules"
                                ></v-text-field>
                            </template>
                            <v-date-picker
                                    v-model="dateStart"
                                    no-title
                                    @input="dateStartMenu = false"
                                    locale="ru-ru"
                                    first-day-of-week="1"
                            ></v-date-picker>
                        </v-menu>
                    </v-col>
                    <v-col cols="11" sm="3" lg="3">
                        <v-menu
                                ref="timeStartMenu"
                                v-model="timeStartMenu"
                                :close-on-content-click="false"
                                :nudge-right="40"
                                :return-value.sync="timeStart"
                                transition="scale-transition"
                                offset-y
                                full-width
                                max-width="290px"
                                min-width="290px"
                        >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                        v-model="timeStart"
                                        label="Время начала"
                                        prepend-icon="access_time"
                                        readonly
                                        v-on="on"
                                ></v-text-field>
                            </template>
                            <v-time-picker
                                    v-if="timeStartMenu"
                                    v-model="timeStart"
                                    full-width
                                    format="24hr"
                                    @click:minute="$refs.timeStartMenu.save(timeStart)"
                            ></v-time-picker>
                        </v-menu>
                    </v-col>
                    <v-col cols="12" lg="3">
                        <v-menu
                                ref="dateEndMenu"
                                v-model="dateEndMenu"
                                :close-on-content-click="false"
                                transition="scale-transition"
                                offset-y
                                full-width
                                max-width="290px"
                                min-width="290px"
                        >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                        v-model="dateEndFormatted"
                                        label="Дата окончания"
                                        persistent-hint
                                        prepend-icon="event"
                                        @blur="dateEnd = parseDate(dateEndFormatted)"
                                        v-on="on"
                                        :rules="dateEndRules"
                                ></v-text-field>
                            </template>
                            <v-date-picker
                                    v-model="dateEnd"
                                    no-title
                                    @input="dateEndMenu = false"
                                    locale="ru-ru"
                                    first-day-of-week="1"
                            ></v-date-picker>
                        </v-menu>
                    </v-col>
                    <v-col cols="11" sm="3" lg="3">
                        <v-menu
                                ref="timeEndMenu"
                                v-model="timeEndMenu"
                                :close-on-content-click="false"
                                :nudge-right="40"
                                :return-value.sync="timeEnd"
                                transition="scale-transition"
                                offset-y
                                full-width
                                max-width="290px"
                                min-width="290px"
                        >
                            <template v-slot:activator="{ on }">
                                <v-text-field
                                        v-model="timeEnd"
                                        label="Время окончания"
                                        prepend-icon="access_time"
                                        readonly
                                        v-on="on"
                                ></v-text-field>
                            </template>
                            <v-time-picker
                                    v-if="timeEndMenu"
                                    v-model="timeEnd"
                                    format="24hr"
                                    full-width
                                    @click:minute="$refs.timeEndMenu.save(timeEnd)"
                            ></v-time-picker>
                        </v-menu>
                    </v-col>
                </v-row>
                <v-row>
                    <v-autocomplete
                            v-model="chips"
                            :disabled="isUpdating"
                            :items="eventsDateFiltered"
                            chips
                            color="blue-grey lighten-2"
                            label="Выберите ролик(и)"
                            item-text="name"
                            item-value="name"
                            multiple
                            @update:search-input="itemChanged"
                    >
                        <template v-slot:selection="data">
                            <v-chip
                                    v-bind="data.attrs"
                                    :input-value="data.selected"
                                    close
                                    @click="data.select"
                                    @click:close="remove(data.item)"
                            >
                                {{ data.item.name }}
                            </v-chip>
                        </template>
                        <template v-slot:item="data">
                            <template v-if="typeof data.item !== 'object'">
                                <v-list-item-content v-text="data.item"></v-list-item-content>
                            </template>
                            <template v-else>
                                <v-list-item-content>
                                    <v-list-item-title v-html="data.item.name"></v-list-item-title>
                                    <v-list-item-subtitle>
                                        <span>Время выхода в эфир: {{dateTimeHumanFormat(data.item.start)}}</span>
                                        <p>Длительность {{data.item.duration}} секунд</p>
                                    </v-list-item-subtitle>
                                </v-list-item-content>
                            </template>
                        </template>
                    </v-autocomplete>
                </v-row>
                <v-row>
                    <v-col cols="12" sm="6">
                        <v-text-field
                                v-model="reportFor"
                                label="Для кого справка"
                                outlined
                                clear-icon="mdi-close-circle"
                                clearable
                                @click:clear="clearReportFor"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                        <v-text-field
                                v-model="signedBy"
                                label="Кем будет подписана"
                                outlined
                                clear-icon="mdi-close-circle"
                                clearable
                                @click:clear="clearSignedBy"
                        ></v-text-field>
                    </v-col>
                    <v-col>
                        <v-text-field
                                v-model="createdBy"
                                label="Исполнитель"
                                outlined
                                clear-icon="mdi-close-circle"
                                clearable
                                @click:clear="clearCreatedBy"
                        ></v-text-field>
                    </v-col>

                </v-row>
                <v-row justify="center" v-if="eventsList.length !==0" ref="content" id="content">
                    <v-col cols="12" lg="12" id="document-to-export">
                        <p class="header">{{reportFor}}</p>
                        <span>Эфирная справка о материалах, прошедших в эфире телеканала</span>
                        <span> ОГТРК «Ямал-Регион»</span>
                        <p>(период размещения: c {{dateStart}} {{timeStart}} по {{dateEnd}} {{timeEnd}})</p>
                        <v-simple-table
                                dense
                                fixed-header
                        >
                            <thead>
                            <tr>
                                <th>Время выхода в эфир</th>
                                <th>Имя ролика</th>
                                <th>Хронометраж (сек.)</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="(item, index) in eventsList" v-bind:key="item.id">
                                <td>{{dateTimeHumanFormat(item.start)}}</td>
                                <td>{{item.name}}</td>
                                <td>{{item.duration}}</td>
                            </tr>
                            </tbody>
                        </v-simple-table>
                        <hr>
                        <div class="summary">
                            <span>Всего роликов: {{eventsList.length}}.</span>
                            <p>Общий хронометраж: {{totalDuration}} секунд. </p>
                        </div>
                        <p class="footer">{{signedBy}} ______________________</p>
                        <p class="contact">{{createdBy}}</p>
                    </v-col>
                    <v-col>
                        <v-btn
                                outlined
                                large
                                block
                                color="success"
                                @click="makePdf"
                        >Скачать документ
                        </v-btn>
                    </v-col>
                </v-row>
            </v-col>
        </v-row>
        <v-overlay :value="loading">
            <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>
    </v-container>
</template>

<script>
    import {mapActions, mapGetters} from 'vuex'

    export default {
        name: "AppReportForm",
        data() {
            return {
                loading: false,
                isUpdating: false,
                itemSearch: null,
                chips: [],
                dateStartMenu: false,
                dateStart: new Date().toISOString().substr(0, 10),
                dateStartFormatted: this.formatDate(new Date().toISOString().substr(0, 10)),
                dateStartRules: [
                    v => new Date(v) < new Date() || "Эфиры за эту дату еще не наступили"
                ],
                timeStartMenu: false,
                timeStart: '00:00',
                dateEndMenu: false,
                dateEnd: new Date().toISOString().substr(0, 10),
                dateEndFormatted: this.formatDate(new Date().toISOString().substr(0, 10)),
                dateEndRules: [
                    v => new Date(v) >= new Date(this.dateStart) || "Дата окончания должна быть больше даты начала",
                    v => new Date(v) < new Date() || "Эфиры за эту дату еще не наступили"
                ],
                timeEndMenu: false,
                timeEnd: '23:59',
                reportFor: 'ИП Осколков И.Н.',
                signedBy: 'Начальник программной дирекции О.А. Криберг',
                createdBy: 'Исп. Пузина Диана Эдуардовна 7-12-46',
                eventsList: [],
                eventsDateFiltered: []
            }
        },

        computed: {
            ...mapGetters([
                'EVENTS',
            ]),
            startAfter() {
                return this.dateStartFormatted + ' ' + this.timeStart
            },
            startBefore() {
                return this.dateEndFormatted + ' ' + this.timeEnd
            },
            totalDuration() {
                return Math.round(this.eventsList.reduce(function (prev, cur) {
                    return prev + parseFloat(cur.duration);
                }, 0))
            }
        },

        methods: {
            ...mapActions([
                'fetchEvents',
            ]),
            async fetchReportData() {
                // https://fetch.spec.whatwg.org/#fetch-api
                let url = new URL("http://api.localhost/rolls/?start_after=" + this.startAfter + "&start_before=" + this.startBefore)

                this.loading = true
                // для реактивной строки поиска - фильтр только по датам
                await fetch(url.href)
                    .then(response => response.json())
                    .then(data => {
                        this.eventsDateFiltered = data.results
                    })

                if (this.itemSearch !== null) {
                    url.searchParams.append('name__icontains', this.itemSearch)
                    await fetch(url.href)
                        .then(response => response.json())
                        .then(data => {
                            this.eventsList = data.results
                        })
                } else {
                    url.searchParams.append('name_in', this.chips.join('|'))
                    await fetch(url.href)
                        .then(response => response.json())
                        .then(data => {
                            this.eventsList = data.results
                        })
                }
                this.loading = false
            },
            formatDate(date) {
                if (!date) return null

                const [year, month, day] = date.split('-')
                return `${year}-${month}-${day}`
            },
            parseDate(date) {
                if (!date) return null

                const [year, month, day] = date.split('-')
                return `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
            },
            clearReportFor() {
                this.reportFor = ''
            },
            clearSignedBy() {
                this.signedBy = ''
            },
            clearCreatedBy() {
                this.createdBy = ''
            },
            itemChanged(item) {
                if (item !== null) {
                    this.fetchEvents(item)
                }
            },
            remove(item) {
                this.chips.splice(this.chips.indexOf(item), 1)
                this.chips = [...this.chips]
            },
            dateTimeHumanFormat(datetime) {
                let moment = require('moment');
                return moment(datetime).format("YYYY-MM-DD HH:mm:ss")
            },
            makePdf() {
                let vm = this
                let pdfMake = require('pdfmake/build/pdfmake.js')
                if (pdfMake.vfs === undefined) {
                    var pdfFonts = require('pdfmake/build/vfs_fonts.js')
                    pdfMake.vfs = pdfFonts.pdfMake.vfs;
                }

                let rows = this.eventsList.map(event => ([
                        this.dateTimeHumanFormat(event.start),
                        event.name,
                        event.duration]
                ));
                rows.unshift(['Время выхода', 'Название ролика', 'Хронометраж (сек.)'])

                let docDefinition = {
                    header: function (currentPage, pageCount, pageSize) {
                        if (currentPage === 1) {
                            return [
                                {
                                    text: vm.reportFor,
                                    style: 'contact',
                                    alignment: 'right'
                                }
                            ]
                        }
                    },
                    content: [
                        {
                            text: 'Эфирная справка о материалах, прошедших в эфире телеканала',
                            style: 'subheader',
                            alignment: 'center'
                        },
                        {
                            text: 'ОГТРК «Ямал-Регион»',
                            style: 'subheader',
                            alignment: 'center'
                        },
                        {
                            text: 'период размещения: c ' + this.dateStart + ' ' + this.timeStart + ' по ' + this.dateEnd + ' ' + this.timeEnd,
                            style: 'subheader',
                            alignment: 'center'
                        },
                        {
                            style: 'tableExample',
                            table: {
                                widths: ['auto', 'auto', 100],
                                body: rows
                            }
                        },
                        {
                            text: 'Всего роликов: ' + this.eventsList.length + '.',
                        },
                        {
                            text: 'Общий хронометраж: ' + this.totalDuration + ' секунд.'
                        },
                        {
                            text: this.signedBy + ' ______________________',
                            alignment: 'right',
                            style: 'sign'
                        },

                    ],
                    footer: function (currentPage, pageCount) {
                        if (currentPage === pageCount)
                            return [
                                {
                                    text: vm.createdBy,
                                    style: 'contact'
                                }
                            ]
                    },
                    styles: {
                        contact: {
                            fontSize: 8,
                            margin: [7, 0, 0, 20]
                        },
                        header: {
                            fontSize: 18,
                            bold: true,
                        },
                        subheader: {
                            fontSize: 16,
                            bold: true,
                        },
                        tableExample: {
                            margin: [0, 5, 0, 15]
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 13,
                            color: 'black'
                        },
                        sign: {
                            margin: [50, 5, 0, 15]
                        }
                    },
                }
                pdfMake.createPdf(docDefinition).download('optionalName.pdf')
            }
        },
        watch: {
            dateStart(val) {
                this.dateStartFormatted = this.formatDate(this.dateStart)
            },
            dateEnd(val) {
                this.dateEndFormatted = this.formatDate(this.dateEnd)
            },
            chips() {
                this.fetchReportData()
            },
            dateStartFormatted() {
                this.fetchReportData()
            },
            dateEndFormatted() {
                this.fetchReportData()
            },
            timeStart() {
                this.fetchReportData()
            },
            timeEnd() {
                this.fetchReportData()
            }
        },
        beforeMount() {
            this.fetchReportData()
        }
    }
</script>

<style scoped>
    #document-to-export {
        border: solid black 1px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    #document-to-export > p.header {
        padding-top: 7px;
        padding-right: 20px;
        align-self: flex-end;
    }

    #document-to-export > div.summary {
        align-self: flex-start;
        padding-left: 20px;
    }

    #document-to-export > p.footer {
        padding-top: 7px;
        padding-right: 20px;
        align-self: flex-end;
    }

    #document-to-export > p.contact {
        padding-top: 7px;
        padding-left: 20px;
        align-self: flex-start;
        font-size: 12px;
    }
</style>
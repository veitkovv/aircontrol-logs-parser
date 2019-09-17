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
                            :disabled="loading"
                            :items="EVENTS"
                            chips
                            color="blue-grey lighten-2"
                            label="Выберите ролик(и)"
                            item-text="name"
                            item-value="name"
                            multiple
                            @update:search-input="eventListAutocomplete"
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
                        <template>
                            <v-toolbar>
                                <v-toolbar-title>Исполнитель</v-toolbar-title>
                                <v-autocomplete
                                        v-model="createdBy"
                                        :loading="loading"
                                        :items="DOERS"
                                        :search-input.sync="createdBy.name"
                                        class="mx-4"
                                        flat
                                        hide-no-data
                                        hide-details
                                        label="Выберите исполнителя или создайте нового"
                                        solo-inverted
                                        return-object
                                        item-text="name"
                                ></v-autocomplete>
                                <v-btn
                                        icon
                                        :disabled="createdBy.name === null"
                                        @click.native="clearCreatedBy()"
                                >
                                    <v-icon>clear</v-icon>
                                </v-btn>
                                <v-btn
                                        icon
                                        :disabled="createdBy.name === null"
                                        color="primary"
                                        @click.native="createOrUpdateDoer(createdBy)"
                                >
                                    <v-icon>save</v-icon>
                                </v-btn>
                                <v-btn
                                        :disabled="createdBy.name === null"
                                        icon
                                        color="error"
                                        @click.native="deleteDoer(createdBy)"
                                >
                                    <v-icon>delete</v-icon>
                                </v-btn>
                            </v-toolbar>
                        </template>
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
                                <th>Наименование</th>
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
                        <p class="contact">Исп. {{createdBy.name}}</p>
                    </v-col>
                    <v-col>
                        <v-btn
                                large
                                block
                                color="success"
                                @click="makeDocx"
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
    import {mapActions, mapGetters, mapMutations} from 'vuex'
    import {Document, Packer, Paragraph, TextRun, Header, Footer, Table, AlignmentType, HeadingLevel} from "docx";
    import {saveAs} from 'file-saver';

    export default {
        name: "AppReportForm",
        data() {
            return {
                loading: false,
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
                reportFor: '',
                signedBy: 'Начальник программной дирекции О.А. Криберг',
                createdBy: {
                    name: null
                },
            }
        },

        computed: {
            ...mapGetters([
                'EVENTS',
                'APP_TITLE',
                'DOERS',
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
            },
            eventsList() {
                return this.EVENTS.filter(x => this.chips.includes(x.name))
            },
        },

        methods: {
            ...mapActions([
                'fetchEvents',
                'fetchDoers',
                'createOrUpdateDoer',
                'deleteDoer',
            ]),
            ...mapMutations([
                'SET_TITLE',
                'SET_DOERS'
            ]),

            fetchReportData() {
                this.loading = true
                this.fetchEvents({
                    startBefore: this.startBefore,
                    startAfter: this.startAfter
                }).then(() => this.loading = false)
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
            eventListAutocomplete(item) {
                if (item !== null) {
                    return this.EVENTS.filter(i => i.name.includes(item));
                } else return this.EVENTS
            },
            remove(item) {
                this.chips.splice(this.chips.indexOf(item.name), 1)
                this.chips = [...this.chips]
            },
            dateTimeHumanFormat(datetime) {
                let moment = require('moment');
                return moment(datetime).format("YYYY-MM-DD HH:mm:ss")
            },
            clearCreatedBy() {
                this.createdBy = {
                    name: null
                }
            },

            makeDocx() {
                // Create document
                let doc = new Document();
                let vm = this;

                const table = new Table({
                    rows: this.eventsList.length + 1,
                    columns: 3,
                });

                table.getCell(0, 0).add(new Paragraph({
                    text: "Время выхода в эфир",
                    heading: HeadingLevel.SUBTITLE,
                    alignment: AlignmentType.CENTER
                }));
                table.getCell(0, 1).add(new Paragraph({
                    text: "Наименование",
                    heading: HeadingLevel.SUBTITLE,
                    alignment: AlignmentType.CENTER
                }));
                table.getCell(0, 2).add(new Paragraph({
                    text: "Хронометраж",
                    heading: HeadingLevel.SUBTITLE,
                    alignment: AlignmentType.CENTER
                }));

                for (let [index, item] of this.eventsList.entries()) {
                    table.getCell(index + 1, 0).add(new Paragraph(this.dateTimeHumanFormat(item.start)));
                    table.getCell(index + 1, 1).add(new Paragraph(item.name));
                    table.getCell(index + 1, 2).add(new Paragraph(item.duration));
                }


                // Documents contain sections, you can have multiple sections per document, go here to learn more about sections
                // This simple example will only contain one section
                doc.addSection({
                    properties: {},
                    footers: {
                        default: new Footer({
                            children: [new Paragraph("Исп. " + vm.createdBy.name)],
                        }),
                    },
                    children: [
                        new Paragraph({
                            text: vm.reportFor,
                            spacing: {
                                before: 3900,
                                after: 500,
                            },
                            alignment: AlignmentType.RIGHT
                        }),
                        new Paragraph({
                            text: "Эфирная справка о материалах, прошедших в эфире телеканала",
                            alignment: AlignmentType.CENTER
                        }),
                        new Paragraph({
                            text: "ОГТРК «Ямал-Регион»",
                            alignment: AlignmentType.CENTER
                        }),
                        new Paragraph({
                            text: 'период размещения: c ' + this.dateStart + ' ' + this.timeStart + ' по ' + this.dateEnd + ' ' + this.timeEnd,
                            alignment: AlignmentType.CENTER,
                            spacing: {
                                after: 300
                            }
                        }),
                        table,
                        new Paragraph({
                            text: 'Всего роликов: ' + this.eventsList.length + '.',
                            spacing: {
                                before: 300
                            }
                        }),
                        new Paragraph('Общий хронометраж: ' + this.totalDuration + ' секунд.'),
                        new Paragraph({
                            text: this.signedBy + ' ______________________',
                            spacing: {
                                before: 300
                            }
                        }),

                    ],
                });

                Packer.toBlob(doc).then((blob) => {
                    // saveAs from FileSaver will download the file
                    saveAs(blob, "Справка.docx");
                });
            }
        },
        watch: {
            dateStart(val) {
                this.dateStartFormatted = this.formatDate(this.dateStart)
            },
            dateEnd(val) {
                this.dateEndFormatted = this.formatDate(this.dateEnd)
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
            },
        },
        beforeMount() {
            this.fetchReportData()
            this.fetchDoers()
            this.SET_TITLE('Создание эфирной справки')
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
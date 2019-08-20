<template>
    <v-layout fill-height>
        <v-flex>
            <v-sheet height="64">
                <v-toolbar flat color="white">
                    <v-btn outlined class="mr-4" @click="setToday">
                        Today
                    </v-btn>
                    <v-btn fab text small @click="prev">
                        <v-icon small>arrow_back_ios</v-icon>
                    </v-btn>
                    <v-btn fab text small @click="next">
                        <v-icon small>arrow_forward_ios</v-icon>
                    </v-btn>
                    <v-toolbar-title>{{ title }}</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-menu bottom right>
                        <template v-slot:activator="{ on }">
                            <v-btn
                                    outlined
                                    v-on="on"
                            >
                                <span>{{ typeToLabel[type] }}</span>
                                <v-icon right>arrow_drop_down</v-icon>
                            </v-btn>
                        </template>
                        <v-list>
                            <v-list-item @click="type = 'day'">
                                <v-list-item-title>Day</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="type = 'week'">
                                <v-list-item-title>Week</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="type = 'month'">
                                <v-list-item-title>Month</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="type = '4day'">
                                <v-list-item-title>4 days</v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                </v-toolbar>
            </v-sheet>
            <v-sheet height="700">
                <v-calendar
                        ref="calendar"
                        v-model="focus"
                        color="primary"
                        :events="getEvents"
                        :event-color="getEventColor"
                        :event-margin-bottom="3"
                        :now="today"
                        :type="type"
                        :locale="locale"
                        :weekdays="weekdays"
                        :short-weekdays="shortWeekdays"
                        :short-months="shortMonths"
                        interval-height="40"
                        interval-minutes="5"
                        interval-count="720"
                        @click:event="showEvent"
                        @click:more="viewDay"
                        @click:date="viewDay"
                        @change="updateRange"
                >
                    <!-- the events at the top (all-day) -->
                    <template v-slot:day-header="{ date }">
                        <template v-for="event in getEventsMap[date]">
                            <!-- all day events don't have time -->
                            <div
                                    v-if="!event.time"
                                    :key="event.title"
                                    class="my-event"
                                    @click="open(event)"
                                    v-html="event.title"
                            ></div>
                        </template>
                    </template>
                    <!-- the events at the bottom (timed) -->
                    <template v-slot:day-body="{ date, timeToY, minutesToPixels }">
                        <template v-for="event in getEventsMap[date]">
                            <!-- timed events -->
                            <div
                                    v-if="event.time"
                                    :key="event.title"
                                    :style="{ top: timeToY(event.time) + 'px', height: minutesToPixels(event.duration) + 'px' }"
                                    class="my-event with-time"
                                    @click="open(event)"
                                    v-html="event.title"
                            ></div>
                        </template>
                    </template>
                </v-calendar>
                <v-menu
                        v-model="selectedOpen"
                        :close-on-content-click="false"
                        :activator="selectedElement"
                        full-width
                        offset-x
                >
                    <v-card
                            color="grey lighten-4"
                            min-width="350px"
                            flat
                    >
                        <v-toolbar
                                :color="selectedEvent.color"
                                dark
                        >
                            <v-btn icon>
                                <v-icon>edit</v-icon>
                            </v-btn>
                            <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
                            <v-spacer></v-spacer>
                            <v-btn icon>
                                <v-icon>favorite</v-icon>
                            </v-btn>
                            <v-btn icon>
                                <v-icon>more_vert</v-icon>
                            </v-btn>
                        </v-toolbar>
                        <v-card-text>
                            <span v-html="selectedEvent.details"></span>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn
                                    text
                                    color="secondary"
                                    @click="selectedOpen = false"
                            >
                                Cancel
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-menu>
            </v-sheet>
        </v-flex>
    </v-layout>
</template>

<script>
    import {mapActions, mapGetters} from 'vuex'

    export default {
        data: () => ({
            today: '2016-09-08',
            focus: '2016-09-08',
            type: 'month',
            weekdays: [1, 2, 3, 4, 5, 6, 0],
            locale: 'ru-ru',
            typeToLabel: {
                month: 'Month',
                week: 'Week',
                day: 'Day',
                '4day': '4 Days',
            },
            start: null,
            end: null,
            selectedEvent: {},
            selectedElement: null,
            selectedOpen: false,
            shortWeekdays: false,
            shortMonths: false
        }),
        computed: {
            ...mapGetters([
                'EVENTS',
            ]),
            getEvents() {
                let moment = require('moment');
                return this.EVENTS.map(event => ({
                    "name": event.name,
                    "start": moment(event.start).format("YYYY-MM-DD HH:mm:ss"),
                    "end": moment(event.end).format("YYYY-MM-DD HH:mm:ss"),
                    "color": "green"
                }))
            },
            title() {
                const {start, end} = this
                if (!start || !end) {
                    return ''
                }

                const startMonth = this.monthFormatter(start)
                const endMonth = this.monthFormatter(end)
                const suffixMonth = startMonth === endMonth ? '' : endMonth

                const startYear = start.year
                const endYear = end.year
                const suffixYear = startYear === endYear ? '' : endYear

                const startDay = start.day + this.nth(start.day)
                const endDay = end.day + this.nth(end.day)

                switch (this.type) {
                    case 'month':
                        return `${startMonth} ${startYear}`
                    case 'week':
                    case '4day':
                        return `${startMonth} ${startDay} ${startYear} - ${suffixMonth} ${endDay} ${suffixYear}`
                    case 'day':
                        return `${startMonth} ${startDay} ${startYear}`
                }
                return ''
            },
            monthFormatter() {
                return this.$refs.calendar.getFormatter({
                    timeZone: 'Asia/Yekaterinburg', month: 'long',
                })
            },
        },
        methods: {
            viewDay({date}) {
                this.focus = date
                this.type = 'day'
            },
            getEventColor(event) {
                return event.color
            },
            setToday() {
                this.focus = this.today
            },
            prev() {
                this.$refs.calendar.prev()
            },
            next() {
                this.$refs.calendar.next()
            },
            showEvent({nativeEvent, event}) {
                const open = () => {
                    this.selectedEvent = event
                    this.selectedElement = nativeEvent.target
                    setTimeout(() => this.selectedOpen = true, 10)
                }

                if (this.selectedOpen) {
                    this.selectedOpen = false
                    setTimeout(open, 10)
                } else {
                    open()
                }

                nativeEvent.stopPropagation()
            },
            updateRange({start, end}) {
                // You could load events from an outside source (like database) now that we have the start and end dates on the calendar
                this.start = start
                this.end = end
            },
            nth(d) {
                return d > 3 && d < 21
                    ? 'th'
                    : ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][d % 10]
            },
            ...mapActions([
                'fetchEvents',
            ])
        },
        beforeMount() {
            this.fetchEvents()
        }
    };
</script>

<style scoped>
    .my-event {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        border-radius: 2px;
        background-color: #1867c0;
        color: #ffffff;
        border: 1px solid #1867c0;
        font-size: 12px;
        padding: 3px;
        cursor: pointer;
        margin-bottom: 1px;
        left: 4px;
        margin-right: 8px;
        position: relative;
    }

    .my-event.with-time {
        position: absolute;
        right: 4px;
        margin-right: 0px;
    }
</style>
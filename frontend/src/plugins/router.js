import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Календарь',
            icon: 'calendar_today',
            component: () => import('../components/AppCalendar')
        },
        {
            path: '/report',
            name: 'Эфирная справка',
            icon: 'edit',
            component: () => import('../components/AppReportForm')
        },
        {
            path: '/about',
            name: 'О приложении',
            icon: 'announcement',
            component: () => import('../components/About')
        },
        {
            path: '*',
            component: () => import('../components/AppNotFound')
        }
    ]
})

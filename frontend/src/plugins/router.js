import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Эфирная справка ТВ',
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

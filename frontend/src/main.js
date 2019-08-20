import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './plugins/router'
import {store} from './plugins/store/main'

import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.config.productionTip = false


new Vue({
    vuetify,
    router,
    store,
    render: h => h(App)
}).$mount('#app')

import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import '@mdi/font/css/materialdesignicons.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import {Ripple} from 'vuetify/lib/directives'


Vue.use(Vuetify, {
    directives: {
        Ripple
    }
});

export default new Vuetify({
    icons: {
        iconfont: 'md',
    },

});

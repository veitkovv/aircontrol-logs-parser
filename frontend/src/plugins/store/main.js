import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);


const state = {
    events: [],
    appTitle: ''
};
const getters = {
    EVENTS: state => {
        return state.events
    },
    APP_TITLE: state => {
        return state.appTitle
    }
};
const mutations = {
    SET_EVENTS: (state, payload) => {
        state.events = payload
    },
    SET_TITLE: (state, payload) => {
        state.appTitle = payload
    }
};
const actions = {
    async fetchEvents({commit}, {startAfter, startBefore}) {
        // Пользователь выбрал диапазон дат, получаем список всех роликов, сохраняем в EVENTS
        // https://fetch.spec.whatwg.org/#fetch-api
        let url = new URL("http://" + process.env.VUE_APP_API_ENDPOINT + "/rolls/?start_after=" + startAfter + "&start_before=" + startBefore)

        // для реактивной строки поиска - фильтр только по датам
        await fetch(url.href)
            .then(response => response.json())
            .then(data => commit('SET_EVENTS', data.results))
            .catch(error => {
                alert(error)
            })
    }
};


export const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
    modules: {}
});
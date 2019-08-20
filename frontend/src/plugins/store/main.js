import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);


const state = {
    events: []
};
const getters = {
    EVENTS: state => {
        return state.events
    }
};
const mutations = {
    SET_EVENTS: (state, payload) => {
        state.events = payload
    }
};
const actions = {
    async fetchEvents({commit}) {
        await fetch(`http://api.localhost/rolls/`)
            .then(response => response.json())
            .then(data => commit('SET_EVENTS', data.results))
    }
};


export const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
    modules: {}
});
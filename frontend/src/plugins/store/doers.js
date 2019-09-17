import apiEndpoint from '../../../apiEndoint'

const state = {
    doers: [],
}

const getters = {
    DOERS: state => {
        return state.doers
    }
}

const mutations = {
    SET_DOERS: (state, payload) => {
        state.doers = payload
    },
    DELETE_DOER(state, id) {
        let index = state.doers.findIndex(doer => doer.id === id)
        state.doers.splice(index, 1)
    }
}

const actions = {
    async fetchDoers({commit}) {
        const url = new URL("http://" + apiEndpoint + "/created-by/")
        await fetch(url.href)
            .then(response => response.json())
            .then(data => commit('SET_DOERS', data.results))
            .catch(error => {
                alert(error)
            })
    },
    async createOrUpdateDoer({commit}, doer) {
        if (doer.hasOwnProperty("id")) {
            const url = new URL("http://" + apiEndpoint + "/created-by/" + doer.id + "/")

            await fetch(url.href, {
                method: "PUT",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: doer.name
                })
            })
                .then(response => console.log(response.ok))
                .then(() => actions.fetchDoers({commit}))
                .catch(error => {
                    alert(error)
                })
        } else {
            const url = new URL("http://" + apiEndpoint + "/created-by/")

            await fetch(url.href, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({name: doer.name})
            })
                .then(response => response.json())
                .then(data => actions.fetchDoers({commit}))
                .catch(error => {
                    alert(error)
                })
        }
    },

    async deleteDoer({commit}, doer) {
        const url = new URL("http://" + apiEndpoint + "/created-by/" + doer.id + "/")

        await fetch(url.href, {
            method: "DELETE",
        })
            .then(response => console.log(response.ok))
            .then(commit('DELETE_DOER', doer.id))
            .then(() => actions.fetchDoers({commit}))
            .catch(error => {
                alert(error)
            })
    }
}

export default {
    state,
    getters,
    actions,
    mutations,
};
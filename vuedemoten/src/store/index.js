import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
import menus from './modules/menus'
import permissions from './modules/permissions'
import roles from './modules/roles'
import peoples from './modules/peoples'
import management from './modules/management'
import process from './modules/process'
import displaystand from './modules/displaystand'
import failsearch from './modules/failsearch'
import whitelist from './modules/whitelist'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    menus,
    permissions,
    roles,
    peoples,
    management,
    process,
    displaystand,
    failsearch,
    whitelist,
  },
  getters
})

export default store

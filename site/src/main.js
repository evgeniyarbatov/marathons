import Vue, { createApp } from '@vue/compat'
import { BootstrapVue } from 'bootstrap-vue-next'

import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import App from './App.vue'

Vue.use(BootstrapVue)

createApp(App).mount('#app')

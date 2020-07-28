import {getFailSearch} from '@/api/failsearch'

const state = {}
const mutations = {}
const actions = {
    GetFailSearch({commit},data){
        return new Promise((resolve,reject)=>{
            getFailSearch(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    }
    
}

export default {
    namespaced: true,
    state,mutations,actions
}
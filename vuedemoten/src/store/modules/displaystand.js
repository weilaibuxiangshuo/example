import {getDisplaystand,delDisplaystand} from '@/api/displaystand'

const state = {}
const mutations = {}
const actions = {
    GetDisplaystand({commit},data){
        return new Promise((resolve,reject)=>{
            getDisplaystand(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    DelDisplaystand({commit},data){
        return new Promise((resolve,reject)=>{
            delDisplaystand(data).then(response=>{
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
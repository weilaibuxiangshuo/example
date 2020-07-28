import {addEventprocessFail,eventprocessConfirm,getEventprocess,eventprocessStatus} from '@/api/process'

const state = {}
const mutations = {}
const actions = {
    AddEventprocessFail({commit},data){
        return new Promise((resolve,reject)=>{
            addEventprocessFail(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    GetMenuList({commit,state},data){
        return new Promise((resolve,reject)=>{
            getMenuList().then(response=>{
                // console.log(response)
                state.selectDataState = response.data
                resolve(response)
            })
        })
    },
    GetEventprocess({commit},data){
        return new Promise((resolve,reject)=>{
            getEventprocess(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    EventprocessStatus({commit},data){
        return new Promise((resolve,reject)=>{
            eventprocessStatus(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    EventprocessConfirm({commit},data){
        return new Promise((resolve,reject)=>{
            eventprocessConfirm(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
}

export default {
    namespaced: true,
    state,mutations,actions
}
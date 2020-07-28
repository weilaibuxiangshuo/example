import {addManagement,getMenuList,putManagement,getManagement,managementStatus,delManagement} from '@/api/management'

const state = {}
const mutations = {}
const actions = {
    AddManagement({commit},data){
        return new Promise((resolve,reject)=>{
            addManagement(data).then(response=>{
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
    GetManagement({commit},data){
        return new Promise((resolve,reject)=>{
            getManagement(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    ManagementStatus({commit},data){
        return new Promise((resolve,reject)=>{
            managementStatus(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    PutManagement({commit},data){
        return new Promise((resolve,reject)=>{
            putManagement(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    DelManagement({commit},data){
        return new Promise((resolve,reject)=>{
            delManagement(data).then(response=>{
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
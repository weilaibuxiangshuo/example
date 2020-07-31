import {setWhitelist,addWhitelist,getWhitelist,putWhitelist,delWhitelist} from '@/api/whitelist'

const state={}
const mutations={}
const actions = {
    AddWhitelist({commit},data){
        return new Promise((resolve,reject)=>{
            addWhitelist(data).then(response=>{
                resolve(response)
            })
        })
    },
    SetWhitelist({commit},data){
        return new Promise((resolve,reject)=>{
            setWhitelist(data).then(response=>{
                resolve(response)
            })
        })
    },
    GetWhitelist({commit},data){
        return new Promise((resolve,reject)=>{
            getWhitelist(data).then(response=>{
                resolve(response)
            })
        })
    },

    PutWhitelist({commit},data){
        return new Promise((resolve,reject)=>{
            putWhitelist(data).then(response=>{
                resolve(response)
            })
        })
    },
    DelWhitelist({commit},data){
        return new Promise((resolve,reject)=>{
            delWhitelist(data).then(response=>{
                resolve(response)
            })
        })
    }
}

export default {
    namespaced:true,
    state,mutations,actions,
}
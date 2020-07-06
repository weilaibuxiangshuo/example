import {addPermission,getPermissionMenu,getPermission,putPermission,delPermission} from '@/api/permissions'

const state={}
const mutations={}
const actions = {
    AddPermission({commit},data){
        return new Promise((resolve,reject)=>{
            addPermission(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    GetPermissionMenu({commit,state},data){
        return new Promise((resolve,reject)=>{
            getPermissionMenu().then(response=>{
                // console.log(response)
                state.selectDataState = response.data
                resolve(response)
            })
        })
    },
    GetPermission({commit},data){
        return new Promise((resolve,reject)=>{
            getPermission(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    PutPermission({commit},data){
        return new Promise((resolve,reject)=>{
            putPermission(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    DelPermission({commit},data){
        return new Promise((resolve,reject)=>{
            delPermission(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    }
}

export default {
    namespaced:true,
    state,mutations,actions,
}
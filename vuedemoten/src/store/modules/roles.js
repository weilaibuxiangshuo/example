import {getRolePermission,addRole,getRole,putRole,delRole} from '@/api/roles'

const state={}
const mutations={}
const actions = {
    AddRole({commit},data){
        return new Promise((resolve,reject)=>{
            addRole(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    GetRole({commit},data){
        // console.log("GetRole")
        return new Promise((resolve,reject)=>{
            getRole(data).then(response=>{
                // console.log(response,"GetRole")
                resolve(response)
            })
        })
    },
    GetRolePermission({commit,state},data){
        // console.log("GetRolePermission")
        return new Promise((resolve,reject)=>{
            getRolePermission().then(response=>{
                // console.log(response,"GetRolePermission")
                resolve(response)
            })
        })
    },

    PutRole({commit},data){
        return new Promise((resolve,reject)=>{
            putRole(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    DelRole({commit},data){
        return new Promise((resolve,reject)=>{
            delRole(data).then(response=>{
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
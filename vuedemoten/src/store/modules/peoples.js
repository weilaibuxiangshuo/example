import {getUserRole,addUser,getUser,putUser,delUser} from '@/api/peoples'

const state={}
const mutations={}
const actions = {
    AddUser({commit},data){
        return new Promise((resolve,reject)=>{
            addUser(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    GetUser({commit},data){
        // console.log("GetRole")
        return new Promise((resolve,reject)=>{
            getUser(data).then(response=>{
                // console.log(response,"GetRole")
                resolve(response)
            })
        })
    },
    GetUserRole({commit,state},data){
        // console.log("GetRolePermission")
        return new Promise((resolve,reject)=>{
            getUserRole().then(response=>{
                // console.log(response,"GetRolePermission")
                resolve(response)
            })
        })
    },

    PutUser({commit},data){
        return new Promise((resolve,reject)=>{
            putUser(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    DelUser({commit},data){
        return new Promise((resolve,reject)=>{
            delUser(data).then(response=>{
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
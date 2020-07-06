import {addMenu,getMenuList,getMenu,putMenu,delMenu} from '@/api/menus'

const defaultState = () =>{
    return {
        selectDataState:[]
    }
}


const state = defaultState
const mutations = {

}
const actions = {
    AddMenu({commit},data){
        return new Promise((resolve,reject)=>{
            addMenu(data).then(response=>{
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
    GetMenu({commit},data){
        return new Promise((resolve,reject)=>{
            getMenu(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    PutMenu({commit},data){
        return new Promise((resolve,reject)=>{
            putMenu(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    },
    DelMenu({commit},data){
        return new Promise((resolve,reject)=>{
            delMenu(data).then(response=>{
                // console.log(response)
                resolve(response)
            })
        })
    }
}

export default {
    namespaced:true,
    state,mutations,actions
}
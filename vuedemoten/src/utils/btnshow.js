import Vue from 'vue'

Vue.directive("dataBtnControl",{
    inserted:(el, binding, vnode)=>{
        const per = binding.value.meta.permission
        let isBool = null
        for (let n in per){
            if(per[n]!=="超级管理组"){
                isBool = 1
            }
        }
        if(!!isBool){
            el.parentNode.removeChild(el)
        }
    },
})


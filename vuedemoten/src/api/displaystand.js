import request from '@/utils/request'



// 分页
export const getDisplaystand = (data) => {
    return request({
        url:`/displaystand/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:data.search
    })
}

// 删除
export const delDisplaystand = (data) => {
    return request({
        url:`/displaystand/`,
        method:"delete",
        data
    })
}






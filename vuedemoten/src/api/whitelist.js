import request from '@/utils/request'

// 获取信息
export const setWhitelist = (data) => {
    return request({
        url:"/whitelist/set/",
        method:"post",
        data:data,
    })
}

// 添加
export const addWhitelist = (data) => {
    return request({
        url:"/whitelist/",
        method:"post",
        data:data,
    })
}

// 分页
export const getWhitelist = (data) => {
    return request({
        url:`/whitelist/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:{"search":data.search}
    })
}
// 编辑
export const putWhitelist = (data) => {
    return request({
        url:`/whitelist/`,
        method:"put",
        data,
    })
}
// 删除
export const delWhitelist = (data) => {
    return request({
        url:`/whitelist/`,
        method:"delete",
        data
    })
}
import request from '@/utils/request'

// 获取信息
export const getRolePermission = () => {
    return request({
        url:"/role/permission/",
        method:"get",
    })
}

// 添加
export const addRole = (data) => {
    return request({
        url:"/role/",
        method:"post",
        data:data,
    })
}

// 分页
export const getRole = (data) => {
    return request({
        url:`/role/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:{"search":data.search}
    })
}
// 编辑
export const putRole = (data) => {
    return request({
        url:`/role/`,
        method:"put",
        data,
    })
}
// 删除
export const delRole = (data) => {
    return request({
        url:`/role/`,
        method:"delete",
        data
    })
}
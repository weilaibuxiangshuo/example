import request from '@/utils/request'

// 获取信息
export const getPermissionMenu = () => {
    return request({
        url:"/permission/menu/",
        method:"get",
    })
}

// 添加
export const addPermission = (data) => {
    return request({
        url:"/permission/",
        method:"post",
        data:data,
    })
}

// 分页
export const getPermission = (data) => {
    return request({
        url:`/permission/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:{"search":data.search}
    })
}
// 编辑
export const putPermission = (data) => {
    return request({
        url:`/permission/`,
        method:"put",
        data,
    })
}
// 删除
export const delPermission = (data) => {
    return request({
        url:`/permission/`,
        method:"delete",
        data
    })
}
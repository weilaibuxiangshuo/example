import request from '@/utils/request'

// 获取信息
export const getUserRole = () => {
    return request({
        url:"/user/role/",
        method:"get",
    })
}

// 添加
export const addUser = (data) => {
    return request({
        url:"/user/",
        method:"post",
        data:data,
    })
}

// 分页
export const getUser = (data) => {
    return request({
        url:`/user/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:{"search":data.search}
    })
}
// 编辑
export const putUser = (data) => {
    return request({
        url:`/user/`,
        method:"put",
        data,
    })
}
// 删除
export const delUser = (data) => {
    return request({
        url:`/user/`,
        method:"delete",
        data
    })
}
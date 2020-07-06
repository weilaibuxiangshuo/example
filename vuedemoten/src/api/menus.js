import request from '@/utils/request'

// 获取信息
export const getMenuList = () => {
    return request({
        url:"/menu/list/",
        method:"get",
    })
}

// 添加
export const addMenu = (data) => {
    return request({
        url:"/menu/",
        method:"post",
        data:data,
    })
}

// 分页
export const getMenu = (data) => {
    return request({
        url:`/menu/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:{"search":data.search}
    })
}
// 编辑
export const putMenu = (data) => {
    return request({
        url:`/menu/`,
        method:"put",
        data,
    })
}
// 删除
export const delMenu = (data) => {
    return request({
        url:`/menu/`,
        method:"delete",
        data
    })
}
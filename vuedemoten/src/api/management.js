import request from '@/utils/request'

// 获取信息
export const getMenuList = () => {
    return request({
        url:"/menu/list/",
        method:"get",
    })
}

// 添加
export const addManagement = (data) => {
    return request({
        url:"/management/",
        method:"post",
        data:data,
    })
}

// 分页
export const getManagement = (data) => {
    return request({
        url:`/management/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:data.search
    })
}


// 编辑
export const putManagement = (data) => {
    return request({
        url:`/management/`,
        method:"put",
        data,
    })
}

// 冻结
export const managementStatus = (data) => {
    return request({
        url:`/management/status/`,
        method:"post",
        data,
    })
}
// 删除
export const delManagement = (data) => {
    return request({
        url:`/management/`,
        method:"delete",
        data
    })
}
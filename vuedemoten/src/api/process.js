import request from '@/utils/request'


// 添加
export const addEventprocessFail = (data) => {
    return request({
        url:"/eventprocess/fail/",
        method:"post",
        data:data,
    })
}

// 分页
export const getEventprocess = (data) => {
    return request({
        url:`/eventprocess/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:data.search
    })
}




// 冻结
export const eventprocessStatus = (data) => {
    return request({
        url:`/eventprocess/status/`,
        method:"post",
        data,
    })
}


// 确定
export const eventprocessConfirm = (data) => {
    return request({
        url:`/eventprocess/confirm/`,
        method:"post",
        data,
    })
}

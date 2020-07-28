import request from '@/utils/request'



// 分页
export const getFailSearch = (data) => {
    return request({
        url:`/failsearch/${data.currentpage}/${data.pagesize}/`,
        method:"get",
        params:data.search
    })
}







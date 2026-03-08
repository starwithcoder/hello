import axios from 'axios'


export default {

    getAll(){
        return axios.get('/permissions/get')
    },
    getOne(id){
        return axios.get(`/permissions/${id}`)
    },
    create(data){
        return axios.post(`/permissions/post`, data)
    },
    update(data){
        return axios.put(`/permissions/update`, data)
    },
    delete(permission_id){
        return axios.delete(`/permissions/delete?permission_id=${permission_id}`)
    },

    search(keyword){
        return axios.get(`/permissions/search?keyword=${keyword}`)
    }



}
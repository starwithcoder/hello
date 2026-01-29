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
    delete(data){
        return axios.delete(`/permissions/delete`,data)
    }



}
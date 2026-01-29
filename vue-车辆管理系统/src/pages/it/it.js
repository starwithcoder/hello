import axios from 'axios'


export default {

    getAll(){
        return axios.get('/it/get')
    },
    getOne(id){
        return axios.get(`/it/${id}`)
    },
    create(data){
        return axios.post(`/it/post`, data)
    },
    update(data){
        return axios.put(`/it/update`, data)
    },
    delete(data){
        return axios.delete(`/it/delete`,data)
    }



}
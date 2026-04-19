import axios from 'axios'


export default {

    getAll() {
        return axios.get('/roles/get')
    },
    getOne(id) {
        return axios.get(`/roles/${id}`)
    },
    create(data) {
        return axios.post(`/roles/post`, data)
    },
    update(data) {
        return axios.put(`/roles/put`, data)
    },
    delete(name) {
        return axios.delete(`/roles/delete?role_name=${name}`)
    },
      getAllP(){
        return axios.get('/permissions/get')
    },
    getOneP(id){
        return axios.get(`/permissions/${id}`)
    },
}




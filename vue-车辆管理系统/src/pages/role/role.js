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
        return axios.put(`/roles/update`, data)
    },
    delete(data) {
        return axios.delete(`/roles/delete`, data)
    }
}




import axios  from "axios";

export default{


    sendfile(){
        return axios.post('/test/sendfile/')
}
}
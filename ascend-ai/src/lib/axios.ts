import axios from "axios"
import {API} from "@/constants/api"

const apiClient = axios.create({
    baseURL: API.BASE_URL,
    withCredentials: true,
    timeout: 10000,
    headers:{
        "Content-Type": "application/json",
    },
});


export default apiClient;
import axios from '../../utils/http'

export function register (user) {
    return axios.post('/api/auth/register', user)
}

export function login (user) {
    return axios.post('/api/auth/login', user)
}

export function getUserInfo (token) {
    return axios.post('/api/auth/get-user-info', { 'token': token })
}

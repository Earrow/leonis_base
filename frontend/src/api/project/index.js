import axios from '../../utils/http'

export function getProjectList (department_id) {
    return axios.get('/api/project/get-list', { params: { department_id } })
}

export function getProjectInfo (params) {
    return axios.get('/api/project/get-info', { params: params })
}

export function setUserActiveProject (project_name) {
    return axios.post('/api/project/set-active-project', { project_name })
}

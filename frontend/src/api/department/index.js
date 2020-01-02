import axios from '../../utils/http'

export function getDepartmentList () {
    return axios.get('/api/department/get-list')
}

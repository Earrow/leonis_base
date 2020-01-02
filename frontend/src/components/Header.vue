<template>
    <div id="page-header">
        <el-card class="header-card" shadow="always">
            <el-row type="flex" justify="space-between">
                <el-col :span="1">
                    <el-button class="btn-collapse" @click="collapse" icon="el-icon-menu"></el-button>
                </el-col>
                <el-col :span="4" class="col-logo">
                    <div class="logo">
                        <a href="/">
                            <h1>Leonis</h1>
                            <span>平台</span>
                        </a>
                    </div>
                </el-col>
                <el-col :span="18" class="project">
                    <el-select v-model="activeProjectName" placeholder="请选择项目" filterable @change="onActiveProjectChange">
                        <el-option-group
                        v-for="group in options"
                        :key="group.label"
                        :label="group.label">
                        <el-option
                            v-for="item in group.options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                        </el-option-group>
                    </el-select>
                </el-col>
                <el-col :span="3">
                    <div class="account">
                        <div class="username">
                            <p>{{ username }}</p>
                            <span>{{ permission }}</span>
                        </div>
                    </div>
                </el-col>
            </el-row>
        </el-card>
    </div>
</template>

<script>
import { getDepartmentList } from '@/api/department'
import { getProjectList, setUserActiveProject } from '@/api/project'

export default {
    name: 'PageHeader',
    data() {
        return {
            options: [],
            activeProjectName: ''
        }
    },
    computed: {
        username() {
            return this.$store.state.user.username
        },
        permission() {
            if (this.$store.state.user.active_project) {
                if (this.$store.state.user.active_project.is_master) {
                    return '管理员'
                }
                else {
                    return '普通用户'
                }
            }

            return ''
        }
    },
    methods: {
        onActiveProjectChange(projectName) {
            this.$store.dispatch('setActiveProject', projectName)
            setUserActiveProject(projectName)
        },
        collapse() {
            this.$store.dispatch('switchCollapse')
        }
    },
    mounted() {
        // 获取部门列表
        getDepartmentList().then(res => {
            for (let d of res.data.departments) {
                let department = {
                    label: d.name,
                    options: []
                }

                // 获取项目列表
                getProjectList(d.id).then(res => {
                    for (let p of res.data.projects) {
                        department.options.push({
                            label: p.name,
                            value: p.name
                        })
                    }
                })

                this.options.push(department)
            }

            // 设置用户之前的活动项目
            if (this.$store.state.user.active_project)
                this.activeProjectName = this.$store.state.user.active_project.name
        }).catch(err => {
              this.$message.error(`获取部门列表失败，${err.response.data.msg}`)
            })
    }
}
</script>

<style>
.box-card {
    width: 100%;
}

.el-card__body {
    padding: .3rem;
}

.col-logo {
    margin-left: .2rem;
}

.logo {
    background: #6164C1;
    text-align: center;
    float: left;
    width: 100%;
}
.logo a{
    padding: 0.9em 3.3em .7em;
    display: flex;
    flex-direction: column;
    justify-content: center;
	text-decoration: none;
}
.logo a h1 {
    color: #fff;
    font-size: 1.5em;
    line-height: 1.2em;
    font-weight: 700;
    margin: .2rem 0;
}
.logo a span {
    color: #F8F8F8;
    font-size: .7em;
    text-align: center;
    letter-spacing: 7px;
}

.account {
    float: right;
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: center;
    padding: 0;
}

.username p{
	font-size:1.4rem;
	color:#DD6777;
	line-height:1em;
    font-weight:700;
    margin: .3rem 0;
}

.username {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.username span {
    font-size: .75rem;
    font-style: italic;
    color: #424f63;
    font-weight: normal;
    text-align: center;
}

.login-state {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: .5rem;
}

.project {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-right: 20%;
    margin-left: .5rem;
}

.btn-collapse {
    width: 100%;
    height: 100%;
    font-size: 1rem;
    text-align: center;
}
</style>

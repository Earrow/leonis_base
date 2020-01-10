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
                            <span class="title">{{ this.GLOBAL.title }}</span>
                            <span class="sub-title">{{ this.GLOBAL.sub_title }}</span>
                        </a>
                    </div>
                </el-col>
                <el-col :span="16" class="project">
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
                        <div class="login-state">
                            <el-dropdown @command="handleLoginCommand">
                                <span class="el-dropdown-link">
                                    <i class="el-icon-arrow-down el-icon--right"></i>
                                </span>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item :command="login_action.name1">{{ login_action.name2 }}</el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
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
            if (this.$store.state.user)
                return this.$store.state.user.username
            
            return '匿名'
        },
        permission() {
            if (this.$store.state.user) 
                if (this.$store.state.user.active_project) {
                    if (this.$store.state.user.active_project.is_master) {
                        return '管理员'
                    }
                    else {
                        return '普通用户'
                    }
                }

            return ''
        },
        login_action() {
            if (this.$store.user !== {}) {
                return {'name1': 'logout', 'name2': '登出'}
            } else {
                return {'name1': 'login', 'name2': '登录'}
            }
        }
    },
    methods: {
        onActiveProjectChange(projectName) {
            this.$store.dispatch('setActiveProject', projectName)
            setUserActiveProject(projectName)
        },
        collapse() {
            this.$store.dispatch('switchCollapse')
        },
        handleLoginCommand(command) {
            if (command === 'logout') {
                this.$store.dispatch('logout')
                .then(() => {
                    let redirect = decodeURIComponent('/login')
                    this.$router.push({
                        path: redirect
                    })
                })
            }
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
    padding: .7em .5em;
    display: flex;
    flex-direction: column;
    justify-content: center;
	text-decoration: none;
}
.logo a .title {
    color: #fff;
    font-size: 1.5em;
    line-height: 1.2em;
    font-weight: 700;
    text-align: center;
    margin: .2rem 0;
}
.logo a .sub-title {
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

.el-dropdown-link {
    cursor: pointer;
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

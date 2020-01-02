<template>
    <div class="register">
        <div class="pad">
            <div class="auth-title"><h3>注册</h3></div>
            <div class="auth-body">
                <el-form :model="formData" :rules="rules" ref="form" label-width="100px" status-icon>
                    <el-form-item label="用户名" prop="username">
                        <el-input v-model="formData.username"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="formData.password" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="password_confirm">
                        <el-input type="password" v-model="formData.password_confirm" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="姓名" prop="name">
                        <el-input v-model="formData.name" @keyup.enter.native="submitForm('form')"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="submitForm('form')">注册</el-button>
                        <el-button @click="resetForm('form')">重置</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Register',
    data () {
        var validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'))
            } else {
                if (this.formData.password_confirm !== '') {
                    this.$refs.form.validateField('password_confirm')
                }
                callback()
            }
        }
        var validatePass2 = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'))
            } else if (value !== this.formData.password) {
                callback(new Error('两次输入密码不一致!'))
            } else {
                callback()
            }
        }
        return {
            formData: {
                username: '',
                password: '',
                password_confirm: '',
                name: ''
            },
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '请输入密码', trigger: 'blur' },
                    { validator: validatePass, trigger: 'blur' }
                ],
                password_confirm: [
                    { required: true, message: '请再次输入密码', trigger: 'blur' },
                    { validator: validatePass2, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        submitForm (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.$store.dispatch('register', this.formData).then(() => {
                        this.$router.push('/')
                    }).catch(err => {
                        let msg = []
                        for (let key in err.response.data.msg)
                            msg.push(err.response.data.msg[key])
                        this.$message.error(`注册失败：${msg.join('；')}`)
                    })
                } else {
                    this.$message.warning('表单异常')
                    return false
                }
            })
        },
        resetForm (formName) {
            this.$refs[formName].resetFields()
        }
    }
}
</script>

<style scoped>
@import url('../../assets/css/auth.css');

.register {
    padding: 3rem 12rem;
}
</style>

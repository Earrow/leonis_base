<template>
  <div class="login">
    <div class="pad">
      <div class="auth-title"><h3>登录</h3></div>
      <div class="auth-top">
        <p>欢迎使用 <strong><em>{{ this.GLOBAL.title }}</em></strong> {{ this.GLOBAL.sub_title }}！</p>
        <p><em>新用户？</em><router-link to="/register">注册»</router-link></p>
      </div>
      <div class="auth-body">
        <el-form :model="formData" :rules="rules" ref="form"  label-width="100px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="formData.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="formData.password" autocomplete="off" @keyup.enter.native="submitForm('form')"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('form')">登录</el-button>
            <el-button @click="resetForm('form')">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      formData: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$store.dispatch('login', this.formData)
            .then(() => {
              return this.$store.dispatch('getUserInfo')
            })
            .then(() => {
              let redirect = decodeURIComponent(this.$route.query.redirect || '/')
              this.$router.push({
                path: redirect
              })
            })
            .catch(err => {
              this.$message.error(`登录失败，${err.response.data.msg}`)
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

.login {
  padding: 3rem 12rem;
}
</style>

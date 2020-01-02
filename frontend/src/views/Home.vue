<template>
    <el-container>
        <el-header height="auto">
            <PageHeader></PageHeader>
        </el-header>

        <el-container class="bottom">
            <el-aside width='initial'>
                <PageSider></PageSider>
            </el-aside>

            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
import PageHeader from '@/components/Header'
import PageSider from '@/components/Sider'

export default {
  name: 'home',
  components: {
    PageHeader,
    PageSider
  }
}
</script>

<style>
    .el-container {
        height: 100%;
    }

    .bottom {
        padding: 12px 20px;
    }
</style>

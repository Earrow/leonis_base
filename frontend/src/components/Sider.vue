<template>
    <div id='page-sider'>
        <el-menu
            :default-active="$route.path"
            router
            :collapse="isCollapse"
            :collapse-transition="false"
            @open="handleOpen"
            @close="handleClose">
            <el-menu-item index="/">
                <i class="el-icon-house"></i>
                <span slot="title">首页</span>
            </el-menu-item>
            <el-menu-item index="/test">
                <i class="el-icon-menu"></i>
                <span slot="title">测试页面</span>
            </el-menu-item>
        </el-menu>
    </div>
</template>

<script>
export default {
    name: 'PageSider',
    data () {
        return {
        }
    },
    computed: {
        isCollapse () {
            return this.$store.state.collapse
        }
    },
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        }
    }
}
</script>

<style>
#page-sider {
    height: 100%;
}

.el-menu {
    height: 100%;
}
</style>

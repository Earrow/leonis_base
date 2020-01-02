<template>
    <div>
        这是一个测试页面，当前项目为{{ project }}
    </div>
</template>

<script>
export default {
    name: 'test',
    computed: {
        project() {
            return this.$store.state.user.active_project.name
        }
    }
}
</script>

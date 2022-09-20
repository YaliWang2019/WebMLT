<template src="./index.html">
</template>

<script>
    import axios from "axios"
    export default {
        name: 'App',
        methods: {
            async trigger() {
                try {
                    let res = await axios.get("http://localhost:8888")
                    alert(res.data.message)
                } catch (e) {
                    console.log(e)
                }
            },
            async scipy() {
                try {
                    let res = await axios.get("http://localhost:8888")
                    alert(res.data.message)
                } catch (e) {
                    console.log(e)
                }
            },
        }
    }
</script>

<style src="./style.css"></style>

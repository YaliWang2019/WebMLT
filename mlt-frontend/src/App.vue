<template src="./index.html">
</template>

<script>
    import axios from "axios"
    export default {
        name: 'App',
        methods: {
            async trigger() {
                try {
                    let res = await axios.get("http://localhost:5000")
                    alert(res.data.message)
                } catch (e) {
                    console.log(e)
                }
            },
            async scipy(obj) {
                try {
                    let res = await axios.post("http://localhost:5000", {
                        "name": obj.target[0].value
                    })
                    alert(res.data.messages)
                } catch (e) {
                    console.log(e)
                }
            },
        }
    }
</script>

<style src="./style.css"></style>

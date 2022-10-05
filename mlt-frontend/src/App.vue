<template src="./index.html">
</template>

<script>
    import axios from "axios"
    export default {
        name: 'App',
        methods: {
            async scipy() {
                try {
                    let res = await axios.post("http://localhost:5000", {
                        //The 'obj' object accepted by the function is a submission event, 
                        //the 'target' refers to the form object that initiated this submission event.
                        //It includes the array of the form that the user submitted
                        "name": this.xValue
                    })
                    alert(res.data.messages)
                } catch (e) {
                    console.log(e)
                }
            },

        },
        
    }
  
</script>

<style src="./style.css"></style>

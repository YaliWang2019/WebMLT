<template src="./index.html">
</template>

<script>
    import axios from "axios"
//    import { defineComponent } from 'vue'
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
                        //The 'obj' object accepted by the function is a submission event, 
                        //the 'target' refers to the form object that initiated this submission event.
                        //It includes the array of the form that the user submitted
                        "name": obj.target[0].value
                    })
                    alert(res.data.messages)
                } catch (e) {
                    console.log(e)
                }
            },
            data() {
                return {
                    textFieldValue: ''
                }
            },
            getName() {
                axios.get("https://reqres.in/api/users/2").then(response => {
                    this.textFieldValue = response.data.data.x
                })
            }
        },
        
    }
  
</script>

<style src="./style.css"></style>

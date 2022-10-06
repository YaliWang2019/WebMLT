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
                        x1: this.x1Value,
                        x2: this.x2Value,
                    })
                    alert(res.data.messages)
                } catch (e) {
                    console.log(e)
                }
            },
        },
        data() {
            return {
                x1Value: 1,
                x2Value: 1,
            }
        },
        submitForms : function () {
            document.getElementById("ID1").submit();
            document.getElementById("ID2").submit();
        }
    }
  
</script>

<style src="./style.css"></style>

<template src="./index.html">
</template>

<script>
    import axios from "axios"
    export default {
        name: 'App',
        methods: {
            async scipy() {
                try {
                    let res = await axios.post("http://localhost:5000", 
                    {
                        x1: this.x1Value,
                        x2: this.x2Value,

                    })
                    this.img_from_server = res.chart;
                } catch (e) {
                    console.log(e)
                }
            },
        },
        data() {
            return {
                img_from_server: "",
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

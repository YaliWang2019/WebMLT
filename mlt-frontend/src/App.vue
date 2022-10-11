<template src="./index.html">
</template>

<script>
    import axios from "axios"
    export default {
        name: 'App',
        submitForms: function () {
            document.getElementById("ID1").value.submit();
            document.getElementById("ID2").value.submit();
        },
        methods: {
            async scipy() {
                try {
                    let res = await axios.post("http://localhost:5000", 
                    {
                        x1: this.x1Value,
                        x2: this.x2Value,

                    })
                    this.img_from_server = res.data.chart
                } catch (e) {
                    console.log(e)
                }
            },
        },
        data() {
            return {
                img_from_server: "",
                x1Value: [],
                x2Value: [],
                
            }
        },
    }
  
</script>

<style src="./style.css"></style>

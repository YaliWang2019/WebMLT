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
                    let x1ValueString = this.x1Value
                    let x2ValueString = this.x2Value
                    let x1Values = x1ValueString.split(" ")
                    let x2Values = x2ValueString.split(" ")

                    for (let i in x1Values) {
                        let result = parseFloat(x1Values[i])
                        if (!isNaN(result)) x1Values[i] = result
                        else return alert("x1 is not a vaild number sequence")
                    }

                    for (let i in x2Values) {
                        let result = parseFloat(x2Values[i])
                        if (!isNaN(result)) x2Values[i] = result
                        else return alert("x2 is not a vaild number sequence")
                    }
                    let res = await axios.post("http://localhost:5000", {
                        x1: x1Values,
                        x2: x2Values,

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

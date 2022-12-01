<template>
    <div class="LGR">
      <h1 align = left>Logistic Regression Model</h1>
      <br />
      <h2 align = left>File Upload: </h2>
      <div>
        <em>Please upload a csv file.</em>
        <form @submit.prevent="submit">
        <input type="file" name="file" />
        <button type="submit">Submit</button>
        </form>
        <br />
        
                  
      </div>
    </div>
  </template>
  <script>

  import { defineComponent } from 'vue'
    import axios from "axios"
    export default defineComponent({
        name: 'LGRView',
        methods: {
            async submit(event) {
                console.log(event.target[0].files[0])
                const formData = new FormData()
                formData.append('file', event.target[0].files[0])
                try {
                    const response = await axios.post('http://localhost:5000', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    
                    
                    this.img_from_server = response.data.charts
                    
                } catch (e) {
                    console.log(e)
                }
            }
        },
        data() {
            return {
                img_scatter: "",
                img_train: "",
                img_test: "",
                img_prediction: "",
                img_from_server: "",
                charts: "",
                file: "",
            }
        },
    })
  </script>
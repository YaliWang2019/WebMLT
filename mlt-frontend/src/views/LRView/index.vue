<template>
  <div class="LR">
    <h1 align = left>Linear Regression Model</h1>
    <br />
    <h2 align = left>Phase 1: File upload </h2>
    <div>
        <em>Please upload a csv file.</em>
        <form @submit.prevent="submitFile">
        <input type="file" name="file" />
        <button type="submit">Submit</button>
        </form>
        <br />                
    </div>

    <h2 align = left>Phase 2: Data preprocessing</h2>
    <h3 align = left>This phase removes missing values from your dataset and scales your data.</h3>
    <br />

    <h3 align = left>The preview of your dataset: </h3>
    <br />

    <em>Please select the scaling mode you want to use: </em>
        <form @submit.prevent="scaleMode">
        <select name="scaling" id="scale">
        <option value="normolization">Normalization</option>
        <option value="standardization">Standardization</option>
        </select>
        <input type="submit" value="Submit" />
        </form>


    <h3 align = left></h3>
    <h2 align = left></h2>
        <em>Please select the parameters you want to use: </em>
        <form @submit.prevent="dataPreprocess">
        <select name="languages" id="lang">
        <option value="javascript">JavaScript</option>
        <option value="php">PHP</option>
        <option value="java">Java</option>
        <option value="golang">Golang</option>
        <option value="python">Python</option>
        <option value="c#">C#</option>
        <option value="C++">C++</option>
        <option value="erlang">Erlang</option>
        </select>
    <input type="submit" value="Submit" />
</form>
  </div>
</template>
<script>
import { defineComponent } from 'vue'
import axios from "axios"
export default defineComponent({
    name: 'LRView',
    methods: {
        async submitFile(event) {
            console.log(event.target[0].files[0])
            const formData = new FormData()
            formData.append('file', event.target[0].files[0])
            try {
                const response = await axios.post('http://localhost:5001/datasets', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                    
                    
                alert("CSV file uploaded successfully!")
                    
            } catch (e) {
                console.log(e)
            }
        },

        /* async dataPreprocess(event) {
            console.log(event.target[0].files[0])
            const formData = new FormData()
            formData.append('file', event.target[0].files[0])
            try {
                const response = await axios.post('http://localhost:5000', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                    
                    
                alert(response.data.massage)
                    
            } catch (e) {
                console.log(e)
            }
        } */
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
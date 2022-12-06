<template>
    <div class="LR">
        <h1 align=left>Linear Regression Model</h1>
        <br />
        <h2 align=left>Phase 1: File upload </h2>
        <div>
            <em>Please upload a csv file.</em>
            <form @submit.prevent="submitFile">
                <input type="file" name="file" />
                <button type="submit">Submit</button>
            </form>
            <br />
        </div>
        <h2 align=left>Phase 2: Data preprocessing</h2>
        <h3 align=left>This phase removes missing values from your dataset and scales your data.</h3>
        <h3 align=left>The preview of your dataset after removing missing values: </h3>
        <br />
        <button @click="getPreview">Get Preview</button>
        <br />
        <div v-if="showPreview">
            <table>
                <thead>
                    <tr>
                        <th v-for="(_,index) in rmMissingValuesResult" :key="index">
                            {{index}}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="index in [0, 1, 2, 3, 4]" :key="index">
                        <td v-for="(_,row) in rmMissingValuesResult" :key="row">
                            {{rmMissingValuesResult[row][index]}}
                        </td>
                    </tr>
                </tbody>
            </table>
            
        </div>

        <em>Please select the scaling mode you want to use: </em>
        <form @submit.prevent="scaleMode">
            <select name="scaling" id="scale">
            <option value="normolization">Normalization</option>
            <option value="standardization">Standardization</option>
            </select>
            <input type="submit" value="Submit" />
            
        </form>
        
        <h3 align=left>Scatter chart of your dataset: </h3>
        <img :src="`data:image/png;base64,${scatterResource}`" v-if="scatterResource!=''"/>
        <button @click="() => showLaterSteps = true">Show Later Steps</button>

        <div v-if="showLaterSteps">
            <h3 align=left>Phase 3: Data visualization</h3>
            <h2 align=left></h2>
            <em>Please select the parameters you want to use: </em>
            <form @submit.prevent="dataPreprocess">
            
            <em for="testSize">test_size = </em>
            <input type="text" id="testSize" />
            <br />
            <em for="randomState">random_state = </em>
            <input type="text" id="randomState" />
            <br />
            <input type="submit" value="Submit" />
            </form>
        </div>
    </div>
</template>

<script>
    import {
        defineComponent
    } from 'vue'
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
                    localStorage.setItem('id', response.data.id)
                } catch (e) {
                    console.log(e)
                }
            },
            async getPreview(){
                try{
                    const res = await axios.get(`http://localhost:5001/datasets/${localStorage.getItem('id')}/missingValues`)
                    this.rmMissingValuesResult = res.data
                    this.showPreview = true
                }catch(e){
                    console.log(e)
                }
            },
            async scaleMode(event){
                console.log(event.target[0].value)
                try{
                    const res = await axios.get(`http://localhost:5001/datasets/${localStorage.getItem("id")}/scatter?scaleMode=${event.target[0].value}`)
                    console.log(res.data)
                    this.scatterResource = res.data.imgScatter
                } catch (e) {
                    console.log(e)
                }
            },
            async dataPreprocess(event){
                console.log(event)
            }
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
                file: "",
                showPreview: false,
                showLaterSteps: false,
                rmMissingValuesResult: null,
                scatterResource: "",
            }
        },
    })
</script>
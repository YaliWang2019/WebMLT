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
            <option value="normalization">Normalization</option>
            <option value="standardization">Standardization</option>
            </select>
            <input type="submit" value="Submit" />
            
        </form>
        
        <h3 align=left>Scatter chart of your dataset: </h3>
        <img :src="`data:image/png;base64,${scatterResource}`" v-if="scatterResource!=''"/>
        <button @click="() => showLaterSteps = true">Show Later Steps</button>

        <div v-if="showLaterSteps">
            <h3 align=left>Phase 3: Data visualization</h3>
            <em>Please select the parameters you want to use: </em>
            <form @submit.prevent="dataPreprocess">
            
            <em for="testSize">test_size = </em>
            <input type="text" id="testSize" pattern="^[1-9][0-9]?$" />
            <em>% (Input percentage here.)</em>
            <br />
            <em for="randomState">random_state = </em>
            <input type="text" id="randomState" pattern="^[0-9]*$" />
            <br />
            <input type="submit" value="Submit" />
            </form>

            <h3 align=left>Scatter charts of your train and test datasets: </h3>
            <img :src="`data:image/png;base64,${trainTestResource}`" v-if="trainTestResource !=='' "/>
    

            <h3 align=left>Phase 4: Model training</h3>
            <em>The prediction chart from your dataset: </em>
            <button @click="getPredict" v-if="predictionImg =='' ">Get Prediction</button>
            <br />
            <img :src="`data:image/png;base64,${predictionImg}`" v-if="predictionImg !=='' " />

            <h3 align=left>Phase 5: Accuracy</h3>
            <em>The calculated errors from your dataset: </em>
            <button @click="getCalculation">Get Accuracy</button>
            <div v-if="showAccuracy != '' ">{{showAccuracy}}</div>
            <br />
            
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
                try{
                    const res = await axios.get(`http://localhost:5001/datasets/${localStorage.getItem("id")}/scatter?scaleMode=${event.target[0].value}`)
                    console.log(res.data)
                    this.scatterResource = res.data.imgScatter
                } catch (e) {
                    console.log(e)
                }
            },
            async dataPreprocess(event){
                let params={}
                if(event.target[0].value && event.target[0].value != ""){
                    params.test_size=parseInt(event.target[0].value)*0.01
                }
                if(event.target[1].value && event.target[1].value != ""){
                    params.random_state=parseInt(event.target[1].value)
                }
                try{
                    const res=await axios.get(`http://localhost:5001/datasets/${localStorage.getItem("id")}/train_test`,{params})
                    console.log(res.data)
                    this.trainTestResource = res.data.trainTestestImg
                    
                } catch (e) {
                    console.log(e)
                }
            },
            async getPredict(){
                try{
                    const res = await axios.get(`http://localhost:5001/datasets/${localStorage.getItem("id")}/model_training`)
                    console.log(res.data)
                    this.predictionImg = res.data.imgPrediction
                } catch (e) {
                    console.log(e)
                }
            },
            async getCalculation(){
                try{
                    const res = await axios.get(`http://localhost:5001/datasets/${localStorage.getItem('id')}/calculation`)
                    
                    this.showAccuracy[0] = res.data['Mean Absolute Error:']
                    this.showAccuracy[1] = res.data['Mean Squared Error:']
                    this.showAccuracy[2] = res.data['Root Mean Squared Error:']
                }catch(e){
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
                file: "",
                imgScatter: "",
                showPreview: false,
                showLaterSteps: false,
                rmMissingValuesResult: null,
                scatterResource: "",
                trainTestResource: ["", ""],
                predictionImg: "",
                showAccuracy: ["", "", ""]
            }
        },
    })
</script>
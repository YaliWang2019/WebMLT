<template>
  <div class="LR">
    <h1 align = left>Linear Regression Model</h1>
    <br />
    <h2 align = left>File Upload: </h2>
    <div>
      <em>Please upload a csv file.</em>
      <form @submit.prevent="submit">
      <input type="file" name="file" />
      <button type="submit">Submit</button>
      </form>
      <br />
      <img style="width:400px" :src="`data:image/png;base64,${img_from_server}`" v-if="img_from_server !== ''" />
                
    </div>
  </div>
</template>
<script>
export default {
  name: 'LRView',
}
</script>
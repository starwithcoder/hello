
<template>
  <h2>文件上传</h2>
  <div @drop.prevent="handleDrop" @dragover.prevent>
    <input type="file" accept="image/*" @change="handleChange" >
    <span v-if="uploadStatus">{{uploadMsg}}</span>
    <button @click="upload">确认上传</button>
  </div>


  <el-upload
   v-model:file-list="accident_image_1"
              action="#"
              list-type="picture-card"
              :auto-upload="false"
  >
    <el-button @click="uploadMsgq"  >shangchuan</el-button>
  </el-upload>





</template>


<script setup>
import testApi from './test.js'
import {ref} from "vue";
const selectedFile  = ref([])
const uploadStatus = ref(false)
const uploadMsg = ref('')
const accident_image_1 = ref([])


const uploadMsgq = async () => {
  accident_image_1.value.forEach((item) => {
    console.log(item)
    console.log(item.raw)
  })

}



const handleDrop = async (e) => {
  const file = e.dataTransfer.files[0];
  if (!file)
    return;
  if (!file.type.startsWith('image/'))
    return;
  selectedFile.value.push(file);

}

const handleChange = async (e) => {
  const file = e.target.files[0];
  if (!file)
      return;
  if (!file.type.startsWith('image/'))
      return;
  selectedFile.value.push(file);

}
const upload = async (selectedFile) => {
  uploadStatus.value = true
  uploadMsg.value = '正在上传'
  const formData = new FormData();
  formData.append('image', selectedFile);
  try{

     const response =  await testApi.sendfile(formData);
      uploadMsg.value = '上传成功'
  }catch(error) {
      uploadMsg.value = '上传失败'

  }
}

</script>




<style scoped>

</style>
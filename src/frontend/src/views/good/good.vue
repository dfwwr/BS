<template>
	<el-scrollbar height="100%" style="width: 100%; height: 100%">
	  <div
		style="
		  margin-top: 20px;
		  margin-left: 20px;
		  font-size: 2em;
		  font-weight: bold;
		"
	  >
		商品展示
	  </div>
	  <div style="width: 90%; margin: 0 auto; padding-top: 5vh">
		<div class="goodBox">
			<Agood
			v-for="(card, index) in cards"
			:key="index"
			:title="card.title"
			:description="card.description"
			/>	
		  <!-- 卡片标题 -->
  
		  <!-- 卡片内容
		  <div style="margin-left: 10px; text-align: start; font-size: 16px;">
			<div style=" height: 40px;margin: auto;display: flex;align-items: center;justify-content: center">
			  <div style ="font-size: 1.5rem;font-weight: bolder; margin-top: 20px;text-align: center">
				用 户 登 录
			  </div>
			</div>
			<el-divider/>
			<el-form label-position="right" label-width="100px" style=" font-weight: bolder; font-size: 10px">
			  <el-form-item label="用户名"  style = "margin-top: 5px;">
				<el-input v-model="account" style="width: 12.5vw; margin-left: 1rem" maxlength="18" clearable/>
			  </el-form-item>
			  <el-form-item label="密码" style = "margin-top: 5px;">
				<el-input v-model="password" style="width: 12.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
			  </el-form-item>
			</el-form>
		  </div>
		  卡片操作 
		  <div style="margin-top: 30px; display:flex;justify-content: center">
			<el-button type="primary"  @click="handle()">
			  登录
			</el-button>
			<el-button :icon="Edit" @click = "signup">
			  注册新用户
			</el-button>
		  </div> -->
  
		</div>
	  </div>
	</el-scrollbar>
</template>


 <script>
  import axios from "axios";
  import Agood from "./Agood.vue";
  import { ElMessage } from "element-plus";
  import {Edit} from "@element-plus/icons-vue";
  export default {
	components:{
		Agood,
	},
	computed: {
	  Edit() {
		return Edit
	  }
	},
	data() {
	return {
      cards: [
        { title: 'Card 1', description: 'This is the first card.' },
        { title: 'Card 2', description: 'This is the second card.' },
        { title: 'Card 3', description: 'This is the third card.' },
        { title: 'Card 4', description: 'This is the fourth card.' },
      ],
    };
	},
	methods: {
	  signup(){
		window.location.href = "/login/signup";
	  },
	  handle() {
		axios
		  .post("http://127.0.0.1:8000/user/sign_in/", { // 后端URL
			user_name: this.account,
			password: this.password,
		  })
		  .then((response) => {
			window.location.href =
			  "/online_user?user_id=" + response.data.user_id;//到online_user.html
		  })
		  .catch((error) => {
			ElMessage.error(error.response.data.error);
		  });
	  },
	},
	mounted() {
	},
  };
  </script>
  
  <style scoped>
  .loginBox {
	height: 300px;
	width: 400px;
	margin-top: 40px;
	margin-left: 27.5px;
	margin-right: 10px;
	padding: 7.5px;
	padding-right: 10px;
	padding-top: 15px;
	box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
	text-align: center;
  }
  </style>
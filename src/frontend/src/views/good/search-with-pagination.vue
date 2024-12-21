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
	  <el-button :icon="Search" @click = "find">
      <button>Search</button>
	  </el-button>
	  <div style="width: 90%; margin: 0 auto; padding-top: 5vh">
		<div class="goodBox">
			<Agood
			v-for="(card, index) in cards"
			:key="index"
			:title="card.title"
			:description="card.description"
			/>	
		</div>
	  </div>
	</el-scrollbar>
</template>


 <script>
  import axios from "axios";
  import Agood from "./Agood.vue";
  import { ElMessage } from "element-plus";
  import {Search} from "@element-plus/icons-vue";
  export default {
	components:{
		Agood,
	},
	computed: {
	  Search() {
		return Search
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
	  find(){
		window.location.href = "/good/search-with-pagination";
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
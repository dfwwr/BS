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
	  <div class="top-right">
		<el-button :icon="Search" @click = "find">
		<button>Search</button>
		</el-button></div>

	  <div style="width: 90%; margin: 0 auto; padding-top: 5vh">
		<div class="card-container">
			<el-card
			v-for="item in currentItems"
			:key="item.id"
			:class="card"
			:name="item.name"
			:description="item.description"
			/>	
			
		</div>
		<el-pagination
		@current-change="handleCurrentChange"
		:current-page="currentPage"
		:page-size="pageSize"
		:total="totalItems"
		layout="total, prev, pager, next, jumper"
    	/>
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
	setup(){
	const currentPage = ref(1);
    const pageSize = ref(5);
    const totalItems = computed(() => items.value.length);

    // 当前页商品
    const currentItems = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      return items.value.slice(start, start + pageSize.value);
    });
	const handleCurrentChange = (page) => {
      currentPage.value = page;
	};
	return {
      currentItems,
      currentPage,
      pageSize,
      totalItems,
      handleCurrentChange
    };
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
  .top-right {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
 }
  </style>
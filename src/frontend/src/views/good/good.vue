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
		<div id="gooddisplay">
		<ul>
			<Agood
			v-for="(card, index) in cards"
			:key="index"
			:title="card.good_name"
			:description="card.description"
			/>	
		</ul>
		<button @click="prevPage" :disabled="currentPage === 1">上一页</button>
		<button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
		<span>当前页: {{ currentPage }} / {{ totalPages }}</span>
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
	created() {
    this.fetchGoods();
  	},
	computed: {
		totalPages() {
            return Math.ceil(this.cards.length / this.pageSize);
        },
        paginatedData() {
            const start = (this.currentPage - 1) * this.pageSize;
            return this.cards.slice(start, start + this.pageSize);
        },
	  Search() {
		return Search
	  }
	},

	data() {
	return {
		currentPage: 1,
		pageSize: 10,
      	cards: []
    };
	},

	methods: {
		nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
		find(){
			window.location.href = "/good/search-with-pagination";
		},

		fetchGoods() {
			axios
			.get("http://127.0.0.1:8000/api/Goods")
			.then((response) => {
				console.log('Response:', response); // 打印整个响应
				this.cards =response.data;
			})
			.catch((error) => {
				console.error('Error:', error); // 打印错误信息
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
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
		我的收藏
	  </div>

		<div class="dashboard-container">
			<div class="product-filter">
			<el-row type="flex" align="middle" style="margin-bottom: 10px">
				<el-col :span="10" :xs="20">
					<el-checkbox-group v-model="selectedPlatforms">
						<el-checkbox label="京东">京东</el-checkbox>
						<el-checkbox label="唯品会">唯品会</el-checkbox>
						<el-checkbox label="苏宁">苏宁易购</el-checkbox>
					</el-checkbox-group>
				</el-col>
				<el-col :span="2" :xs="24">
				<el-input v-model="priceRange[0]" placeholder="最低价" @input="handlePriceChange"></el-input>
				</el-col>
				<el-col :span="1" :xs="24" style="text-align: center;">
				——
				</el-col>
				<el-col :span="2" :xs="24">
				<el-input v-model="priceRange[1]" placeholder="最高价" @input="handlePriceChange"></el-input>
				</el-col>

				<el-col :span="2" :xs="24" style="margin-left: 36px; margin-right: 20px">
				<el-button type="primary" @click="sortProducts('low')">价格从低到高</el-button>
				</el-col>
				<el-col :span="2" :xs="24">
				<el-button type="primary" @click="sortProducts('high')" style="margin-left: 20px">价格从高到低</el-button>
				</el-col>
				</el-row>
			</div> 
		<div class="products">
			<el-row>
			<el-col :span="6" :xs="24" v-for="product in filteredProducts" :key="product.title" style="display: flex; justify-content: center;">
				<el-card class="product-card">
				<img :src="product['good_pic']" class="product-image" alt="商品图片">
				<div style="padding: 14px;">
					<div class="price" style="color: brown; font-weight: bold; font-size: 26px;">
					￥{{ product['price'] }}
					</div>
					<div class="title" style="font-weight: bold; margin-top: 10px; font-size: 14px;
					line-clamp: 2;overflow: hidden;
					display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 2;  ">
					{{ product['good_description'] }}
					</div>
					<div class="shop" style="color: #666666; margin-top: 10px; font-size: 14px;">
              			{{ product['good_platform'] }}
            		</div>	
					<div class="card-footer" style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
					<a :href="product['good_link']" target="_blank" class="product-detail-link">查看详情</a>		
					<el-button
						type="info"
						size="small"
						@click="showPriceHistory(product)"
						style="margin-left: 10px;">
						历史价格</el-button>
					<el-button
					type="primary"
					size="small"
					@click="unstarProduct(product)"
					>取消收藏</el-button>
					</div>
					<el-button
						type="info"
						size="small"
						@click="showPriceHistorytest(product)"
						style="margin-left: 10px;">
						历史价格测试</el-button>
				</div>
				</el-card>
			</el-col>
			</el-row>
			<el-dialog
				v-model=priceHistoryVisible
				title="历史价格走势"
				width="80%">
				<div class="price-chart" style="height: 600px; padding: 20px;">
					<v-chart :option="chartOption" autoresize />
				</div>
			</el-dialog>
			<button @click="prevPage" :disabled="currentPage === 1">上一页</button>
			<button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
			<span>当前页: {{ currentPage }} / {{ totalPages }}</span>
			</div>
		</div>
	  
	</el-scrollbar>
</template>


 <script>
  import axios from "axios";
  import { ElMessage } from "element-plus";
  import { StarFilled } from '@element-plus/icons-vue'
  import VChart from 'vue-echarts'
  import ECharts from 'vue-echarts'
  import { use } from 'echarts/core'
  import { CanvasRenderer } from 'echarts/renderers'
  import { LineChart } from 'echarts/charts'
  import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'
  
  export default {
	components:{
		StarFilled,
		VChart
	},
	created() {
		this.user_id = this.$store.state.user.id;
    	this.fetchGoods();
  	},
	computed: {
		totalPages() {
            return Math.ceil(this.products.length / this.pageSize);
        },
        paginatedData() {
            const start = (this.currentPage - 1) * this.pageSize;
            return this.products.slice(start, start + this.pageSize);
        },
		filteredProducts() {
		// 将 priceRange 中的空字符串转换为 null 以表示无限制
		// 如果没有选择任何平台，则默认选择所有平台
		const selectedPlatforms = this.selectedPlatforms.length === 0 ? this.allPlatforms : this.selectedPlatforms
		// 将 priceRange 中的空字符串转换为 null 以表示无限制
		const [minPrice, maxPrice] = this.priceRange.map(range => range === '' ? null : parseFloat(range))
		// 根据平台、价格范围和排序类型过滤和排序产品
		let filteredAndSortedProducts = this.products.filter(product =>
			selectedPlatforms.includes(product['good_platform']) &&
			(minPrice === null || product['price'] >= minPrice) &&
			(maxPrice === null || product['price'] <= maxPrice)
		)
		if (this.sortType === 'low') {
			filteredAndSortedProducts = filteredAndSortedProducts.sort((a, b) => a.price - b.price)
		} else if (this.sortType === 'high') {
			filteredAndSortedProducts = filteredAndSortedProducts.sort((a, b) => b.price - a.price)
		}
		const start = (this.currentPage - 1) * this.pageSize;
		const end = this.currentPage * this.pageSize;
		return filteredAndSortedProducts.slice(start, end)
		},
	},
	data() {
	return {
		search_goods:false,
		productName: '',
		user_id:null,
		currentPage: 1,
		pageSize: 8,
      	cards: [],
		products: [],
		sortType: '',
		priceRange: ['', ''],
		allPlatforms: ['京东', '唯品会', '苏宁'],
		selectedPlatforms: [],
		loading: null,
		priceHistoryVisible: false,
		chartOption: {
			title: {text: '商品价格走势'},
			tooltip: {trigger: 'axis',
			formatter: function(params) {
			const date = new Date(params[0].value[0]);
			return `${date.toLocaleDateString()}<br/>价格：¥${params[0].value[1]}`;
			} },
			xAxis: {
			type: 'time',
			name: '日期'
			},
			yAxis: {
			type: 'value',
			name: '价格(元)'
			},
			series: [{
				data: [],
				type: 'line',
				smooth: true
				}]
		},
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


		handlePriceChange() {
			const [minPrice, maxPrice] = this.priceRange.map(range => range === '' ? null : parseFloat(range));
			if (minPrice !== null && maxPrice !== null && minPrice > maxPrice) {
				this.priceRange[0] = this.priceRange[1];
			}
		},
		sortProducts(type) {
			this.sortType = type;
		},
		fetchGoods() {
			if(this.search_goods==false){
			axios.post("http://127.0.0.1:8000/star/Goods/",{
				user_id:this.user_id
			})
			.then((response) => {
				this.products=response.data;
				console.log(this.products);
			})
			.catch((error) => {
				ElMessage.error(error.response.data.error);
			});
			}
		},
		unstarProduct(product){
			axios.post("http://127.0.0.1:8000/good/unstar_product/", {
				user_id: this.user_id,
				good_id: product['good_id']
			})
			.then((response) => {
				this.$message.success('取消收藏成功');
				this.fetchGoods();
			})
			.catch((error) => {
				ElMessage.error(error.response.data.error);
			});
		},
		showPriceHistory(product) {

			axios.post("http://127.0.0.1:8000/good/price_history/", {
				good_id: product['good_id']
			})
			.then((response) => {
				this.priceHistoryVisible = true;
				console.log(this.priceHistoryVisible)
				console.log(response.data)
				this.chartOption.series[0].data = response.data.logs.map(log => [
					new Date(log.timestamp),
					log.prise
				]);
				console.log(this.chartOption.series[0].data)
			})
			.catch((error) => {
				ElMessage.error(error.response.data.error);
			});
		},
		showPriceHistorytest(product){
			axios.post("http://127.0.0.1:8000/good/price_history_test/", {
				good_id: product['good_id']
			})
			.then((response) => {
				this.priceHistoryVisible = true;
				console.log(this.priceHistoryVisible)
				console.log(response.data)
				this.chartOption.series[0].data = response.data.logs.map(log => [
					new Date(log.timestamp),
					log.prise
				]);
				console.log(this.chartOption.series[0].data)
			})
			.catch((error) => {
				ElMessage.error(error.response.data.error);
			});
		}
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
.dashboard-container {

.search-box {
  margin: 50px auto 40px;
  position: relative;
  width: 400px; /* 增加搜索框的宽度 */
  height: 50px; /* 增加搜索框的高度 */
  background-color: #ffffff;
  border-radius: 25px; /* 圆润的搜索框 */
  overflow: hidden;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影以增加立体感 */

  input {
	width: 100%;
	height: 100%;
	padding: 0 20px;
	border: none;
	background: none;
	outline: none;
	color: #333;
	font-size: 16px;
  }

  .search-btn {
	position: absolute;
	right: 0;
	top: 2px;
	width: 50px;
	height: 50px;
	background: none;
	border: none;
	cursor: pointer;
	outline: none;

	img {
	  width: 80%;
	  height: auto;
	}
  }
}
.is-favorite {
  background-color: #F56C6C !important;
  color: white !important;
}
.product-card {
  margin-bottom: 10px;
  height: 500px;
  width: 300px;
}

.product-image {
  width: 100%; /* 使图片宽度适应容器 */
  height: 200px; /* 设置图片高度 */
  object-fit: cover; /* 裁剪图片以适应容器 */
}

.product-detail-link {
  display: inline-block;
  margin-top: 10px;
  font-size: 14px;
  color: #9ea0a1; /* Element UI 主题色 */
  text-decoration: none; /* 去除下划线 */
}

.product-detail-link:hover {
  text-decoration: underline; /* 鼠标悬浮时添加下划线 */
}

:deep(.el-dialog) {
  width: 25%;
}

:deep(.el-dialog .el-dialog__body) {
  flex: 1;
  overflow: auto;
  padding-top: 0;
  padding-bottom: 0;
}

.product-filter {
  margin-left: 36px;
  margin-bottom: 30px;
}

 .page-button1 {
	  display: inline-block;
	  border-radius: 20px;
	  background-color: #72d1b2;
	  border: none;
	  color: #ffff;
	  text-align: center;
	  font-size: 16px;
	  font-weight: 400;
	  padding: 12px;
	  width: 120px;
	  transition: all 0.5s;
	  cursor: pointer;
	  margin: 5px;
	  vertical-align: middle;
	}

	.page-button1 span {
	  cursor: pointer;
	  display: inline-block;
	  position: relative;
	  transition: 0.5s;
	}

	.page-button1 span::before {
	  content: "<<";
	  position: absolute;
	  opacity: 0;
	  top: 0;
	  left: -20px;
	  transition: 0.5s;
	}

	.page-button1:hover span {
	  padding-left: 30px;
	}

	.page-button1:hover span::before {
	  opacity: 1;
	  left: 0;
	}

 .page-button2 {
	  display: inline-block;
	  border-radius: 20px;
	  background-color: #a181d5;
	  border: none;
	  color: #ffff;
	  text-align: center;
	  font-size: 16px;
	  font-weight: 400;
	  padding: 12px;
	  width: 120px;
	  transition: all 0.5s;
	  cursor: pointer;
	  margin: 5px;
	  vertical-align: middle;
	}

	.page-button2 span {
	  cursor: pointer;
	  display: inline-block;
	  position: relative;
	  transition: 0.5s;
	}

	.page-button2 span::after {
	  content: ">>";
	  position: absolute;
	  opacity: 0;
	  top: 0;
	  right: -20px;
	  transition: 0.5s;
	}

	.page-button2:hover span {
	  padding-right: 30px;
	}

	.page-button2:hover span::after {
	  opacity: 1;
	  right: 0;
	}

}

.price-chart {
    width: 100%;
    min-height: 600px;
    background: #fff;
    border-radius: 4px;
}

:deep(.el-dialog) {
    min-width: 1000px;  /* 设置更大的最小宽度 */
}

:deep(.el-dialog__body) {
    padding: 20px;  /* 增加内边距 */
}
</style>
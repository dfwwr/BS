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

		<div class="dashboard-container">
			<div class="search-box">
			<form @submit.prevent="checkLogin">
				<input
					type="text"
					placeholder="探索你心仪的商品吧..."
					v-model="productName"
				/>
				<button class="search-btn" type="button" @click="checkLogin()">
				<img src="./search.png" alt="搜索">
				</button>
			</form>
			</div>
		

		<el-dialog v-model="jd_card" center>
			<template #header>
				<div>
				使用微信扫一扫登录
				</div>
				<div>
					请确保您的微信账号与京东账号已绑定！
				</div>
				<div style="font-weight: bold; font-size: 22px; margin-top: 16px;">
				「 京东 」
				</div>
			</template>
			<img 
				:src="jd_qrcode === '' ? defaultQrcode : jd_qrcode" 
				alt="微信扫码登录" 
				style="clear: both; display: block; margin: auto; width: 50%;"
			>
			<template #footer>
				<div style="font-size: 13px">
				（取消扫码则跳过京东的搜索结果）
				</div>
			</template>
		</el-dialog>

		<el-dialog v-model="vph_card" center>
			<template #header>
				<div>
				使用微信扫一扫登录
				</div>
				<div>
					请确保您的微信账号与唯品会账号已绑定！
				</div>
				<div style="font-weight: bold; font-size: 22px; margin-top: 16px;">
				「 唯品会 」
				</div>
			</template>
			<img 
				:src="vph_qrcode === '' ? defaultQrcode : vph_qrcode" 
				alt="微信扫码登录" 
				style="clear: both; display: block; margin: auto; width: 50%;"
			>
			<template #footer>
				<div style="font-size: 13px">
				（取消扫码则跳过唯品会的搜索结果）
				</div>
			</template>
		</el-dialog>

		<el-dialog v-model="sn_card" center>
			<template #header>
				<div>
				使用微信扫一扫登录
				</div>
				<div>
					请确保您的微信账号与苏宁易购账号已绑定！
				</div>
				<div style="font-weight: bold; font-size: 22px; margin-top: 16px;">
				「 苏宁易购 」
				</div>
			</template>
			<img 
				:src="sn_qrcode === '' ? defaultQrcode : sn_qrcode" 
				alt="微信扫码登录" 
				style="clear: both; display: block; margin: auto; width: 50%;"
			>
			<template #footer>
				<div style="font-size: 13px">
				（取消扫码则跳过苏宁易购的搜索结果）
				</div>
			</template>
		</el-dialog>

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
				<img :src="product.img" class="product-image" alt="商品图片">
				<div style="padding: 14px;">
					<div class="price" style="color: brown; font-weight: bold; font-size: 26px;">
					￥{{ product.price }}
					</div>
					<div class="title" style="font-weight: bold; margin-top: 10px; font-size: 14px;
					line-clamp: 4;overflow: hidden;
					display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 4;  ">
					{{ product.title }}
					</div>
					<div class="sales" style="color: #666666; margin-top: 10px; font-size: 14px;">
					已售 <span style="color: #1482f0">{{ product.sales }}</span>
					</div>
					<div class="shop" style="color: #666666; margin-top: 10px; font-size: 14px;">
						{{ product.platform }}
					</div>
					<div class="card-footer" style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
					<a :href="product.link" target="_blank" class="product-detail-link">查看详情</a>		
      				<el-button
        			type="primary"
					circle size="small"
					@click="star_product(product)"
					>
					<el-icon :size="20"><StarFilled /></el-icon>
					</el-button>
					</div>
				</div>
				</el-card>
			</el-col>
			</el-row>
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
  import defaultQrcode from './qrcode.png'  
  export default {
	components:{
		StarFilled,
	},
	created() {
    //this.fetchGoods();
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
		console.log(this.products)
		let filteredAndSortedProducts = this.products.filter(product =>
			selectedPlatforms.includes(product.platform) &&
			(minPrice === null || product.price >= minPrice) &&
			(maxPrice === null || product.price <= maxPrice)
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
	watch: {
		jd_card(newVal, oldVal) {
			if (newVal === false && oldVal === true) {
				this.jd_qrcode = ''
				if(this.jd_timer) {
					clearTimeout(this.jd_timer)
					this.jd_timer = null
				}
				if (this.vph_check === 'false') {
					this.vph_card = true
					this.vphLogin()
				}
				else if (this.sn_check === 'false') {
					this.sn_card = true
					this.snLogin()
				}
				else {
					this.loading.close()
					this.loading = this.$loading({fullscreen: false, text: '稍等一下下，马上就加载出来啦...', target: '.products'})
					this.good_search()
				}
			}
		},
		vph_card(newVal, oldVal) {
			if (newVal === false && oldVal === true) {
				this.vph_qrcode = ''
				if(this.vph_timer) {
				clearTimeout(this.vph_timer)
				this.vph_timer = null
				}
				if (this.sn_check === 'false') {
				this.sn_card = true
				this.snLogin()
				}
				else {
				this.loading.close()
				this.loading = this.$loading({fullscreen: false, text: '稍等一下下，马上就加载出来啦...', target: '.products'})
				this.good_search()
				}
			}
		},
		sn_card(newVal, oldVal) {
			if (newVal === false && oldVal === true) {
				this.sn_qrcode = ''
				if(this.sn_timer) {
				clearTimeout(this.sn_timer)
				this.sn_timer = null
				}
				this.loading.close()
				this.loading = this.$loading({fullscreen: false, text: '稍等一下下，马上就加载出来啦...', target: '.products'})
				this.good_search()
			}
		},
	},
	data() {
	return {
		defaultQrcode:defaultQrcode,
		productName: '',
		user_id:null,
		currentPage: 1,
		pageSize: 8,
      	cards: [],
		products: [],
		sortType: '',
		priceRange: ['', ''],
		allPlatforms: ['京东', '唯品会', '苏宁'],
		selectedPlatforms: ['京东', '唯品会', '苏宁'],
		loading: null,
		jd_timer: null,
		jd_qrcode: '',
		jd_card: false,
		jd_check: '',

		vph_timer: null,
		vph_qrcode: '',
		vph_card: false,
		vph_check: '',

		sn_timer: null,
		sn_qrcode: '',
		sn_card: false,
		sn_check: '',
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

		checkLogin() {
      	this.loading = this.$loading({fullscreen: false, text: '稍等一下下，马上就加载出来啦...', target: '.products'})
      	axios.post('http://127.0.0.1:8000/search/checklogin/', {
			method: 'check',
			user_id: this.user_id,
      		}).then(response => {
			console.log(response.data)
			let res = response.data
			this.jd_check = res.jd
			this.vph_check = res.vph
			this.sn_check = res.sn
			const needsJD = this.selectedPlatforms.includes("京东");
			const needsVPH = this.selectedPlatforms.includes("唯品会");
			const needsSN = this.selectedPlatforms.includes("苏宁");
			if (this.jd_check === 'false' && needsJD) {
			this.loading.close()
			this.jd_card = true
			this.jdLogin()
			}
			else if (this.vph_check === 'false' && needsVPH) {
			this.loading.close()
			this.vph_card = true
			this.vphLogin()
			}
			else if (this.sn_check === 'false' && needsSN) {
			this.loading.close()
			this.sn_card = true
			this.snLogin()
			}
			else
			{
				this.good_search()
			}
      		})
			.catch((error) => {
				console.log(error)
				ElMessage.error(error.response.data.error);
			});
    	},

		jdLogin() {
		axios.post('http://127.0.0.1:8000/search/login/', {
			method: 'jd_login',
			user_id:this.user_id,
      	}).then(response => {
			console.log(response.data)
			console.log(this.jd_card)
        let res = response.data
        if (res.message === '待扫码') {
			if (this.jd_card === false)
				return
			this.jd_qrcode = res.qrcode
			this.jd_card = true

			if(this.jd_qrcode === ''){
				this.$message.error('无法登录，请检查您的账号')
				this.jd_card=false;
				return 
			}
          	this.jd_timer = setTimeout(this.jdLogin, 8000)
        }
        else if (res.message === '扫码成功') {
          this.jd_card = false
          this.$message.success('扫码成功')
        }
        else {
          this.$message.error('扫码失败，请重新搜索')
          console.log(res.message)
        } })
		},

		vphLogin() {
		axios.post('http://127.0.0.1:8000/search/login/', {
			method: 'vph_login',
			user_id:this.user_id,
		}).then(response => {
			let res = response.data
			if (res.message === '待扫码') {
				if (this.vph_card === false)
				return
				this.vph_qrcode = res.qrcode
				this.vph_card = true
				if(this.vph_qrcode === ''){
					this.$message.error('无法登录，请检查您的账号')
					this.vph_card=false;
					return 
				}
				this.vph_timer = setTimeout(this.vphLogin, 8000)
			}
			else if (res.message === '扫码成功') {
			this.vph_card = false
			this.$message.success('扫码成功')
			}
			else {
			this.$message.error('扫码失败，请重新搜索')
			console.log(res.message)
			}
		})
		},

		snLogin() {
		axios.post('http://127.0.0.1:8000/search/login/', {
			method: 'sn_login',
			user_id:this.user_id,
		}).then(response => {
			let res = response.data
			if (res.message === '待扫码') {
			if (this.sn_card === false)
				return
			this.sn_qrcode = res.qrcode
			this.sn_card = true
			if(this.sn_qrcode === ''){
				this.$message.error('无法登录，请检查您的账号')
				return 
			}
			this.sn_timer = setTimeout(this.snLogin, 8000)
			}
			else if (res.message === '扫码成功') {
			this.sn_card = false
			this.$message.success('扫码成功')
			}
			else {
			this.$message.error('扫码失败，请重新搜索')
			console.log(res.message)
			}
		})
		},
		good_search() {
		this.$message.success('查询中，请稍等')
		Promise.allSettled([
			axios.post('http://127.0.0.1:8000/search/goodsearch/', 
			{method: 'jd_search', user_id:this.user_id, name:this.productName}),
			axios.post('http://127.0.0.1:8000/search/goodsearch/', 
			{method: 'vph_search', user_id:this.user_id, name:this.productName}),
			axios.post('http://127.0.0.1:8000/search/goodsearch/',
			 {method: 'sn_search', user_id:this.user_id, name:this.productName}),
		]).then(responses => {
			this.good_search=true
			this.products = []
			responses.forEach(response => {
			if (response.status === 'fulfilled') {
				let res = response.value.data
				if (res.message === 'success')
				this.products = this.products.concat(res.products)
			}
			else
				console.log(response.reason)
			})
			this.loading.close()
			this.$message.success('成功查询')
		}).catch(error => {
			console.log('Error fetching data:', error)
			this.$message.error('查询失败，请重试')
		})
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
		star_product(product){
			axios.post("http://127.0.0.1:8000/good/star_product/", { // 后端URL
			user_id: this.user_id,
			product:product,
			productname:this.productName
			})
			.then((response) => {
				this.$message.success('成功收藏')
			})
			.catch((error) => {
			console.log(error)
			ElMessage.error(error.response.data.error);
			});
		}
	},
	mounted() {
		this.user_id = this.$store.state.user.id
		console.log(this.user_id)
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
  </style>
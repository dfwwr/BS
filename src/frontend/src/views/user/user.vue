<template>
  <el-scrollbar height="100%" style="width: 100%; height: 100%">
    <div class="user-container">
      <el-card class="user-card">
        <template #header>
          <div class="card-header">
            <span class="title">个人信息</span>
            <el-button 
              type="primary" 
              @click="editMode = true" 
              v-if="!editMode"
            >
              修改信息
            </el-button>
          </div>
        </template>

        <!-- 展示模式 -->
        <div v-if="!editMode" class="info-display">
          <div class="info-item">
            <span class="label">用户名：</span>
            <span>{{ userInfo.username }}</span>
          </div>
          <div class="info-item">
            <span class="label">邮箱：</span>
            <span>{{ userInfo.email }}</span>
          </div>
          <div class="info-item">
            <span class="label">手机号：</span>
            <span>{{ userInfo.phone || '未设置' }}</span>
          </div>
        </div>

        <!-- 编辑模式 -->
        <el-form 
          v-else 
          :model="editForm" 
          :rules="rules"
          ref="formRef"
          label-width="80px"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="editForm.username" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="editForm.email" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="editForm.phone" />
          </el-form-item>
          <el-form-item label="新密码" prop="newPassword">
            <el-input 
              v-model="editForm.newPassword" 
              type="password" 
              show-password
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">保存</el-button>
            <el-button @click="cancelEdit">取消</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 统计信息卡片 -->
      <el-card class="stats-card">
        <template #header>
          <div class="card-header">
            <span class="title">收藏统计</span>
          </div>
        </template>
        <div class="stats-content">
          <div class="stat-item">
            <div class="stat-value">{{ stats.totalGoods }}</div>
            <div class="stat-label">收藏商品</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.jdGoods }}</div>
            <div class="stat-label">京东商品</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.vphGoods }}</div>
            <div class="stat-label">唯品会商品</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ stats.snGoods }}</div>
            <div class="stat-label">苏宁商品</div>
          </div>
        </div>
      </el-card>
    </div>
  </el-scrollbar>
</template>

<script>
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  data() {
    return {
      editMode: false,
	  user_id:this.$store.state.user.id,
      userInfo: {
        username: '',
        email: '',
        phone: ''
      },
      editForm: {
        username: '',
        email: '',
        phone: '',
        newPassword: ''
      },
      stats: {
        totalGoods: 0,
        jdGoods: 0,
        vphGoods: 0,
        snGoods: 0
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        phone: [
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        newPassword: [
          { min: 6, message: '密码长度至少为 6 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.fetchUserInfo()
    this.fetchUserStats()
  },
  methods: {
    fetchUserInfo() {
      axios.post('http://127.0.0.1:8000/user/info/', {
        user_id: this.user_id
      })
      .then(response => {
        this.userInfo = response.data
        this.editForm = { ...this.userInfo, newPassword: '' }
      })
      .catch(error => {
        ElMessage.error('获取用户信息失败')
        console.error(error)
      })
    },
    fetchUserStats() {
      axios.post('http://127.0.0.1:8000/user/stats/', {
        user_id:this.user_id
      })
      .then(response => {
        this.stats = response.data
      })
      .catch(error => {
        ElMessage.error('获取统计信息失败')
        console.error(error)
      })
    },
    submitForm() {
	 axios.post('http://127.0.0.1:8000/user/edit/', {
        user_id:this.user_id,
		username:this.editForm.username,
		email:this.editForm.email,
		phone:this.editForm.phone,
		newPassword:this.editForm.newPassword
      })
      .then(response => {
        ElMessage.success('更新成功')
      })
      .catch(error => {
        ElMessage.error('获取统计信息失败')
        console.error(error)
      })
    },
    cancelEdit() {
      this.editMode = false
      this.editForm = { ...this.userInfo, newPassword: '' }
    }
  }
}
</script>

<style scoped>
.user-container {
  padding: 20px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.user-card {
  flex: 1;
  min-width: 300px;
  max-width: 600px;
}

.stats-card {
  flex: 1;
  min-width: 300px;
  max-width: 600px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: bold;
}

.info-display {
  padding: 20px 0;
}

.info-item {
  margin-bottom: 15px;
  font-size: 16px;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  color: #606266;
}

.stats-content {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px 0;
}

.stat-item {
  text-align: center;
  padding: 15px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  margin-top: 8px;
  color: #606266;
}
</style>

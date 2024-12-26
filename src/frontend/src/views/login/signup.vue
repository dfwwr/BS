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
      用户
    </div>
    <div style="width: 45%; margin: 0 auto; padding-top: 5vh">
      <div class="goodBox">
        <!-- 卡片标题 -->

        <!-- 卡片内容 -->
        <div style="margin-left: 10px; height: 180px ;text-align: start; font-size: 16px;">
          <div style=" height: 40px;margin: auto;display: flex;align-items: center;justify-content: center">
            <div style ="font-size: 1.5rem;font-weight: bolder; margin-top: 20px;text-align: center">
              用 户 注 册
            </div>
          </div>
          <el-divider/>
          <el-form :model="form" :rules="rules" label-position="right" label-width="100px" style=" font-weight: bolder; font-size: 10px">
            <el-form-item label="用户名" prop="username" style = "margin-top: 5px;">
              <el-input v-model="form.username" style="width: 12.5vw; margin-left: 1rem" maxlength="18" clearable/>
            </el-form-item>
            <el-form-item label="密码" prop="password" style = "margin-top: 5px;">
              <el-input v-model="form.password" style="width: 12.5vw; margin-left: 1rem" type="password" maxlength="20" clearable/>
            </el-form-item>
            <el-form-item label="电话号码" prop="phone" style = "margin-top: 5px;">
              <el-input v-model="form.phone" style="width: 12.5vw; margin-left: 1rem" maxlength="18" clearable/>
            </el-form-item>
            <el-form-item label="邮箱" prop="email" style = "margin-top: 5px;">
              <el-input v-model="form.email" style="width: 12.5vw; margin-left: 1rem" maxlength="25" clearable/>
            </el-form-item>

            <!-- 卡片操作 -->
            <div style="margin-top: 30px; display:flex;justify-content: center">
              <el-button type="primary"  @click="handle()">
                注册
              </el-button>
              <el-button  @click = "login">
                返回
              </el-button>
            </div>
          </el-form>
        </div>
      </div>
    </div>
  </el-scrollbar>
</template>
  <script>
import axios from "axios";
import { ElMessage } from "element-plus";
export default {
  data() {
    const validateUsername = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('用户名长度必须大于6个字符'))
      } else {
        callback()
      }
    }

    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码长度必须大于6个字符'))
      } else {
        callback()
      }
    }

    return {
      form: {
        username: "",
        password: "",
        email: "",
        phone: "",
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { validator: validateUsername, trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { validator: validatePassword, trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
      }
    }
  },
  methods: {
    login() {
      window.location.href = "/login/user";
    },
    handle() {
      axios
        .post("http://127.0.0.1:8000/user/sign_up/", {
          username: this.form.username,
          password: this.form.password,
          email: this.form.email,
          phone: this.form.phone,
        })
        .then((response) => {
          console.log(response)
          ElMessage.success(response.data.message);
          setTimeout(() => {
            window.location.href = "/login/user"; // 跳转到指定页面
          }, 1000);
        })
        .catch((error) => {
          ElMessage.error(error.response.data.error);
        });
    }
  }
};
</script>
  
  <style scoped>
.loginBox {
  height: 400px;
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
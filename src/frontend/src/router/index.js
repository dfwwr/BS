import { createRouter, createWebHistory} from 'vue-router'
//import 自定义组件名 from 路径
import User from "@/views/login/user.vue";
import Signup from "@/views/login/signup.vue";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/login/user'
        },
        {
            path: '/login/user',
            component: User,
        },
        {
            path: '/login/signup',
            component: Signup,
        },
        {
            path: '/star/user',
            component: () => import('../views/star/user.vue')
		},
		{
            path: '/good',
            component: () => import('../views/good/good.vue')
        },
        {
            path: '/user',
            component: () => import('../views/user/user.vue')
        }
    ]
})

export default router
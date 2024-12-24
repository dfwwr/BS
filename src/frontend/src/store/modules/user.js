// import { getToken } from '@/utils/auth'
const getDefaultState = () => {
	return {
	//   token: getToken(),
	  id: localStorage.getItem('user_id') || null,
	  name: '',
	  avatar: '',
	  email: ''
	}
  }
const state = getDefaultState()

const mutations = {
	RESET_STATE: (state) => {
	  Object.assign(state, getDefaultState())
	},
	// SET_TOKEN: (state, token) => {
	//   state.token = token
	// },
	SET_NAME: (state, name) => {
	  state.name = name
	},
	SET_AVATAR: (state, avatar) => {
	  state.avatar = avatar
	},
	SET_EMAIL: (state, email) => {
	  state.email = email
	},
	SET_ID: (state, id) => {
	  state.id = id
	  localStorage.setItem('user_id', id)
	}
}

export default {
	namespaced: true,
	state,
	mutations
}
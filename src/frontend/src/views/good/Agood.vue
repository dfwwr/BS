<template>
	<div class="Agood">
	  <h3 center>{{ title }}</h3>
	  <p>{{ description }}</p>
	  <button @click="handleClick">Click Me</button>
	</div>
  </template>
  
  <script>
  export default {
	props: {
	  title: String,
	  description: String,
	},
	methods: {
	  handleClick() {
		alert(`You clicked on ${this.title}`);
	  },
	},
  };
  </script>
  
  <style scoped>
  .Agood {
	text-align: center;
	height: 400px;
  width: 400px;
  margin-top: 40px;
  margin-left: 27.5px;
  margin-right: 10px;
  padding: 7.5px;
  padding-right: 10px;
  padding-top: 15px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  }
  </style>
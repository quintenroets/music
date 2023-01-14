<template>
  <div class="loader" v-if="enabled"></div>
</template>

<script>
export default {
  name: "Spinner",
  props: {
    enabled: Boolean,
  },
};
</script>

<style scoped>
.loader {
  position: relative;
  display: inline-block;
  margin-left: 20px;
  border: 10px solid #3a3a3a; /* Light grey */
  border-top: 10px solid #cacaca; /* Black */
  border-radius: 50%;
  width: 25px;
  height: 25px;
  top: 15px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>

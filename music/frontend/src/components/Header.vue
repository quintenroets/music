<template>
  <title>{{ title }}</title>
  <div
    style="
      position: absolute;
      color: white;
      background-color: black;
      top: 0;
      left: 0;
      width: 100%;
      height: 55px;
      padding: 0;
      display: flex;
      line-height: 55px;
    "
  >
    <div
      style="
        position: absolute;
        left: 40%;
        display: flex;
        justify-content: space-between;
        width: 20%;
      "
    >
      <div>
        <div @click="$emit('artistclick', '')" style="cursor: pointer">
          <div style="font-size: 18px">{{ title }}</div>
        </div>
      </div>
      <div>
        <div @click="$emit('songsclick', '')" style="cursor: pointer">
          <div style="font-size: 18px">Songs</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: {
    title: String,
    seasonTitle: String,
    episodeTitle: String,
  },
  watch: {
    title: {
      immediate: true,
      handler() {
        document.title = this.title;
      },
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>

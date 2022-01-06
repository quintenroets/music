<template>
  <div style="display: inline-block">
    <button>
      <h2>{{ this.episode.name }}</h2>
      <div style="height: 100px">{{ this.episode.summary }}</div>
      <img :src="this.episode.image" border="1px" />
      <p style="float: left">{{ this.episode.number }}</p>
    </button>
  </div>
</template>

<script lang="ts">
export default {
  name: "EpisodeTile",
  props: {
    episode: {},
  },
};
</script>

<style scoped>
button {
  background-color: #3a3a3a;
  height: 500px;
  width: 500px;

  border-radius: 5px;
  border: none;
  padding: 10px;
  margin: 10px 10px;
}

img {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}
</style>

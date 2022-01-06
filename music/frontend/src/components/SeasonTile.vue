<template>
  <div style="display: inline-block">
    <button>
      <h2>{{ this.season.name }}</h2>
      <img :src="season.imageUrl" border="1px" />
      <p style="float: right">{{ this.season.episodes.length }} episodes</p>
    </button>
  </div>
</template>

<script lang="ts">
export default {
  name: "SeasonTile",
  props: {
    season: {},
  },
};
</script>

<style scoped>
button {
  background-color: #3a3a3a;
  height: 400px;
  width: 300px;

  border-radius: 5px;
  border: none;
  padding: 0px 10px;
  margin: 10px 10px;
}

img {
  max-width: 100%;
  max-height: 100%;
  height: 300px;
  width: 300px;
  object-fit: contain;
}
</style>

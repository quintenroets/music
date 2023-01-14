<template>
  <div style="display: inline-block" ref="tile">
    <button>
      <div>
        <p style="float: left">{{ this.episode.name }}</p>
        <p style="float: right">{{ this.episode.number }}</p>
      </div>
      <img :src="this.episode.image" border="1px" />
    </button>
  </div>
</template>

<script lang="ts">
export default {
  name: "SmallEpisodeTile",
  props: {
    episode: {},
    episodecheckpoint: {},
  },
  mounted() {
    let previous = this.episodecheckpoint - 1;
    if (previous < 1) {
      previous = 1;
    }
    if (this.episode.number == previous) {
      this.$refs.tile.scrollIntoView();
    }
  },
};
</script>

<style scoped>
button {
  background-color: #3a3a3a;
  height: 220px;
  width: 290px;

  border-radius: 5px;
  border: none;
  padding: 10px;
  margin: 10px 0px;
}

img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>

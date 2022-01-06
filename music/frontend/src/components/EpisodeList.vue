<template>
  <div>
    <EpisodeTile
      @click="$emit('episodecheckpoint', episode.number)"
      v-for="episode in this.episodes"
      :key="episode.number"
      v-bind:episode="episode"
    ></EpisodeTile>
  </div>
</template>

<script>
import EpisodeTile from "./EpisodeTile";

export default {
  name: "EpisodeList",
  props: {
    episodes: {},
  },
  components: {
    EpisodeTile,
  },
};
</script>

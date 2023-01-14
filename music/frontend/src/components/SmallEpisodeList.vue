<template>
  <div>
    <SmallEpisodeTile
      @click="$emit('episodecheckpoint', episode.number)"
      v-for="episode in this.episodes"
      :key="episode.number"
      v-bind:episode="episode"
      v-bind:episodecheckpoint="episodecheckpointvalue"
    ></SmallEpisodeTile>
  </div>
</template>

<script>
import SmallEpisodeTile from "./SmallEpisodeTile";

export default {
  name: "SmallEpisodeList",
  props: {
    episodes: {},
    episodecheckpointvalue: {},
  },
  components: {
    SmallEpisodeTile,
  },
};
</script>

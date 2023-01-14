<template>
  <div>
    <SeasonList
      @seasoncheckpoint="onSeason"
      v-bind:seasons="serie.seasons"
      v-bind:seriename="serie.name"
      v-bind:config="serie.config"
      v-if="!this.checkpoint.season || this.checkpoint.season == 0"
    />
    <EpisodeList
      @episodecheckpoint="onEpisode"
      v-bind:episodes="serie.seasons[this.checkpoint.season - 1].episodes"
      v-else-if="!this.checkpoint.episode || this.checkpoint.episode == 0"
    />
    <Episode
      @close="onClose"
      @episodecheckpoint="onEpisode"
      v-bind:episode="
        serie.seasons[this.checkpoint.season - 1].episodes[
          this.checkpoint.episode - 1
        ]
      "
      v-bind:episodes="serie.seasons[this.checkpoint.season - 1].episodes"
      v-bind:checkpoint="checkpoint"
      v-bind:autopause="serie.config.autopause"
      :key="checkpoint"
      v-else
    />
  </div>
</template>

<script lang="ts">
import SeasonList from "./SeasonList.vue";
import EpisodeList from "./EpisodeList.vue";
import MusicService from "../services/MusicService.ts";
import Episode from "./Episode.vue";

export default {
  name: "Serie",
  props: {
    serie: {},
    checkpoint: {},
  },
  methods: {
    onSeason: function (number) {
      MusicService.setSeason(this.serie.name, number).then(() =>
        this.$emit("reload")
      );
    },
    onEpisode: function (number) {
      MusicService.setEpisode(this.serie.name, number).then(() => {
        this.$emit("reload");
      });
    },
    onClose: function (position, duration) {
      MusicService.onClose(this.serie.name, position, duration);
    },
  },
  components: {
    Episode,
    SeasonList,
    EpisodeList,
  },
};
</script>

<style scoped>
button {
  background-color: #3a3a3a;
  height: 400px;
  width: 3s00px;

  border-radius: 5px;
  border: none;
  padding: 10px;
  margin: 40px 2px;
}

img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>

<template>
  <button v-on:click="onSelect">
    <div
      class="hiddenscrollbar"
      style="display: inline-block; overflow: auto; height: 40px"
    >
      <img
        style="float: left; margin-right: 10px"
        @click="onShow"
        width="30"
        height="30"
        src="@/assets/logo.png"
      />
      <b style="font-size: 30px">{{ this.artist.name }}</b>
      <img
        width="20"
        height="20"
        src="@/assets/checkmark.png"
        style="margin-left: 20px"
        v-if="this.artist.added"
      />
    </div>
    <div style="display: flex">
      <div style="float: left">
        <img :src="artist.images[0].url" height="250" border="1px" />
      </div>

      <div
        class="hiddenscrollbar"
        style="height: 250px; overflow: auto; text-align: left"
      >
        <spinner v-bind:enabled="selected"></spinner>
        <img
          width="40"
          height="20"
          v-if="finished"
          src="@/assets/checkmark.png"
        />
        <p style="font-size: small; margin: 10px">
          Popularity: {{ this.artist.popularity }} %
        </p>
        <p
          style="font-size: small; margin: 10px"
          v-for="genre in this.artist.genres"
          :key="genre"
          v-bind:genre="genre"
        >
          {{ genre }}
        </p>
      </div>
    </div>
  </button>
</template>

<script>
import Spinner from "./Spinner.vue";
import MusicService from "../services/MusicService.ts";

export default {
  name: "NewArtistTile",
  props: {
    artist: {},
  },
  data() {
    return {
      selected: false,
      finished: false,
    };
  },
  methods: {
    onSelect: function () {
      this.selected = true;
      MusicService.addArtist(this.artist.id, this.artist.name).then(() => {
        this.selected = false;
        this.finished = true;
        this.$emit("clicked", this.artist.id);
      });
    },
    onShow: function (e) {
      e.stopImmediatePropagation(); // don't add artist yet
      let url = "https://open.spotify.com/artist/" + this.artist.id;
      let tab = window.open(url, "_blank");
      tab.focus();
    },
  },
  components: {
    Spinner,
  },
};
</script>

<style scoped>
button {
  background-color: #3a3a3a;
  height: 340px;
  width: 400px;

  border-radius: 5px;
  border: none;
  padding: 10px;
  margin: 15px 15px;
}

img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.hiddenscrollbar::-webkit-scrollbar {
  width: 10px;
  height: 10px;
  background-color: rgba(160, 160, 160, 0.25);
  border: 2px solid transparent;
  border-radius: 10px;
  background-clip: padding-box;
  float: right;
}

.hiddenscrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(200, 200, 200, 0.5);

  border: 2px solid transparent;
  border-radius: 10px;
  background-clip: padding-box;
  float: right;
}
</style>

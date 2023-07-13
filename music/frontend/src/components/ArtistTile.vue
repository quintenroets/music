<template>
  <div class="pseudobutton" v-on:click="onSelect">
    <div
      class="hiddenscrollbar"
      style="
        display: flex;
        overflow: auto;
        height: 40px;
        justify-content: center;
      "
    >
      <img
        style="float: left; margin-right: 10px"
        width="30"
        height="30"
        v-if="favorite"
        src="@/assets/favorite.png"
        alt="favorite-indicator"
      />
      <img
        style="float: left; margin-right: 10px"
        @click="onShow"
        width="30"
        height="30"
        src="@/assets/logo.png"
        alt="spotify logo"
      />
      <b style="font-size: 30px">{{ artist.name }}</b>
    </div>
    <div style="display: flex">
      <div style="float: left">
        <img :src="artist.images[0].url" height="250" alt="artist" />
      </div>

      <div
        class="hiddenscrollbar"
        style="height: 250px; overflow: auto; text-align: left"
      >
        <spinner v-bind:enabled="selected"></spinner>
        <p style="font-size: small; margin: 10px">
          Popularity: {{ artist.popularity }} %
        </p>
        <p
          style="font-size: small; margin: 10px"
          v-for="genre in artist.genres"
          :key="genre"
        >
          {{ genre }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import Spinner from "./Spinner.vue";
import MusicService from "../services/MusicService.ts";

export default {
  name: "ArtistTile",
  props: {
    artist: {},
  },
  data() {
    return {
      selected: false,
      favorite: this.artist.type === "favorite",
    };
  },
  methods: {
    onSelect: function () {
      this.selected = true;
      MusicService.ChangeArtist(this.artist.id).then(() => {
        this.selected = false;
        this.favorite = !this.favorite;
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
.pseudobutton {
  background-color: #3a3a3a;
  height: 340px;
  width: 400px;

  border-radius: 5px;
  border: none;
  padding: 10px;
  margin: 15px 15px;
  cursor: pointer;
  display: inline-block;
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

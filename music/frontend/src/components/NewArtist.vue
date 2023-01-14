<template>
  <div>
    <h3>{{ message }}</h3>
    <br /><br />
    <div>
      <input
        @input="onInput(input)"
        autofocus
        v-model="input"
        v-on:keydown.enter="onInput(input)"
      />
      <spinner v-bind:enabled="waiting"></spinner>
    </div>
    <div>
      <NewArtistTile
        @clicked="onArtist"
        v-for="artist in this.newartists"
        :key="artist.id"
        v-bind:artist="artist"
      />
    </div>
    <spinner v-bind:enabled="waitingrecommendations"></spinner>
    <NewArtistTile
      @clicked="onArtist"
      v-for="artist in this.recommendedartists"
      :key="artist.id"
      v-bind:artist="artist"
    />
  </div>
</template>

<script>
import NewArtistTile from "./NewArtistTile.vue";
import Spinner from "./Spinner.vue";
import MusicService from "../services/MusicService.ts";

export default {
  name: "NewArtist",
  data: function () {
    return {
      message: "Search new artist",
      input: "",
      waiting: false,
      newartists: [],
      recommendedartists: [],
      waitingrecommendations: true,
    };
  },
  components: {
    Spinner,
    NewArtistTile,
  },
  methods: {
    onInput: function (input) {
      if (input === "") {
        this.newartists = [];
        this.message = "Search new artist";
      } else {
        this.waiting = true;
        this.message = "Searching for " + input;
        this.newartists = [];
        MusicService.getNewArtist(input).then((response) => {
          this.newartists = response;
          this.waiting = false;
          this.message = "Select an option";
        });
      }
    },
    onArtist: function (id) {
      this.$emit("clicked", id);
    },
    setRecommendations: function () {
      MusicService.getRecommendedArtists().then((response) => {
        this.recommendedartists = response;
        this.waitingrecommendations = false;
      });
    },
  },
  mounted() {
    this.setRecommendations();
  },
};
</script>

<style scoped>
input {
  background-color: gray;
  height: 50px;
  width: 400px;
}
</style>

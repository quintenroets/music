<template>
  <div>
    <h3>{{ message }}</h3>
    <br /><br />
    <div>
      <input @input="onInput(input)" autofocus v-model="input" v-on:keydown.enter="onInput(input)" />
      <spinner v-bind:enabled="waiting"></spinner>
    </div>
    <div>
          <NewSongTile
            @clicked="onSong"
            v-for="song in this.newsongs"
            :key="song.id"
            v-bind:song="song"
          />
      </div>
  </div>
</template>

<script lang="ts">
import NewSongTile from "./NewSongTile.vue";
import Spinner from "./Spinner.vue";
import MusicService from "../services/MusicService.ts";

export default {
  name: "NewArtist",
  data: function () {
    return {
      message: "Search new song",
      input: "",
      waiting: false,
      newsongs: {},
    };
  },
  components: {
    Spinner,
    NewSongTile,
  },
  methods: {
    onInput: function (input) {
      if (input === "") {
        this.newsongs = [];
        this.message = "Search new songs";
      } else {
        this.waiting = true;
        this.message = "Searching for " + input;
        this.newsongs = [];
        MusicService.getNewSongs(input).then((response) => {
          this.newsongs = response;
          this.waiting = false;
          this.message = "Select an option";
        });
      }
    },
    onSong: function (id) {
      this.$emit("clicked", id);
    }
  }
};
</script>

<style scoped>
input {
  background-color: gray;
  height: 50px;
  width: 400px;
}
</style>

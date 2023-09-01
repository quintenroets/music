<template>
  <div class="flex justify-center items-center">
    <div class="vl-parent flex-col justify-center">
      <loading
        :active="waiting"
        :is-full-page="false"
        color="white"
        :height="100"
        :width="100"
      />
      <div />
    </div>
    <div class="inline-block overflow-y-auto">
      <ArtistTile
        v-for="artist in this.artists"
        :key="artist.id"
        v-bind:artist="artist"
      />
    </div>
  </div>
</template>

<script>
import ArtistTile from "../components/tiles/ArtistTile";
import MusicService from "@/services/MusicService.ts";
import Loading from "vue-loading-overlay";

export default {
  name: "ArtistList",

  data: function () {
    return {
      artists: [],
      waiting: true,
    };
  },
  components: {
    Loading,
    ArtistTile,
  },
  methods: {
    setArtists: function () {
      MusicService.getArtists().then((response) => {
        this.artists = response;
        this.waiting = false;
      });
    },
  },
  mounted() {
    this.setArtists();
  },
};
</script>

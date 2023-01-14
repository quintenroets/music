<template>
  <div>
    <ArtistTile
      v-for="artist in this.artists"
      :key="artist.id"
      v-bind:artist="artist"
    />
  </div>
</template>

<script>
import ArtistTile from "./ArtistTile";
import MusicService from "@/services/MusicService.ts";

export default {
  name: "ArtistList",

  data: function () {
    return {
      artists: [],
    };
  },
  components: {
    ArtistTile,
  },
  methods: {
    setArtists: function () {
      MusicService.getArtists().then((response) => {
        this.artists = response;
      });
    },
  },
  mounted() {
    this.setArtists();
  },
};
</script>

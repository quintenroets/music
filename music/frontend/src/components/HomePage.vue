<template>
  <Header
    @artistclick="
      showNew = !showNew;
      showSongs = false;
    "
    @songsclick="showSongs = !showSongs"
    v-bind:title="title"
  />
  <NewArtist v-if="showNew && !showSongs" />
  <ArtistList v-else-if="!showSongs" />
  <NewSong v-else />
</template>

<script>
import Header from "./Header";
import ArtistList from "./ArtistList";
import NewArtist from "./NewArtist";
import NewSong from "./NewSong";

export default {
  name: "HomePage",
  components: {
    Header,
    ArtistList,
    NewArtist,
    NewSong,
  },
  data() {
    return {
      title: "Artists",
      showNew: true,
      showSongs: true,
    };
  },
};
</script>

<style>
body {
  background-color: #181818;
  color: white;
}
</style>

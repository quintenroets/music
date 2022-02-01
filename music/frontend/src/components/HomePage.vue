<template>
  <Header @artistclick="showNew = !showNew; showSongs=false" @songsclick="showSongs = !showSongs" v-bind:title="title"/>
  <NewArtist v-if="showNew && !showSongs"/>
  <ArtistList v-else-if="!showSongs"/>
  <NewSong v-else/>
</template>

<script>
import Header from "./Header";
import ArtistList from "./ArtistList";
import NewArtist from "./NewArtist"
import NewSong from "./NewSong"

export default {
  name: "HomePage",
  components: {
    Header,
    ArtistList,
    NewArtist,
    NewSong
  },
  data() {
    return {
      title: "Artists",
      showNew: true,
      showSongs: true
    };
  }
};
</script>

<style>
@import "https://codex.nflxext.com/%5E3.0.0/truthBundle/webui/0.0.1-shakti-css-v1b8c742f/css/css/less%7Csignup%7CnmContent%7CnmTitle%7CnmTitle.less/1/tDvL3ruF9CIK/none/true/none";
</style>

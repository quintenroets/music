<template>
  <Header @artistclick="showNew = !showNew" v-bind:title="title"/>
  <NewArtist v-if="showNew"/>
  <ArtistList v-else/>
</template>

<script>
import Header from "./Header";
import ArtistList from "./ArtistList";
import NewArtist from "./NewArtist"

export default {
  name: "HomePage",
  components: {
    Header,
    ArtistList,
    NewArtist
  },
  data() {
    return {
      title: "Artists",
      showNew: false
    };
  }
};
</script>

<style>
@import "https://codex.nflxext.com/%5E3.0.0/truthBundle/webui/0.0.1-shakti-css-v1b8c742f/css/css/less%7Csignup%7CnmContent%7CnmTitle%7CnmTitle.less/1/tDvL3ruF9CIK/none/true/none";
</style>

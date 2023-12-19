<template>
  <NewItemTile
    v-bind:name="artist.name"
    v-bind:id="artist.id"
    v-bind:popularity="artist.popularity"
    v-bind:images="artist.images"
    v-bind:genres="artist.genres"
    v-bind:selected="selected"
    type="artist"
    @click="onSelect"
  >
    <template #top-right-image>
      <img src="@/assets/favorite.png" alt="checkmark" v-if="favorite" />
    </template>
  </NewItemTile>
</template>

<script>
import MusicService from "../../services/MusicService.ts";
import NewItemTile from "./NewItemTile.vue";

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
  },
  components: {
    NewItemTile,
  },
};
</script>

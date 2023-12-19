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
      <img
        src="@/assets/checkmark.png"
        alt="checkmark"
        v-if="artist.added || finished"
      />
    </template>
  </NewItemTile>
</template>

<script>
import MusicService from "../../services/MusicService.ts";
import NewItemTile from "./NewItemTile.vue";

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
      });
    },
  },
  components: {
    NewItemTile,
  },
};
</script>

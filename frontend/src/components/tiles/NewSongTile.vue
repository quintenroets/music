<template>
  <NewItemTile
    v-bind:name="song.name"
    v-bind:id="song.id"
    v-bind:popularity="song.popularity"
    v-bind:images="song.album.images"
    v-bind:genres="song.artists.map((artist) => artist.name)"
    v-bind:selected="selected"
    type="track"
    @click="onSelect"
  >
    <template #top-right-image>
      <img
        src="@/assets/checkmark.png"
        alt="checkmark"
        v-if="finished || this.song.downloaded"
      />
    </template>
  </NewItemTile>
</template>

<script>
import MusicService from "../../services/MusicService.ts";
import NewItemTile from "./NewItemTile.vue";

export default {
  name: "NewSongTile",
  props: {
    song: {},
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
      MusicService.addSong(this.song.id).then(() => {
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

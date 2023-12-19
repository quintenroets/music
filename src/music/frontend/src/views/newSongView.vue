<template>
  <NewItemView
    :fetch-function="MusicService().getNewSongs"
    :fetch-recommendations-function="MusicService().getRecommendedSongs"
    item-name="song"
    :item-component="NewSongTile"
  />
</template>

<script>
import MusicService from "../services/MusicService.ts";
import NewItemView from "@/components/NewItemView.vue";
import NewSongTile from "@/components/tiles/NewSongTile.vue";

export default {
  name: "NewArtist",
  computed: {
    NewSongTile() {
      return NewSongTile;
    },
  },
  components: {
    NewItemView,
  },
  methods: {
    MusicService() {
      return MusicService;
    },
  },
};
</script>

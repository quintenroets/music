<template>
  <NewItemView
    :fetch-function="MusicService().getNewArtist"
    :fetch-recommendations-function="MusicService().getRecommendedArtists"
    item-name="artist"
    :item-component="NewArtistTile"
  />
</template>

<script>
import MusicService from "../services/MusicService.ts";
import NewItemView from "@/components/NewItemView.vue";
import NewArtistTile from "@/components/tiles/NewArtistTile.vue";

export default {
  name: "NewArtist",
  computed: {
    NewArtistTile() {
      return NewArtistTile;
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

<template>
  <div class="tile h-64 w-96 max-w-full vl-parent relative">
    <div
      class="absolute inset-0 flex justify-center items-center"
      v-if="selected"
    >
      <loading
        :active="selected"
        :is-full-page="false"
        color="white"
        :width="100"
        :height="100"
      />
    </div>
    <div>
      <div class="flex h-14 overflow-y-auto">
        <div class="image-wrapper aspect-1 h-10 p-1" @click.stop="onShow">
          <img
            src="@/assets/logo.png"
            alt="spotify logo"
            width="40"
            height="40"
          />
        </div>
        <div class="flex justify-center flex-grow p-1">
          <p class="text-sm font-bold">{{ name }}</p>
        </div>
        <div class="image-wrapper aspect-1 h-10 p-1">
          <slot name="top-right-image"></slot>
        </div>
      </div>
      <div class="flex overflow-y-auto h-40">
        <div class="image-wrapper aspect-1 p-1">
          <img
            :src="image"
            :alt="this.type + ' image'"
            width="160"
            height="160"
          />
        </div>
        <div class="overflow-y-auto text-left p-2 flex-grow">
          <p class="font-xs">Popularity: {{ popularity }}%</p>
          <div
            class="font-xs overflow-y-auto"
            v-for="genre in genres"
            :key="genre"
          >
            {{ genre }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Loading from "vue-loading-overlay";

export default {
  name: "NewItemTile",
  props: {
    id: {},
    name: {},
    images: {},
    popularity: {},
    genres: {},
    selected: {},
    type: {},
  },
  methods: {
    onShow: function () {
      let url = "https://open.spotify.com/" + this.type + "/" + this.id;
      let tab = window.open(url, "_blank");
      tab.focus();
    },
  },
  computed: {
    image() {
      for (let i = this.images.length - 1; i >= 0; i--) {
        if (this.images[i].height >= 160) {
          // smallest one that is large enough
          // h-40 = 40 * 0.25 rem = 10rem = 10 * 16 px = 160px
          return this.images[i].url;
        }
      }
      return null;
    },
  },
  components: {
    Loading,
  },
};
</script>

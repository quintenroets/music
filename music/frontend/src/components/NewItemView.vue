<template>
  <div class="flex flex-col">
    <h3 class="mt-4 mb-8">{{ message }}</h3>
    <div class="flex justify-center">
      <div class="flex justify-center relative px-16 w-full max-w-lg">
        <input
          class="bg-gray-300 text-black h-12 w-full text-center px-10 rounded"
          @input="onInput(input)"
          autofocus
          v-model="input"
          v-on:keydown.enter="onInput(input)"
        />
      </div>
      <div class="flex justify-center items-center">
        <div class="absolute -translate-x-6 vl-parent flex-col justify-center">
          <loading
            :active="waiting"
            :is-full-page="false"
            color="white"
            :height="30"
          />
          <div />
        </div>
      </div>
    </div>
    <div class="w-full flex justify-center mt-10">
      <div class="vl-parent w-full h-full flex justify-center">
        <loading
          class="mt-10"
          :active="waitingrecommendations"
          :is-full-page="false"
          color="white"
        />
        <div class="inline-block overflow-y-auto">
          <component
            @clicked="onClick"
            v-for="item in newItems"
            :key="item.id"
            :is="itemComponent"
            v-bind="{ [itemName]: item }"
          />
          <component
            @clicked="onClick"
            v-for="item in recommendedItems"
            :key="item.id"
            :is="itemComponent"
            v-bind="{ [itemName]: item }"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MusicService from "../services/MusicService.ts";
import Loading from "vue-loading-overlay";

export default {
  name: "NewItemView",
  data: function () {
    return {
      message: "Search new " + this.itemName,
      input: "",
      waiting: false,
      newItems: {},
      recommendedItems: {},
      waitingrecommendations: true,
    };
  },
  components: {
    Loading,
  },

  props: {
    itemName: {
      type: String,
      required: true,
    },
    itemComponent: {
      type: Object,
      required: true,
    },
    fetchFunction: {
      type: Function,
      required: true,
    },
    fetchRecommendationsFunction: {
      type: Function,
      required: true,
    },
  },
  methods: {
    onInput: function (input) {
      if (input === "") {
        this.newsongs = [];
      } else {
        this.waiting = true;
        this.newsongs = [];
        MusicService.getNewArtist(input).then((response) => {
          this.newItems = response;
          this.waiting = false;
        });
      }
    },
    onClick: function (id) {
      this.$emit("clicked", id);
    },
    setRecommendations: function () {
      this.fetchRecommendationsFunction().then((response) => {
        this.recommendedItems = response;
        this.waitingrecommendations = false;
      });
    },
  },
  mounted() {
    this.setRecommendations();
  },
};
</script>

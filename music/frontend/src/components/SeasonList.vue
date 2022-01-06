<template>
  <div style="display: flex">
      <div style="margin: auto">
          <SeasonTile
            @click="$emit('seasoncheckpoint', season.number)"
            v-for="season in this.seasons"
            :key="season.number"
            v-bind:season="season"
          />
      </div>
    <settings
        @delete="$emit('seasoncheckpoint', 0)"
        v-bind:seriename="seriename"
        v-bind:config="config"
    />
  </div>
</template>

<script>
import SeasonTile from "./SeasonTile";
import Settings from "./Settings"

export default {
  name: "SeasonList",
  props: {
    seasons: {},
    seriename: {},
    config: {}
  },
  data: function () {
    return {
      showSettings: false
    };
  },
  components: {
    SeasonTile,
    Settings
  },
  methods: {
    onSettings: function(){
      this.showSettings = true;
    }
  }
};
</script>

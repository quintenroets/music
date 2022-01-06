<template>
  <div>
      <img @click="showSettings=!showSettings" src="@/assets/settings.png">

      <div v-if="showSettings" style="width: 200px">
            <!-- Rounded switch -->
            <h3>Download Episodes</h3>
            <label class="switch">
              <input style="width: 200px" type="checkbox" v-model="download">
              <span class="slider round"></span>
            </label>

            <h3>Autopause timer</h3>
            <input type="number" style="background-color: gray; width: 150px; border-radius: 10px; border: 2px" v-model="autopause">

            <button
                @click="onDelete"
                style="margin-top: 30px; width: 150px; height: 60px; border-radius: 15px; border: 2px"
            >
              <h3>Delete serie</h3>
            </button>
      </div>
  </div>
</template>

<script>
import MusicService from "@/services/MusicService.ts"

export default {
  name: "SeasonList",
  props: {
    seriename: {},
    config: {}
  },
  data: function () {
    return {
      showSettings: false,
      download: this.config.download,
      autopause: this.config.autopause? this.config.autopause: 0,
    };
  },
  methods: {
    onDelete: function(){
      if (confirm("Are you sure you want to delete this serie?")){
        MusicService.deleteSerie(this.seriename).then(
            () => {
              this.$emit("delete");
            }
        )
      }
    }
  },
    watch: {
      download: {
        immediate: true,
        handler() {
          MusicService.setConfig(this.seriename, "download", this.download);
        },
      },
      autopause: {
        immediate: true,
        handler() {
          MusicService.setConfig(this.seriename, "autopause", this.autopause);
        },
      }
    }
};
</script>

<style scoped>

img{
  width: 48px;
  height: 48px;
  margin-right: 40px;
  margin-top: 10px;
  cursor:pointer;
}

/* The switch - the box around the slider */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

button{
  background-color: gray;
}

</style>

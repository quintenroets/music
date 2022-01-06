<template>
  <div style="display: flex;float: right">
    <div style="float: right; margin-right: 180px">
        <h1 style="width: 900px;">{{episode.name}}</h1>
        <p></p>
        <video-player
            @close="onClose"
            @error="onError"
            v-bind:source="streamingUrl"
            v-bind:subtitles="subtitleUrl"
            v-bind:poster="episode.image"
            v-bind:checkpoint="checkpoint"
            v-bind:autopause="autopause"
        />
        <p></p>
        <p style="width: 900px; margin-top: 40px;">{{episode.summary}}</p>
    </div>
    <SmallEpisodeList
        @episodecheckpoint="onEpisode"
        class="hiddenscrollbar"
        style="width: 400px; height: 750px; overflow: scroll; overflow-x:hidden; margin-right: 10px"
        v-bind:episodes="episodes"
        v-bind:episodecheckpointvalue="episode.number">
    </SmallEpisodeList>

	</div>
</template>

<script>
import VideoPlayer from "@/components/VideoPlayer.vue";
import SmallEpisodeList from "@/components/SmallEpisodeList.vue"
import EpisodeService from "@/services/EpisodeService.ts"

export default {
	name: "Episode.vue",
  data: function () {
    return {
      streamingUrl: "",
      subtitleUrl: ""
    };
  },
	components: {
		VideoPlayer,
    SmallEpisodeList
	},
  props: {
    episode: {},
    episodes: {},
    checkpoint: {},
    autopause: {}
  },
  methods: {
    onEpisode: function (number) {
      this.$emit("episodecheckpoint", number);
    },
    setStreamingUrl: function(){
      EpisodeService.getStreamingUrl(this.episode).then(
          (response) => {this.streamingUrl = response;}
      )
    },
    setSubtitleUrl: function(){
      EpisodeService.getSubtitleUrl(this.episode).then(
          (response) => {this.subtitleUrl = process.env.VUE_APP_API_URL + response;}
      )
    },
    onClose: function (position, duration){
      this.$emit('close', position, duration);
    },
    onError: function(){
      EpisodeService.sendError(this.episode).then(
          // force reload
          () => {this.$emit("episodecheckpoint", this.checkpoint.episode);}
      )
    }
  },
    watch: {
      episode: {
        immediate: true,
        handler() {
          this.setStreamingUrl();
          this.setSubtitleUrl();
        },
      },
  }
};
</script>

<style scoped>

.hiddenscrollbar::-webkit-scrollbar {
  width: 10px;
  height: 10px;
  background-color: rgba(160,160,160,0.25);
  border: 2px solid transparent;
  border-radius: 10px;
  background-clip: padding-box;
}

.hiddenscrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(200,200,200,0.5);

  border: 2px solid transparent;
  border-radius: 10px;
  background-clip: padding-box;
}

</style>
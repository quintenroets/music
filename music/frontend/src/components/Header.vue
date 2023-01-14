<template>
  <div>
    <title>{{ title }}</title>
    <div class="basicLayout nonmemberTitle dark" lang="en-BE" dir="ltr">
      <div class="nmtitle-wrapper with-fixed-header">
        <div class="nm-content-header is-fixed" data-uia="site-header">
          <div class="nm-content-header-section nm-content-header-left">
            <div
              style="cursor: pointer"
              @click="$emit('homebutton', '')"
              class="svg-nfLogo"
              data-uia="netflix-header-svg-logo"
            ></div>
            <div class="nm-content-header-text" id="title">
              <div
                @click="$emit('artistclick', '')"
                style="display: inline-block; cursor: pointer"
              >
                <div style="font-size: 18px">&emsp;&emsp;&emsp;{{ title }}</div>
              </div>
            </div>
            <div class="nm-content-header-text" id="title">
              <div
                @click="$emit('songsclick', '')"
                style="display: inline-block; cursor: pointer"
              >
                <div style="font-size: 18px">&emsp;&emsp;&emsp; Songs</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <section
        class="nmtitle-section section-hero"
        id="section-hero"
        data-uia="section-hero"
      ></section>
    </div>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: {
    title: String,
    seasonTitle: String,
    episodeTitle: String,
  },
  watch: {
    title: {
      immediate: true,
      handler() {
        document.title = this.title;
      },
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
button.simple-button {
  /* button to prev en next episodes*/
  width: 50px;
  height: 56px;
  border-radius: 3px;
  border: none;
  background: black;
  font-size: 40px;
  color: white;
}
</style>

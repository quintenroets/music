<template>
  <div class="flex flex-col h-screen justify-start">
    <div ref="navigation" class="overflow-x-auto flex-shrink-0 bg-black">
      <div class="flex justify-center">
        <nav
          class="whitespace-nowrap flex justify-between w-full max-w-2xl p-4 text-lg"
          :style="{ 'font-size': ratio < 1 ? '13px' : '' }"
        >
          <router-link to="/">Songs</router-link>
          <router-link to="/artists">Artists</router-link>
          <router-link to="/newartists">New artists</router-link>
        </nav>
      </div>
    </div>
    <div
      class="flex flex-col w-full overflow-y-auto flex-grow p-6 hiddenscrollbar"
      :class="{ 'px-2': ratio >= 1 }"
      id="pagecontent"
    >
      <router-view
        key="$route.fullPath"
        class="flex flex-grow flex-col hiddenscrollbar"
        :class="{ 'pb-14': ratio < 1, 'overflow-y-auto': ratio >= 1 }"
      />
    </div>
  </div>
</template>
<script>
import { ref } from "vue";

export default {
  name: "RouterBar",

  setup() {
    const ratio = ref(window.innerWidth / window.innerHeight);
    return {
      ratio,
    };
  },
};
</script>

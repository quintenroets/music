<template>
  <div class="flex flex-col h-screen">
    <div class="overflow-x-auto flex-shrink-0 bg-black flex justify-center">
      <nav
        class="whitespace-nowrap flex justify-between w-full max-w-2xl p-4 text-lg"
        :style="{ 'font-size': ratio < 1 ? '13px' : '' }"
      >
        <router-link to="/">Songs</router-link>
        <router-link to="/artists">Artists</router-link>
        <router-link to="/newartists">New artists</router-link>
      </nav>
    </div>
    <router-view
      class="flex flex-col flex-grow overflow-y-auto w-full my-4"
      :class="{ 'px-2': ratio >= 1, 'pb-14': ratio < 1 }"
    >
    </router-view>
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

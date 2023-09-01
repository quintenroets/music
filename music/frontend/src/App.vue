<template>
  <HomePage class="flex-grow" />
</template>

<script>
import HomePage from "@/components/HomePage.vue";

export default {
  name: "App",
  components: {
    HomePage,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

nav a.router-link-exact-active {
  font-weight: bold;
}

h1 {
  font-weight: bold !important;
  font-size: 2em !important;
}
h3 {
  font-size: 20px !important;
  font-weight: bold !important;
}

p {
  margin-bottom: 1em !important;
  font-size: 17px !important;
}

.image-wrapper {
  border-radius: 0.25rem;
  overflow: hidden;
}

img {
  border-radius: 0.25rem;
  object-fit: contain;
}

body {
  font-family: "Times New Roman", sans-serif;
  background-color: #181818;
  color: white;
}

::-webkit-scrollbar {
  width: 10px;
  height: 10px;
  background-color: rgba(160, 160, 160, 0.25);
  border: 2px solid transparent;
  border-radius: 10px;
  background-clip: padding-box;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(200, 200, 200, 0.5);
  border: 2px solid transparent;
  border-radius: 10px;
  background-clip: padding-box;
}

.tile {
  background-color: #3a3a3a;
  display: inline-block;
  flex-direction: column;
  padding: 1rem;
  margin: 1rem;
  border-radius: 0.5rem;
  justify-content: space-around;
  overflow: hidden;
  cursor: pointer;
}
</style>

<script setup>
import { useHead } from "unhead";

useHead({
  meta: [
    {
      name: `description`,
      content: "Manage artists and songs to analyze.",
    },
  ],
  htmlAttrs: {
    lang: "en",
  },
});
</script>

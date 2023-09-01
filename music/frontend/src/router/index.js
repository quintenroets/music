import { createRouter, createWebHistory } from "vue-router";
import NewSongView from "@/views/newSongView.vue";

const routes = [
  {
    path: "/",
    name: "New Songs",
    component: NewSongView,
  },
  {
    path: "/artists",
    name: "Artists",
    component: () =>
      import(/* webpackChunkName: "artists" */ "../views/ArtistsView.vue"),
  },
  {
    path: "/newartists",
    name: "New Artists",
    component: () =>
      import(/* webpackChunkName: "newartists" */ "../views/newArtistView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  let title = to.name;
  if (title) {
    title = "Music - " + title;
  }
  document.title = title;
  next();
});

export default router;

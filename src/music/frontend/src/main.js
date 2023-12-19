import { createApp } from "vue";
import App from "./App.vue";
import { createHead } from "unhead";
import router from "./router";

import "@/assets/css/tailwind.css";

const head = createHead();
const app = createApp(App);
app.use(head);
app.use(router);
app.mount("#app");

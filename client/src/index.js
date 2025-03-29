import Home from "./components/Home.vue";
import Trainings from "./components/Trainings.vue";
import { createMemoryHistory, createRouter } from "vue-router";

export const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/trainings",
    name: "Trainings",
    component: Trainings,
  },
];

const router = createRouter({
  history: createMemoryHistory(),
  routes,
});

export default router;
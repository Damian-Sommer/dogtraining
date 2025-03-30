import Cards from "./components/Cards.vue";
import Home from "./components/Home.vue";
import Trainings from "./components/Trainings.vue";
import { createWebHistory, createRouter } from "vue-router";

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
  {
    path: "/cards",
    name: "Karten",
    component: Cards,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
import Cards from "./components/Cards.vue";
import Home from "./components/Home.vue";
import NewCard from "./components/NewCard.vue";
import Trainings from "./components/Trainings.vue";
import { createWebHistory, createRouter } from "vue-router";

export const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      nav: false,
    },
  },
  {
    path: "/trainings",
    name: "Trainings",
    component: Trainings,
    meta: {
      nav: true,
    },
  },
  {
    path: "/cards",
    name: "Karten",
    component: Cards,
    meta: {
      nav: true,
    },
  },
  {
    path: "/newCard",
    name: "Neue Karte",
    component: NewCard,
    meta: {
      nav: false,
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

import Cards from "./components/Cards.vue";
import Home from "./components/Home.vue";
import NewCard from "./components/NewCard.vue";
import NewTraining from "./components/NewTraining.vue";
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
  {
    path: "/newTraining",
    name: "Neues Training",
    component: NewTraining,
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

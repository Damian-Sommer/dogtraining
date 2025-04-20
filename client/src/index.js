import Cards from "./components/Cards.vue";
import Dogs from "./components/Dogs.vue";
import Home from "./components/Home.vue";
import NewCard from "./components/NewCard.vue";
import NewDog from "./components/NewDog.vue";
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
  {
    path: "/dogs",
    name: "Hunde",
    component: Dogs,
    meta: {
      nav: true,
    },
  },
  {
    path: "/newDog",
    name: "Hund Registrieren",
    component: NewDog,
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

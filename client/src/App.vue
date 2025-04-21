<script setup>
import { routes } from "./index.js";
</script>

<template>
  <header>
    <h1><RouterLink to="/">Dogtraining</RouterLink></h1>
  </header>
  <main>
    <aside>
      <nav>
        <ul>
          <li v-for="link in routes">
            <RouterLink
              :to="link.path"
              v-if="link.meta.nav === true"
              :key="link.path"
              >{{ link.name }}</RouterLink
            >
          </li>
        </ul>
      </nav>
      <div class="foot">
        <a id="github_logo" href="https://github.com/Damian-Sommer/dogtraining" target="_blank"><img src="../public/github.svg" alt="Github Repository"></a>
      </div>
    </aside>
    <div class="view">
      <RouterView />
    </div>
  </main>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
  watch: {
    $route: {
      immediate: true,
      handler(to, from) {
        document.title = `Dogtraining - ${to.name}`;
      },
    },
  },
});
</script>
<style scoped>
main {
  display: flex;
  width: 100%;
  height: calc(100vh - 50px);
}
header {
  display: flex;
  align-items: center;
  height: 50px;
  width: 100%;
  background-color: aquamarine;
  padding-left: 1em;
}
header h1 {
  font-size: 2em;
  color: black;
}
header a {
  color: black;
}
aside {
  display: flex;
  width: 200px;
  height: 100%;
  background-color: aqua;
  flex-direction: column;
}
nav {
  height: 80%;
  width: 100%;
}
.foot {
  height: 20%;
  display: flex;
  align-items: center;
  padding: 0 1em;
}

.foot #github_logo {
  width: 50px;
  height: 50px;
}
ul {
  color: black;
  list-style: none;
  padding: 0 1em;
  font-size: 1.25em;
  font-weight: 600;
}
nav ul a:hover {
  background-color: rgb(34, 170, 170);
}
nav ul a {
  display: block;
  padding: 0.5em;
}
.view {
  margin: 1em;
}
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>

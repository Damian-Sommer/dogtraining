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
            <RouterLink :to="link.path" v-if="link.name !== 'Home'" :key="link.path">{{ link.name }}</RouterLink>
          </li>
        </ul>
      </nav>
    </aside>
    <div class="view">
      <RouterView/>
    </div>
  </main>
</template>

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
}
nav { 
  height: 100%;
  width: 100%;
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
  padding: .5em;
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

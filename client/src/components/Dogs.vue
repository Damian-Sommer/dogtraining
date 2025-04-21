<template>
  <table id="dogTable">
    <thead>
      <tr>
        <td>Name</td>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(dog, index) in dogs" :key="dog.id">
        <td>{{ dog.name }}</td>
      </tr>
    </tbody>
  </table>
  <button @click="$router.push('/newDog')">Hund Registrieren</button>
</template>

<script>
import { defineComponent } from "vue";
import { dog_api } from "../api/index.js";
export default defineComponent({
  data() {
    return {
      dogs: [],
      interval: null,
    };
  },
  methods: {
    fetch_all_dogs() {
      dog_api.get_all().then((response) => {
        this.dogs = response;
      });
    },
  },
  created() {
    this.fetch_all_dogs();
  },
  mounted() {
    this.interval = setInterval(() => {
      this.fetch_all_dogs();
    }, 4000);
  },
  unmounted() {
    clearInterval(this.interval);
  },
});
</script>

<style scoped>
table,
th,
td {
  border: 1px solid white;
}
#dogTable {
  border-collapse: collapse;
}
thead td {
  font-weight: 700;
}
td {
  padding: 0.25em 0.75em;
}
button {
  margin: 1em 1em 1em 0;
}
</style>

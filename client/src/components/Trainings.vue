<template>
  <table id="trainingTable">
    <thead>
      <tr>
        <td>date</td>
        <td>type</td>
        <td>dog</td>
        <td>karte</td>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(training, index) in trainings" :key="index">
        <td>{{ new Date(training.timestamp).toLocaleDateString() }}</td>
        <td>{{ training.type }}</td>
        <td>{{ training.dog.name }}</td>
        <td>{{ training.card_id }}</td>
      </tr>
    </tbody>
  </table>
  <button @click="$router.push('/newTraining')">Neues Training eintragen</button>
</template>

<script>
import { defineComponent } from "vue";
import { training_api } from "../api/index.js";
export default defineComponent({
  data() {
    return {
      trainings: [],
      interval: null,
    };
  },
  methods: {
    fetch_all_trainings() {
      training_api.get_all().then((response) => {
        this.trainings = response;
      });
    }
  },
  created() {
    this.fetch_all_trainings();
  },
  mounted() {
    this.interval = setInterval(() => {
      this.fetch_all_trainings();
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
#trainingTable {
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

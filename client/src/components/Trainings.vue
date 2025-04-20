<template>
  <table id="trainingTable">
    <thead>
      <tr>
        <td>id</td>
        <td>type</td>
        <td>dog</td>
        <td>karte</td>
        <td>date</td>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(training, index) in trainings" :key="index">
        <td>{{ training.id }}</td>
        <td>{{ training.type }}</td>
        <td>{{ training.dog_id }}</td>
        <td>{{ training.card_id }}</td>
        <td>{{ new Date(training.timestamp).toLocaleDateString() }}</td>
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
    setInterval(() => {
      this.fetch_all_trainings();
    }, 4000);
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

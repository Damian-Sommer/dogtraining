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
      <tr>
        <td>1</td>
        <td>uo spaziergang</td>
        <td>vasco</td>
        <td>1</td>
        <td>29.03.2025</td>
      </tr>
    </tbody>
  </table>
  <button @click="$router.push('/newTraining')">Neues Training eintragen</button>
</template>

<script>
import { defineComponent } from "vue";
import { training_api } from "../api/index.js";
export default defineComponent({
  computed: {
    trainings() {
      setInterval(() => {
        console.log("test");
        let all_trainings = training_api.get_all();
        console.table(all_trainings);
        return all_trainings;
      }, 4000);
    }
  }
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

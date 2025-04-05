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

export default defineComponent({});
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

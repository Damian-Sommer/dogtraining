<template>
    <table id="cardTable">
      <thead>
        <tr>
          <td>id</td>
          <td>Verfügbare Trainings</td>
          <td>Besuchte Trainings</td>
          <td>Kaufdatum</td>
          <td>Kosten</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>12</td>
          <td>1</td>
          <td>29.03.2025</td>
          <td>200</td>
        </tr>
      </tbody>
    </table>
    <button @click="$router.push('/newCard')">Neue Karte</button>
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
  #cardTable {
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
  
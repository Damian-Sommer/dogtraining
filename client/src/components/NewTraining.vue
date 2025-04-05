<template>
  <form>
    <label for="slots">Verfügbare Trainings:</label><br />
    <input v-model="slots" id="slots" name="slots" /><br />
    <label for="cost">Kosten:</label><br />
    <input v-model="cost" id="cost" name="cost" /><br /><br />
    <label for="date">Datum</label><br />
    <input v-model="date" type="date" name="date" id="date" />
  </form>
  <button @click="$router.push('/trainings')">Zurück</button>
  <button @click="sendData">Eintragen</button>
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

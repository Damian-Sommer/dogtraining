<template>
  <form>
    <label for="slots">Verfügbare Trainings:</label><br />
    <input v-model="slots" id="slots" name="slots" type="number"/><br />
    <label for="cost">Kosten:</label><br />
    <input v-model="cost" id="cost" name="cost" type="number"/><br /><br />
    <label for="buyDate">Kaufdatum</label><br />
    <input v-model="buyDate" type="date" name="buyDate" id="buyDate" />
  </form>
  <button @click="$router.push('/cards')">Zurück</button>
  <button @click="sendData">Erstellen</button>
</template>

<script>
import { defineComponent } from "vue";
import { card_api } from "../api/index.js";
import router from "../index.js";

export default defineComponent({
  data() {
    return {
      slots: 12,
      cost: 200,
      buyDate: new Date().toISOString().split("T")[0],
    };
  },
  methods: {
    async send_data() {
      if (this.buyDate == null || this.buyDate === NaN || this.buyDate === "") {
        this.buyDate = new Date().toISOString().split("T")[0];
      }
      let timestamp = new Date(this.buyDate).getTime();
      await card_api.create_entry(timestamp, this.cost, this.slots);
      router.push('/cards');
    },
  },
});
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

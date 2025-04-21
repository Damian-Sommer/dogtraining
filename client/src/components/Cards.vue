<template>
  <table id="cardTable">
    <thead>
      <tr>        
        <td>Kaufdatum</td>
        <td>Verfügbare Trainings</td>
        <td>Besuchte Trainings</td>
        <td>Kosten</td>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(card, index) in cards" :key="card.id">
        <td>{{ new Date(card.timestamp).toLocaleDateString() }}</td>
        <td>{{ card.slots }}</td>
        <td>{{ card.trainings.length }}</td>
        <td>{{ card.cost }}</td>
      </tr>
    </tbody>
  </table>
  <button @click="$router.push('/newCard')">Neue Karte</button>
</template>

<script>
import { defineComponent } from "vue";
import { card_api } from "../api/index.js";
export default defineComponent({
  data() {
    return {
      cards: [],
      interval: null,
    };
  },
  methods: {
    fetch_all_cards() {
      card_api.get_all().then((response) => {
        this.cards = response;
      });
    }
  },
  created() {
    this.fetch_all_cards();
  },
  mounted() {
    this.interval = setInterval(() => {
      this.fetch_all_cards();
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

<template>
  <form>
    <h2>Trainingsart</h2>
    <div v-for="(option, index) in training_type_options" :key="index">
      <label>
        <input type="radio" :value="option" v-model="selected_training_type" />
        {{ option[0].toUpperCase() + option.slice(1) }}
      </label>
    </div>
    <h2>Hunde</h2>
    <div v-for="option in dogs" :key="option.id">
      <label>
        <input type="checkbox" :value="option.id" v-model="selected_dogs" />
        {{ option.name }}
      </label>
    </div>
    <label for="date">Datum</label><br />
    <input v-model="date" type="date" name="date" id="date" />
  </form>
  <button @click="$router.push('/trainings')">Zurück</button>
  <button @click="send_data">Eintragen</button>
</template>

<script>
import { defineComponent } from "vue";
import { training_api, dog_api } from "../api/index";
import router from "../index.js";

export default defineComponent({
  data() {
    return {
      training_type_options: null,
      selected_training_type: null,
      dogs: null,
      selected_dogs: [],
      date: new Date().toISOString().split("T")[0],
    };
  },
  methods: {
    fetch_training_types() {
      training_api.get_training_types().then((response) => {
        this.training_type_options = response;
      });
    },
    fetch_all_dogs() {
      dog_api.get_all().then((response) => {
        this.dogs = response;
      });
    },
    async send_data() {
      if (this.buyDate == null || this.buyDate === NaN || this.buyDate === "") {
        this.buyDate = new Date().toISOString().split("T")[0];
      }
      let timestamp = new Date(this.buyDate).getTime();
      await training_api.create_entry(
        timestamp,
        this.selected_training_type,
        this.selected_dogs,
      );
      router.push("/trainings");
    },
  },
  created() {
    this.fetch_training_types();
    this.fetch_all_dogs();
  },
  mounted() {
    setInterval(() => {
      this.fetch_training_types();
      this.fetch_all_dogs();
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

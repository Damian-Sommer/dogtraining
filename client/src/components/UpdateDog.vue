<template>
  <form @submit.prevent="update_data">
    <label for="name">Name</label><br />
    <input v-model="name" id="name" name="name" type="text"/><br />

    <label for="registration_time">Registrierungs Datum</label><br />
    <input
      v-model="registration_time"
      type="date"
      name="registration_time"
      id="registration_time"
    />
  </form>

  <button @click="$router.push('/dogs')">Zurück</button>
  <button @click="update_data">Speichern</button>
</template>
<script>
import { defineComponent } from "vue";
import { dog_api } from "../api/index.js";
import router from "../index.js";

export default defineComponent({
  data() {
    return {
      dog: history.state.dog,
      name: history.state.dog?.name || "",
      registration_time: history.state.dog
        ? new Date(history.state.dog.registration_time)
            .toISOString()
            .split("T")[0]
        : "",
    };
  },

  methods: {
    async update_data() {
      if (!this.name || !this.registration_time) {
        return;
      }

      const timestamp = new Date(this.registration_time).getTime();

      await dog_api.update_entry(
        this.dog.id,
        timestamp,
        this.name
      );

      router.push("/dogs");
    },
  },
});
</script>
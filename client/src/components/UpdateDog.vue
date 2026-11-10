<template>
  <div v-if="dog">
    <form @submit.prevent="update_data">
      <label for="name">Name</label><br />
      <input v-model="dog.name" id="name" name="name" type="text" /><br />

      <label for="registration_time">Registrierungs Datum</label><br />
      <input
        v-model="dog.registration_time"
        type="date"
        name="registration_time"
        id="registration_time"
      />
    </form>

    <button @click="$router.push('/dogs')">Zurück</button>
    <button @click="update_data">Speichern</button>
  </div>

  <p v-else>Hund wird geladen...</p>
</template>
<script>
import { defineComponent } from "vue";
import { dog_api } from "../api/index.js";

export default defineComponent({
  data() {
    return {
      dog: null,
    };
  },
  methods: {
    async update_data() {
      if (!this.dog.name || !this.dog.registration_time) {
        return;
      }

      const timestamp = new Date(this.dog.registration_time).getTime();

      await dog_api.update_entry(this.dog.id, timestamp, this.dog.name);

      this.$router.push("/dogs");
    },

    fetch_dog() {
      dog_api.get_by_id(this.$route.params.id).then((response) => {
        this.dog = {
          ...response,
          registration_time: new Date(response.registration_time)
            .toISOString()
            .split("T")[0],
        };
      });
    },
  },
  created() {
    this.fetch_dog();
  },
});
</script>

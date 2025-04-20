<template>
  <form>
    <label for="name">Name</label><br />
    <input v-model="name" id="name" name="name" type="text" /><br />
    <label for="registration_time">Registrierungs Datum</label><br />
    <input
      v-model="registration_time"
      type="date"
      name="registration_time"
      id="registration_time"
    />
  </form>
  <button @click="$router.push('/dogs')">Zurück</button>
  <button @click="sendData">Erstellen</button>
</template>

<script>
import { defineComponent } from "vue";
import { dog_api } from "../api/index.js";
import router from "../index.js";

export default defineComponent({
  data() {
    return {
      name: "",
      registration_time: new Date().toISOString().split("T")[0],
    };
  },
  methods: {
    async sendData() {
      if (
        this.registration_time == null ||
        this.registration_time === NaN ||
        this.registration_time === ""
      ) {
        this.registration_time = new Date().toISOString().split("T")[0];
      }
      let timestamp = new Date(this.registration_time).getTime();
      await dog_api.create_entry(timestamp, this.name);
      router.push("/dogs");
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

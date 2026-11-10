<template>
  <div class="dog-container">
    <h2>Registrierte Hunde</h2>

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Registrierungsdatum</th>
            <th>Aktionen</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="dog in dogs" :key="dog.id">
            <td>{{ dog.name }}</td>
            <td>{{ formatDate(dog.registration_time) }}</td>
            <td>
              <button class="edit-button" @click="edit_dog(dog)">
                Bearbeiten
              </button>
            </td>
          </tr>

          <tr v-if="dogs.length === 0">
            <td colspan="3" class="empty-message">Keine Hunde registriert.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <button class="add-button" @click="$router.push('/newDog')">
      + Hund registrieren
    </button>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { dog_api } from "../api/index.js";
export default defineComponent({
  data() {
    return {
      dogs: [],
      interval: null,
    };
  },
  methods: {
    formatDate(timestamp) {
      if (!timestamp) return "-";

      // Convert seconds to milliseconds if necessary
      if (typeof timestamp === "number" && timestamp < 1000000000000) {
        timestamp *= 1000;
      }

      const date = new Date(timestamp);

      if (isNaN(date.getTime())) return "-";

      return date.toLocaleDateString("de-CH", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
      });
    },
    fetch_all_dogs() {
      dog_api.get_all().then((response) => {
        this.dogs = response;
      });
    },
    edit_dog(dog) {
      this.$router.push(`/updateDog/${dog.id}`);
    },
  },
  created() {
    this.fetch_all_dogs();
  },
  mounted() {
    this.interval = setInterval(() => {
      this.fetch_all_dogs();
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
thead td {
  font-weight: 700;
}
td {
  padding: 0.25em 0.75em;
}
button {
  margin: 1em 1em 1em 0;
}

table {
  border-collapse: collapse
}
th {
  padding: 0 10px;
}
</style>

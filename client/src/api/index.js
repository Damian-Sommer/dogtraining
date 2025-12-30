class API {
  constructor(url) {
    this.url = url;

    this.headers = new Headers();
    this.headers.append("user_id", "test");

    this.requestOptions = {
      headers: this.headers,
    };
  }

  async get_by_id(id) {}

  async get_all() {}

  async create_entry() {}
}

class Card extends API {
  constructor(url) {
    super((url = url));
  }

  async get_by_id(id) {
    const response = await fetch(
      `${this.url}/cards/${id}`,
      this.requestOptions
    );
    if (!response.ok) {
      throw new Error(await response.json());
    }
  }

  async get_all() {
    const response = await fetch(`${this.url}/cards`, this.requestOptions);
    if (!response.ok) {
      throw new Error(await response.json());
    }

    return await response.json();
  }

  async create_entry(timestamp, cost, slots) {
    const response = await fetch(`${this.url}/cards`, {
      method: "POST",
      body: JSON.stringify({ timestamp: timestamp, cost: cost, slots: slots }),
      headers: this.headers,
    });
    if (!response.ok) {
      throw new Error(await response.json());
    }
  }
}

class Training extends API {
  constructor(url) {
    super((url = url));
  }

  async get_training_types() {
    const response = await fetch(
      `${this.url}/training_types`,
      this.requestOptions
    );
    if (!response.ok) {
      throw new Error(await response.json());
    }
    return await response.json();
  }

  async get_by_id(id) {
    const response = await fetch(
      `${this.url}/trainings/${id}`,
      this.requestOptions
    );
    if (!response.ok) {
      throw new Error(await response.json());
    }
  }

  async get_all() {
    const response = await fetch(`${this.url}/trainings`, this.requestOptions);
    if (!response.ok) {
      throw new Error(await response.json());
    }

    return await response.json();
  }

  async create_entry(timestamp, type, dogs) {
    const response = await fetch(`${this.url}/trainings`, {
      method: "POST",
      body: JSON.stringify({
        timestamp: timestamp,
        type: type,
        dogs: dogs,
      }),
      headers: this.headers,
    });
    if (!response.ok) {
      throw new Error(await response.json());
    }
  }
}

class Dog extends API {
  constructor(url) {
    super((url = url));
  }

  async get_by_id(id) {
    const response = await fetch(`${this.url}/dogs/${id}`, this.requestOptions);
    if (!response.ok) {
      throw new Error(await response.json());
    }
  }

  async get_all() {
    const response = await fetch(`${this.url}/dogs`, this.requestOptions);
    if (!response.ok) {
      throw new Error(await response.json());
    }

    return await response.json();
  }

  async create_entry(registration_time, name) {
    const response = await fetch(`${this.url}/dogs`, {
      method: "POST",
      body: JSON.stringify({ registration_time: registration_time, name: name }),
      headers: this.headers,
    });
    if (!response.ok) {
      throw new Error(await response.json());
    }
  }
}

var dog_api = null;
var card_api = null;
var training_api = null;

if (process.env.NODE_ENV === "development"){
  dog_api = new Dog("http://127.0.0.1:5000");
  card_api = new Card("http://127.0.0.1:5000");
  training_api = new Training("http://127.0.0.1:5000");
} else {
  const server_url = `http://${import.meta.env.VITE_SERVER_IP}:${import.meta.env.VITE_SERVER_BACKEND_PORT}`;
  dog_api = new Dog(server_url);
  card_api = new Card(server_url);
  training_api = new Training(server_url);
}

export {dog_api, card_api, training_api};


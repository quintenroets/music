import axios from "axios";

export default axios.create({
  baseURL: "http://" + window.location.hostname + ":9889",
  headers: {
    "Content-type": "application/json",
  },
});

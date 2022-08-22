import axios from "axios";

const urlServer = "http://localhost:5000"

const api = axios.create({
	baseURL: urlServer,
});

export default api;


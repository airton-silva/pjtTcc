import axios from "axios";

const urlServer = "localhost:5000"

const api = axios.create({
	baseURL: urlServer,
});

function getTargetsUp ()
{
    return api.get('/');
    
}

export default {getTargetsUp}


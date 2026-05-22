import axios from "axios";

const API_URL = "http://127.0.0.1:8000";


export async function analyzeCode(code) {

    const response = await axios.post(
        `${API_URL}/analyze`,
        {
            code
        }
    );

    return response.data;
}
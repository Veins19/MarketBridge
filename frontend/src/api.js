import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // ensure backend running here

export const runCampaign = async (query, product) => {
  const res = await axios.post(`${API_URL}/run_campaign`, { query, product });
  return res.data;
};

import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; // ensure backend running here

export const runCampaign = async (query, product) => {
  try {
    console.log('🚀 Sending request to backend:', { query, product });
    const res = await axios.post(`${API_URL}/run_campaign`, { query, product });
    
    console.log('📡 Backend response:', res.data);
    
    // Backend returns { success: true, data: {...} }
    if (res.data.success) {
      console.log('✅ Campaign data received:', res.data.data);
      return res.data.data; // Return the actual campaign results
    } else {
      throw new Error(res.data.error || 'Campaign failed');
    }
  } catch (error) {
    console.error('❌ API Error:', error);
    throw error;
  }
};

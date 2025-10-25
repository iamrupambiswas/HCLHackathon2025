import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL; // backend URL

// Get token from localStorage
const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  return { Authorization: `Bearer ${token}` };
};

// ---------------- API calls ----------------
export const createAccount = async (account_type, initial_deposit) => {
  const response = await axios.post(
    `${API_URL}/accounts/`,
    { account_type, initial_deposit }, // <-- body
    { headers: getAuthHeaders() }
  );
  return response.data;
}

export const getUserAccounts = async () => {
  const response = await axios.get(`${API_URL}/accounts/`, {
    headers: getAuthHeaders(),
  });
  return response.data;
};

export const depositMoney = async (account_id, amount) => {
  const response = await axios.post(
    `${API_URL}/accounts/deposit`,
    { account_id, amount },
    { headers: getAuthHeaders() }
  );
  return response.data;
};

export const withdrawMoney = async (account_id, amount) => {
  const response = await axios.post(
    `${API_URL}/accounts/withdraw`,
    { account_id, amount },
    { headers: getAuthHeaders() }
  );
  return response.data;
};

export const transferMoney = async (from_account_id, to_account_number, amount) => {
  const response = await axios.post(
    `${API_URL}/accounts/transfer`,
    { from_account_id, to_account_number, amount },
    { headers: getAuthHeaders() }
  );
  return response.data;
};

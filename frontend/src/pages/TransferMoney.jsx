import React, { useEffect, useState } from "react";
import { getUserAccounts, transferMoney } from "../services/accountService";
import { useNavigate } from "react-router-dom";

function TransferMoney() {
  const [accounts, setAccounts] = useState([]);
  const [fromAccountId, setFromAccountId] = useState("");
  const [toAccountNumber, setToAccountNumber] = useState("");
  const [amount, setAmount] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const data = await getUserAccounts();
        setAccounts(data);
        if (data.length > 0) setFromAccountId(data[0].id);
      } catch (err) {
        console.error("Error fetching accounts:", err);
        setError("Failed to fetch your accounts.");
      }
    };
    fetchAccounts();
  }, []);

  const handleTransfer = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!fromAccountId || !toAccountNumber || !amount) {
      setError("All fields are required.");
      return;
    }

    try {
      await transferMoney(fromAccountId, toAccountNumber, parseFloat(amount));
      setSuccess(`₹${amount} transferred successfully!`);
      setAmount("");
      setToAccountNumber("");
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Transfer failed.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <button
        onClick={() => navigate("/dashboard")}
        className="mb-6 bg-gray-300 px-4 py-2 rounded hover:bg-gray-400 transition"
      >
        ← Back to Dashboard
      </button>

      <div className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto">
        <h2 className="text-2xl font-bold mb-2 text-center text-gray-800">
          Transfer Money
        </h2>
        <p className="text-gray-500 text-center mb-6">
          Send money securely between accounts
        </p>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">
            {error}
          </div>
        )}
        {success && (
          <div className="bg-green-100 text-green-700 p-3 rounded mb-4 text-sm">
            {success}
          </div>
        )}

        <form onSubmit={handleTransfer} className="space-y-5">
          {/* From Account */}
          <div>
            <label className="block mb-1 font-medium text-gray-700">
              From Account
            </label>
            <select
              value={fromAccountId}
              onChange={(e) => setFromAccountId(e.target.value)}
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-400 outline-none"
            >
              {accounts.map((acc) => (
                <option key={acc.id} value={acc.id}>
                  {acc.account_type} — {acc.account_number} (₹
                  {acc.balance.toFixed(2)})
                </option>
              ))}
            </select>
          </div>

          {/* Receiver Account */}
          <div>
            <label className="block mb-1 font-medium text-gray-700">
              Receiver’s Account Number
            </label>
            <input
              type="text"
              value={toAccountNumber}
              onChange={(e) => setToAccountNumber(e.target.value)}
              placeholder="Enter receiver’s account number"
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-400 outline-none"
            />
          </div>

          {/* Amount */}
          <div>
            <label className="block mb-1 font-medium text-gray-700">
              Amount
            </label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="Enter amount"
              className="w-full border border-gray-300 p-2 rounded focus:ring-2 focus:ring-blue-400 outline-none"
              min="1"
              step="0.01"
            />
          </div>

          {/* Transfer Button */}
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors font-medium"
          >
            Transfer Now
          </button>
        </form>
      </div>

      {/* Show current accounts below for quick view */}
      {accounts.length > 0 && (
        <div className="mt-8 max-w-md mx-auto">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Your Accounts
          </h3>
          <div className="space-y-3">
            {accounts.map((acc) => (
              <div
                key={acc.id}
                className="bg-white p-4 rounded-lg shadow flex justify-between items-center"
              >
                <div>
                  <p className="font-semibold text-gray-800">
                    {acc.account_type}
                  </p>
                  <p className="text-sm text-gray-500">
                    Account No: {acc.account_number}
                  </p>
                </div>
                <p className="font-bold text-green-600">
                  ₹{acc.balance.toFixed(2)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default TransferMoney;

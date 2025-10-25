import React, { useState } from "react";
import { createAccount } from "../services/accountService";

export default function CreateAccount({ onAccountCreated }) {
  const [accountType, setAccountType] = useState("savings");
  const [initialBalance, setInitialBalance] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const data = await createAccount(accountType, parseFloat(initialBalance));
      setMessage("Account created successfully!");
      setInitialBalance("");
      setAccountType("savings");
      if (onAccountCreated) onAccountCreated(data); // update parent
    } catch (err) {
      setMessage("Failed to create account.");
      console.error(err);
    }
  };

  return (
    <div className="bg-white shadow-lg rounded-xl p-6 w-full">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
        Create New Account
      </h2>

      {message && (
        <div
          className={`${
            message.includes("success")
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          } p-3 rounded mb-4 text-center`}
        >
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-700 font-medium mb-1">
            Account Type
          </label>
          <select
            value={accountType}
            onChange={(e) => setAccountType(e.target.value)}
            className="w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            <option value="savings">Savings</option>
            <option value="current">Current</option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-1">
            Initial Balance
          </label>
          <input
            type="number"
            value={initialBalance}
            onChange={(e) => setInitialBalance(e.target.value)}
            placeholder="0.00"
            required
            className="w-full border px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors font-semibold"
        >
          Create Account
        </button>
      </form>
    </div>
  );
}

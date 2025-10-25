import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getUserAccounts } from "../services/accountService";
import AccountCard from "../components/AccountCard";
import CreateAccount from "../components/CreateAccount";

function Dashboard() {
  const [accounts, setAccounts] = useState([]);
  const [error, setError] = useState("");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const data = await getUserAccounts();
        setAccounts(data);
      } catch (err) {
        console.error("Error fetching accounts:", err);
        setError("Failed to fetch accounts");
      }
    };
    fetchAccounts();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
          <p className="text-gray-600">Welcome to your banking app!</p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors"
          >
            Create Account
          </button>

          <button
            onClick={() => navigate("/transfer")}
            className="bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-600 transition-colors"
          >
            Transfer Money
          </button>

          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Account List */}
      {accounts.length === 0 ? (
        <p className="text-gray-500">No accounts found.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {accounts.map((acc) => (
            <AccountCard key={acc.id} account={acc} />
          ))}
        </div>
      )}

      {/* Create Account Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md relative">
            <button
              onClick={() => setShowCreateModal(false)}
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 font-bold"
            >
              ✕
            </button>

            <CreateAccount
              onAccountCreated={(newAccount) => {
                setAccounts((prev) => [...prev, newAccount]);
                setShowCreateModal(false);
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;

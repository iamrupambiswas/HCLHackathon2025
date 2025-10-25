// components/AccountCard.jsx
import React from "react";

function AccountCard({ account }) {
  return (
    <div className="bg-white p-5 rounded-xl shadow hover:shadow-lg transition-shadow duration-300">
      <h2 className="text-xl font-semibold text-gray-800 capitalize">
        {account.account_type} Account
      </h2>
      <p className="text-gray-500 mt-1">
        <span className="font-medium">Account Number:</span> {account.account_number}
      </p>
      <p className="text-gray-700 mt-2 font-medium">
        Balance: ₹{account.balance.toFixed(2)}
      </p>
    </div>
  );
}

export default AccountCard;

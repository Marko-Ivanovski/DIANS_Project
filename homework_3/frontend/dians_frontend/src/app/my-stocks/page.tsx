'use client';

import { useState, useEffect } from "react";
import axios from "axios";

const MyStocksPage = () => {
  const [transactionType, setTransactionType] = useState("BUY");
  const [shares, setShares] = useState<any[]>([]); // For available shares to buy
  const [myShares, setMyShares] = useState<any[]>([]); // For user's shares to sell
  const [quantity, setQuantity] = useState<number | string>(""); // Quantity for transaction
  const [error, setError] = useState<string | null>(null); // Error messages

  // Fetch shares based on transaction type
  useEffect(() => {
    const fetchData = async () => {
      const accessToken = localStorage.getItem("access_token");

      if (!accessToken) {
        setError("You must be logged in to view or edit your stocks.");
        return;
      }

      try {
        const response = await axios.get(
          `http://localhost:8000/transactions/my-shares?transaction_type=${transactionType}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );

        if (transactionType === "BUY") {
          setShares(response.data);
        } else if (transactionType === "SELL") {
          setMyShares(response.data);
        }
      } catch (err) {
        setError("Error fetching data.");
        console.error(err);
      }
    };

    fetchData();
  }, [transactionType]);

  // Handle Buy/Sell Transaction
  const handleTransaction = async (selectedShare: any) => {
    if (!quantity || Number(quantity) <= 0) {
      alert("Please enter a valid quantity.");
      return;
    }

    const availableQuantity =
      transactionType === "BUY"
        ? selectedShare.quantity_of_shares
        : selectedShare.quantity;

    if (Number(quantity) > availableQuantity) {
      alert("Insufficient shares available for this transaction.");
      return;
    }

    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
      alert("You must be logged in to perform this action.");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:8000/transactions/my-shares",
        {
          share_id: selectedShare.id,
          quantity,
          transaction_type: transactionType,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      alert(response.data.message);

      if (transactionType === "BUY") {
        const remainingAvailableQuantity = selectedShare.quantity_of_shares - Number(quantity);

        if (remainingAvailableQuantity > 0) {
          setShares((prevShares) =>
            prevShares.map((share) =>
              share.id === selectedShare.id
                ? { ...share, quantity_of_shares: remainingAvailableQuantity }
                : share
            )
          );
        } else {
          setShares((prevShares) =>
            prevShares.filter((share) => share.id !== selectedShare.id)
          );
        }

        setMyShares((prevMyShares) => [
          ...prevMyShares,
          {
            ...selectedShare,
            quantity: Number(quantity),
            price_of_last_transaction: selectedShare.price_of_last_transaction,
            purchase_date: selectedShare.date,
          },
        ]);
      }

      if (transactionType === "SELL") {
        const remainingPurchasedQuantity = selectedShare.quantity - Number(quantity);

        if (remainingPurchasedQuantity > 0) {
          setMyShares((prevMyShares) =>
            prevMyShares.map((share) =>
              share.id === selectedShare.id
                ? { ...share, quantity: remainingPurchasedQuantity }
                : share
            )
          );
        } else {
          setMyShares((prevMyShares) =>
            prevMyShares.filter((share) => share.id !== selectedShare.id)
          );
        }

        setShares((prevShares) => [
          ...prevShares,
          {
            ...selectedShare,
            quantity_of_shares: Number(quantity),
            price_of_last_transaction: selectedShare.price_of_last_transaction,
            date: response.data.sell_date, // Display today's sell date
          },
        ]);
      }

      setQuantity(""); // Clear the quantity input
    } catch (error) {
      console.error("Error handling transaction:", error);
      alert("Failed to complete the transaction.");
    }
  };

  return (
  <div className="p-6 bg-gray-100 min-h-screen">
    <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">My Stocks</h1>

    {error && <p className="text-red-500 text-center mb-4">{error}</p>}

    <div className="mb-6">
      <label className="block text-gray-700 font-medium mb-2">Transaction Type:</label>
      <select
        className="block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={transactionType}
        onChange={(e) => setTransactionType(e.target.value)}
      >
        <option value="BUY">Buy</option>
        <option value="SELL">Sell</option>
      </select>
    </div>

    <div className="mb-6">
      <label className="block text-gray-700 font-medium mb-2">Quantity:</label>
      <input
        type="number"
        className="block w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        min="1"
      />
    </div>

    <div>
      {transactionType === "BUY" ? (
        <h2 className="text-xl font-semibold text-green-700 mb-4">Available Shares to Buy</h2>
      ) : (
        <h2 className="text-xl font-semibold text-red-700 mb-4">Your Purchased Stocks</h2>
      )}

      <table className="w-full border-collapse bg-white rounded-lg shadow-md overflow-hidden">
        <thead className="bg-gray-200">
          <tr>
            <th className="p-4 text-left font-semibold text-gray-600">Firm</th>
            <th className="p-4 text-left font-semibold text-gray-600">Price</th>
            <th className="p-4 text-left font-semibold text-gray-600">Quantity</th>
            <th className="p-4 text-left font-semibold text-gray-600">Date</th>
            <th className="p-4 text-left font-semibold text-gray-600">Actions</th>
          </tr>
        </thead>
        <tbody>
          {(transactionType === "BUY" ? shares : myShares).map((share, index) => (
            <tr
              key={share.id}
              className={`${
                index % 2 === 0 ? "bg-gray-50" : "bg-white"
              } hover:bg-gray-100 transition-colors`}
            >
              <td className="p-4">{share.firm}</td>
              <td className="p-4">{share.price_of_last_transaction} MKD</td>
              <td className="p-4">{transactionType === "BUY" ? share.quantity_of_shares : share.quantity}</td>
              <td className="p-4">{transactionType === "BUY" ? share.date : share.purchase_date}</td>
              <td className="p-4">
                <button
                  className={`px-4 py-2 text-sm font-medium text-white rounded-md ${
                    transactionType === "BUY"
                      ? "bg-green-500 hover:bg-green-600"
                      : "bg-red-500 hover:bg-red-600"
                  } transition-colors`}
                  onClick={() => handleTransaction(share)}
                >
                  {transactionType === "BUY" ? "Buy" : "Sell"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

};

export default MyStocksPage;
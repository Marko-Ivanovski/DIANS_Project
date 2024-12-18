"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

const EditUserPage = () => {
  const [user, setUser] = useState({
    first_name: "",
    last_name: "",
    email: "",
    balance: 0,
  });
  const [password, setPassword] = useState("");
  const [amount, setAmount] = useState<number | string>("");
  const [error, setError] = useState(""); // Added error state to show any errors
  const router = useRouter();

  // Fetch user data
  useEffect(() => {
    const fetchUser = async () => {
      const accessToken = localStorage.getItem("access_token");

      if (!accessToken) {
        setError("You must be logged in to view or edit user details.");
        return;
      }

      try {
        const response = await axios.get("http://localhost:8000/edit-user/", {
          headers: {
            Authorization: `Bearer ${accessToken}`, // Add JWT token in header
          },
        });
        setUser(response.data);
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        setError("Failed to fetch user data.");
      }
    };

    fetchUser();
  }, []);

  // Update user details
  const handleUpdate = async () => {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
      setError("You must be logged in to update your details.");
      return;
    }

    try {
      const response = await axios.put(
        "http://localhost:8000/edit-user/",
        { ...user, password },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      alert("User details updated successfully!");
      setPassword("");
    } catch (error: any) {
      console.error("Error updating user details:", error.response?.data || error);
      alert("Failed to update user details.");
    }
  };

  // Add balance
  const handleAddBalance = async () => {
    if (!amount || Number(amount) <= 0) {
      alert("Please enter a valid amount.");
      return;
    }

    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
      setError("You must be logged in to add balance.");
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:8000/edit-user/",
        { amount },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`, // Add JWT token in header
          },
        }
      );
      alert(response.data.message);
      setUser((prev) => ({ ...prev, balance: response.data.new_balance }));
      setAmount(""); // Clear balance input field
    } catch (error: any) {
      console.error("Error adding balance:", error.response?.data || error);
      alert("Failed to add balance.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Edit User Details</h1>

      {/* Error message */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Form for editing user details */}
      <div>
        <label>First Name:</label>
        <input
          type="text"
          value={user.first_name}
          onChange={(e) => setUser({ ...user, first_name: e.target.value })}
        />
      </div>
      <div>
        <label>Last Name:</label>
        <input
          type="text"
          value={user.last_name}
          onChange={(e) => setUser({ ...user, last_name: e.target.value })}
        />
      </div>
      <div>
        <label>Email:</label>
        <input
          type="email"
          value={user.email}
          onChange={(e) => setUser({ ...user, email: e.target.value })}
        />
      </div>
      <div>
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Leave blank to keep current password"
        />
      </div>
      <button onClick={handleUpdate}>Update Details</button>

      {/* Section to add balance */}
      <div style={{ marginTop: "20px" }}>
        <h2>Account Balance: MKD {user.balance.toFixed(2)}</h2>
        <label>Add Balance:</label>
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <button onClick={handleAddBalance}>Add Balance</button>
      </div>
    </div>
  );
};

export default EditUserPage;

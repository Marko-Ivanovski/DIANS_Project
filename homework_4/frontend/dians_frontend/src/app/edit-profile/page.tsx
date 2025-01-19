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
      <>
        <main>
          <section className="account-section p-5">
            <div className="account-badge text-lg font-bold">My Account</div>
            <h1 className="account-title text-2xl mt-4">Account Details</h1>
            <div className="account-details mt-4">
              <div className="details-row flex gap-4">
                <div>
                  <label htmlFor="first-name">First Name</label>
                  <input
                      type="text"
                      id="first-name"
                      name="first-name"
                      value={user.first_name}
                      onChange={(e) => setUser({...user, first_name: e.target.value})}
                      className="border p-2 mt-1"
                      placeholder="Change your name"
                  />
                </div>
                <div>
                  <label htmlFor="last-name">Last Name</label>
                  <input
                      type="text"
                      id="last-name"
                      name="last-name"
                      value={user.last_name}
                      onChange={(e) => setUser({...user, last_name: e.target.value})}
                      className="border p-2 mt-1"
                      placeholder="Change your last name"
                  />
                </div>
              </div>
              <div className="details-row flex gap-4 mt-4">
                <div>
                  <label htmlFor="email">Email</label>
                  <input
                      type="email"
                      id="email"
                      name="email"
                      value={user.email}
                      onChange={(e) => setUser({...user, email: e.target.value})}
                      className="border p-2 mt-1"
                      placeholder="Change your email"
                  />
                </div>
                <div>
                  <label htmlFor="password">Password</label>
                  <input
                      type="password"
                      id="password"
                      name="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="border p-2 mt-1"
                      placeholder="Leave blank to keep current password"
                  />
                </div>
              </div>
            </div>
            {/* Error message */}
            {error && <p style={{color: "red"}}>{error}</p>}

            <button onClick={handleUpdate} className="save-changes-btn bg-blue-500 text-white p-2 mt-4">Save Changes
            </button>

            {/* Section to add balance */}
            <div className="balance-section mt-8">
              <label htmlFor="balance-input">Add Balance (MKD):</label>
              <input
                  type="number"
                  id="balance-input"
                  name="balance-input"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="border-2 p-6 mt-1 text-black w-96"
                  placeholder="Enter amount"
              />
              <button onClick={handleAddBalance} className="add-balance-btn bg-green-500 text-white p-2 mt-4">Add
              </button>

              <h2 className="mt-4">Account Balance: MKD {user.balance.toFixed(2)}</h2>
            </div>
          </section>
        </main>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
        <br/>
      </>
  );
};

export default EditUserPage;

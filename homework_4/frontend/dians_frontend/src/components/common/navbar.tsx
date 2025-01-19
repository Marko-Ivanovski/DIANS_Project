"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import axios from "axios";

axios.defaults.withCredentials = true;

const Header = () => {
  const [user, setUser] = useState<{ first_name: string } | null>(null);

  // Check for user authentication
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    console.log("Token from localStorage:", localStorage.getItem("access_token"));
    if (token) {
      axios
        .get("http://localhost:8000/users/first-name/", {

          headers: { Authorization: `Bearer ${token}` },
        })
        .then((response) => setUser(response.data))
        .catch(() => setUser(null));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  return (
    <header className="Primary-Header">
      <div className="container">
        <Link href="/">
          <Image
            src="/Images/Logo.png"
            alt="Macedonian Stock Exchange Logo"
            width={100}
            height={50}
          />
        </Link>
        <nav className="primary-navigation">
          <ul className="nav-list">
            <li><Link href="/">Home</Link></li>
            <li><Link href="/about">About Us</Link></li>
          </ul>
        </nav>
        <div className="buttons">
          {!user ? (
            <>
              <Link href="/login">
                <button className="login-btn">Log In</button>
              </Link>
              <Link href="/signup">
                <button className="signup-btn">Sign Up</button>
              </Link>
            </>
          ) : (
            <div className="dropdown">
              <button className="user-btn">Hello <b>{user.first_name}</b></button>
              <div className="dropdown-content">
                <Link href="/my-stocks">My Stocks</Link>
                <Link href="/edit-profile">Edit Profile</Link>
                <button onClick={handleLogout}>Log Out</button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
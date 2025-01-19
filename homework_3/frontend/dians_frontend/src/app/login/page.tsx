"use client";

import { useRouter } from "next/navigation";
import { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";

axios.defaults.withCredentials = true;

const Login = () => {
    const router = useRouter();
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://localhost:8001/login/", formData, {
                headers: {
                    "Content-Type": "application/json",
                },
            });
            console.log("User logged in:", response.data);

            // Store the tokens in localStorage or cookies (preferably httpOnly cookies)
            localStorage.setItem("user_id", response.data.user_id);
            localStorage.setItem("access_token", response.data.access_token);
            localStorage.setItem("refresh_token", response.data.refresh_token);


            // Redirect to the user's dashboard or home page after successful login
            router.push("/home");
        } catch (error: unknown) {
            if (error instanceof Error) {
                console.error("Error logging in:", error.message);

            } else {
                console.error("Unknown error occurred during login");
            }
        }
    };

    return (
        <main className="login-page">
            <div className="login-container">
                {/* Left Section: Login Form */}
                <div className="login-form">
                    <div className="badge">Log In</div>
                    <h1 className="form-title">Welcome Back</h1>
                    <hr className="divider" />
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="email">Email*</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                placeholder="e.g. john.doe@example.com"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password*</label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                placeholder="Password"
                                value={formData.password}
                                onChange={handleChange}
                                minLength={4}
                                required
                            />
                        </div>
                        <button className="cta-button" type="submit">
                            Log In
                        </button>
                    </form>
                    <p className="signup-link">
                        Don't have an account? <a href="/signup">Sign Up</a>
                    </p>
                </div>

                {/* Right Section: Picture and Text */}
                <div className="login-background">
                    <div className="background-text">
                        <h1>Start Your Journey to Smarter Investing</h1>
                        <p>
                            Join our community and access cutting-edge tools and insights to make informed investment decisions.
                        </p>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default Login;

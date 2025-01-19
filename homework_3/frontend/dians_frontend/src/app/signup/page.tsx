"use client";

import { useRouter } from "next/navigation";
import { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";

const Signup = () => {
    const router = useRouter();
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
    });

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://localhost:8001/signup/", formData);
            console.log("User signed up:", response.data);

            router.push("/login");
        } catch (error: unknown) {
            if (error instanceof Error) {
                console.error("Error signing up:", error.message);
            } else {
                console.error("Unknown error occurred during signup");
            }
        }
    };

    return (
        <main className="signup-page">
            <div className="signup-container">
                {/* Left Section: Signup Form */}
                <div className="signup-form">
                    <div className="badge">Sign Up</div>
                    <h1 className="form-title">Become a Member</h1>
                    <hr className="divider" />
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="first_name">First Name*</label>
                            <input
                                type="text"
                                id="first_name"
                                name="first_name"
                                placeholder="e.g. John"
                                value={formData.first_name}
                                onChange={handleChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="last_name">Last Name*</label>
                            <input
                                type="text"
                                id="last_name"
                                name="last_name"
                                placeholder="e.g. Doe"
                                value={formData.last_name}
                                onChange={handleChange}
                                required
                            />
                        </div>
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
                                placeholder="Enter your password"
                                value={formData.password}
                                onChange={handleChange}
                                minLength={8}
                                required
                            />
                        </div>
                        <button className="cta-button" type="submit">
                            Create Account Today!
                        </button>
                    </form>
                    <p className="login-link">
                        Already have an account? <a href="/login">Log In</a>
                    </p>
                </div>

                {/* Right Section: Picture and Text */}
                <div className="login-background">
                    <div className="background-text">
                        <h1>Start Your Journey to Smarter Investing</h1>
                        <p>
                            Join our community and access cutting-edge tools and insights to make informed investment
                            decisions.
                        </p>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default Signup;
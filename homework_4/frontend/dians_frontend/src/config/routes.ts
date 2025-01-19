const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_BASE_URL; // Reads from .env.local

// FRONTEND ROUTES
export const ROUTES = {
    HOME: "/",
    ABOUT: "/about",
    SIGNUP: "/signup",
    LOGIN: "/login",
    MY_STOCKS: "/my-stocks",
    PROFILE: "/edit-profile",
    NOT_FOUND: "/404"
};

// BACKEND API ROUTES(endpoints)
export const API_ROUTES = {
    SIGNUP: `${BASE_URL}/signup`,
    LOGIN: `${BASE_URL}/login`,
    GET_MY_STOCKS: `${BASE_URL}/get-my-stocks`
};
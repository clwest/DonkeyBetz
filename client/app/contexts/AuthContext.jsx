"use client";
const React = require("react");
const { createContext, useContext, useState, useEffect } = require("react");
const {useRouter} = require("next/navigation");


const AuthContext = createContext(null);

const useAuth = () => useContext(AuthContext)

const AuthProvider = ({children}) => {
    const [user, setUser] = useState(null)
    const router = useRouter()
    const API_URL = process.env.NEXT_PUBLIC_FLASK_URL

    useEffect(() => {
        console.log("User state updated:", user);
    }, [user])

    const login = async (username, password) => {
        try {
            const response = await fetch(`${API_URL}/users/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({username, password}),
            });

            if (!response.ok) {
                throw new Error("Error in login");
            }
            const {access_toke, user } = await response.json();

            localStorage.setItem("useToken", access_toke);
            setUser(user);
            console.log("Logged in user AuthContext:", user)
        } catch (error) {
            console.error("Login Error: ", error);
        }
    };

    const refreshToken = async () => {
        try {
            const response = await fetch(`${API_URL}/users/refresh`, {
                method: "POST",
                credentials: "include",
            });
            if (!response.ok) {
                throw new Error("Error in token refresh");
            }
        } catch (e) {
            console.error(e)
        }
    };

    const logout = async () => {
        try {
            const response = await fetch(`${API_URL}/users/logout`, {
                method: "POST",
                credentials: "include",
            });
            if (!response.ok) {
                throw new Error("Failed to log out");
            }
            localStorage.removeItem("userToken");
            setUser(null);
            router.push("/login")
        } catch (e) {
            console.error(e)    
        }
    };
    return (
        React.createElement(AuthContext.Provider, {value: {user, login, logout, refreshToken}}, children )
    );
};

module.exports = { AuthProvider, useAuth };


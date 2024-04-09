"use client";

const {useRouter} = require("next/navigation");
import { useState } from "react";
import Link from "next/link";
const API_URL = process.env.NEXT_PUBLIC_FLASK_URL

export default function RegisterForm() {
    const router = useRouter()
    const [data, setData] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: ""
    })

    const handleChange = (e) => {
        setData({...data, [e.target.name]: e.target.value})
    }

    const registerUser = async (e) => {
        e.preventDefault()
        const {confirmPassword, ...userData} = data;
        if (userData.password !== confirmPassword) {
            alert("Passwords do not match, try again")
            return
        }
        try {
            const response = await fetch(`${API_URL}/users/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            });

            if (!response.ok) {
                throw new Error("Error in register");
            }
            console.log(response)
            const userInfo = await response.json();
            router.push("/login");
        } catch (e) {
            console.error("Registration Error: ", e)
        }
    }
    return (
    <>
        <div className="flex flex-col justify-center items-center h-96 bg-gray-600 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
            <h2 className="mt-5 text-2xl font-bold leading-9 tracking-tight text-center text-slate-400">
            Register Account
            </h2>
        </div>

        </div>
    </>
    );
}
"use client";


import { useState } from "react"
import { useAuth } from "../contexts/AuthContext"
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_FLASK_URL

export default function LoginForm({onLoginSuccess}) {
    const {login} = useAuth();
    const [data, setData] = useState({username: "", password: ""});
    const [rememberMe, setRememberMe] = useState(false);

    const handleChange = (e) => {
        setData({...data, [e.target.name]: e.target.value});
    };

    const handleRememberMeChange = (e) => {
        setRememberMe(e.target.checked);
    };

    const handleSubmit = async (e) => {
        e.preventDefault()
        const {username, password} = data;
        try {
            await login(username, password);
            onLoginSuccess()
        } catch (e) {
            console.error("Error at login",)
        }
    }
    


    return (
        <>
        <div className="flex flex-col justify-center flex-none lg:px-8 bg-slate-600">
            <h2 className="mt-10 text-2xl font-bold leading-9 tracking-tight text-center text-cyan-500">
                Log in
            </h2>
            <form className="space-y-6" onSubmit={handleSubmit}>
                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                    <label 
                    htmlFor="username" 
                    className="block text-sm font-medium leading-6 text-slate-400"
                    >
                        UserName
                    </label>
                    <input
                    id="username"
                    name="username" 
                    type="text"
                    required
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300
                    placeholder:text-gray-400 focus:ring-2 focus:ring-inset
                    focus:ring-slate-600 sm:text-sm sm:leading-6"
                    placeholder="Username"
                    value={data.username}
                    onChange={handleChange}
                    />
                </div>
                <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                <label
                htmlFor="password"
                className="block text-sm font-medium leading-6 text-slate-400"
                >
                Password
                </label>
                <input
                type="password"
                id="password"
                name="password"
                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-slate-600 sm:text-sm sm:leading-6"
                value={data.password}
                onChange={handleChange}
                />
            </div>
            <div className="flex items-start justify-center mb-6">
                <div className="flex items-center h-5 m-1">
                <input
                    id="remember"
                    type="checkbox"
                    onChange={handleRememberMeChange}
                    className="w-4 h-4 border border-slate-400  bg-slate-100 focus:ring-3 focus:ring-slate-300 dark:bg-amber-700 dark:border-gray-600 dark:focus:ring-slate-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800"
                />
                </div>
                <label
                htmlFor="remember"
                className="block text-md font-medium leading-6 text-slate-400 p-1"
                >
                Remember me
                </label>
            </div>
            <div className="flex items-start justify-center mb-6">
                <button
                type="submit"
                className="flex justify-center rounded-md bg-slate-500 px-3 py-1.5 text-sm font-semibold leading-6 text-slate-300 shadow-sm hover:bg-slate-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-600"
                >
                Log In
                </button>
            </div>
            </form>
        </div>
        </>
    )
}
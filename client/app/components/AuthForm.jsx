// components/AuthForm.js
import React, { useState } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

const AuthForm = ({ onLoginSuccess }) => {
    const [isLogin, setIsLogin] = useState(true);

    return (
        <div className="bg-slate-600 flex flex-col justify-center items-center h-screen px-4 sm:px-6 lg:px-8">
        {isLogin ? (
            <>
            <LoginForm onLoginSuccess={onLoginSuccess} />
            <p className="text-center">
                Don't have an account?{" "}
                <button onClick={() => setIsLogin(false)} className="text-cyan-500">
                Register
                </button>
            </p>
            </>
        ) : (
            <>
            <RegisterForm />
            <p className="text-center">
                Already have an account?{" "}
                <button onClick={() => setIsLogin(true)} className="text-blue-500">
                Login
                </button>
            </p>
            </>
        )}
        </div>
    );
};

export default AuthForm;
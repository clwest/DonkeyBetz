"use client";
import React, { useState } from "react";
import Modal from "./Modal";
import AuthForm from "./AuthForm";
import { useAuth } from "../contexts/AuthContext";
import Image from "next/image";
import LaptopDonkey from "../../public/LaptopDonkey.jpeg";
import PokerDonkey from "../../public/PokerDonkey.jpeg";

export default function Header({className}) {
        const [modalOpen, setModalOpen] = useState(false);
        const { user, logout } = useAuth();

    
        return (
        <header
            className={`flex items-center justify-center text-cyan-600 text-2xl ${className}`}
        >
            <Image
            src={LaptopDonkey}
            alt="Laptop Donkey"
            width="150"
            height="50"
            className="p-4 ml-3 rounded-full"
            />
            <h1 className="text-6xl p-9 mt-6 italic font-extrabold text-center text-cyan-700">
            Donkey Betz
            </h1>
            <Image
            src={PokerDonkey}
            alt="Poker Donkey"
            width="145"
            height="50"
            className="p-4 ml-3 rounded-full"
            />
            {user ? (
            <div>
                {/* User is logged in */}
                <div className="flex items-center">
                <span className="mr-4">Welcome, {user.username}</span>
                </div>
                <button onClick={logout} className="mr-5">
                Logout
                </button>
            </div>
            ) : (
            // User is not logged in
            <button onClick={() => setModalOpen(true)} className="mr-5">
                Login/Register
            </button>
            )}
            {modalOpen && (
            <Modal isOpen={modalOpen} closeModal={() => setModalOpen(false)}>
                <AuthForm onLoginSuccess={modalOpen} />
            </Modal>
            )}
        </header>
        );
}
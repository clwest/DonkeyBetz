import { useState } from 'react';

const Modal = ({ isOpen, closeModal }) => {
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and register forms

    return (
        <div className={`fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full ${isOpen ? '' : 'hidden'}`}>
        <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
            <h3 className="text-lg leading-6 font-medium text-gray-900">{isLogin ? 'Login' : 'Register'}</h3>
            <div className="mt-2 px-7 py-3">
                <form action="#" method="POST">
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
                {isLogin ? (
                    <button type="submit" className="mt-3 w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    Log in
                    </button>
                ) : (
                    <button type="submit" className="mt-3 w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                    Register
                    </button>
                )}
                </form>
                <p className="mt-4">
                {isLogin ? 'Need an account?' : 'Already have an account?'}
                <button
                    onClick={() => setIsLogin(!isLogin)}
                    className="font-medium text-indigo-600 hover:text-indigo-500"
                >
                    {isLogin ? 'Register' : 'Login'}
                </button>
                </p>
            </div>
            </div>
            <div className="absolute top-0 right-0 cursor-pointer p-1">
            <button onClick={closeModal} className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center" aria-label="Close">
                {/* <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd"></path></svg> */}
            </button>
            </div>
        </div>
        </div>
    );
};

export default Modal;

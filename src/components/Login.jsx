import { useState } from "react";
import { useOutletContext } from "react-router-dom";

function Login() {
    // STATE //
    const { attemptLogin } = useOutletContext();
    const [name, setName] = useState("");
    const [password, setPassword] = useState("");

    console.log(attemptLogin);
    // EVENTS //

    const handleChangeUsername = (e) => setName(e.target.value);
    const handleChangePassword = (e) => setPassword(e.target.value);

    function handleSubmit(e) {
        e.preventDefault();
        attemptLogin({ name: name, password: password });
        
    }

    // RENDER //

    return (
        <div
            className="h-screen items-center px-4"
            style={{ paddingTop: "100px" }}
        >
            <form
                className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
                onSubmit={handleSubmit}
            >
                <div className="mb-4">
                    <label
                        className="block text-gray-700 text-sm font-bold mb-2"
                        htmlFor="username"
                    >
                        Username
                    </label>
                    <input
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        type="text"
                        onChange={handleChangeUsername}
                        value={name}
                        placeholder="name"
                    />
                </div>
                <div className="mb-6">
                    <label
                        className="block text-gray-700 text-sm font-bold mb-2"
                        htmlFor="password"
                    >
                        Password
                    </label>
                    <input
                        className="shadow appearance-none border border-red-500 rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                        type="password"
                        onChange={handleChangePassword}
                        value={password}
                        placeholder="password"
                    />
                    
                </div>

                <div className="flex items-center justify-between">
                    <button
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="button"
                        onClick={handleSubmit}
                    >
                        Log In
                    </button>
                </div>
            </form>
        </div>
    );
}

export default Login;

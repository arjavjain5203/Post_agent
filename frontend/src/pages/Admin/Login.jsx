import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function AdminLogin() {
    const [secret, setSecret] = useState('');
    const [error, setError] = useState('');
    const { adminLogin } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        const res = await adminLogin(secret);
        if (res.success) {
            navigate('/admin/dashboard');
        } else {
            setError(res.message);
        }
    };

    return (
        <div className="flex min-h-screen flex-1 flex-col justify-center px-6 py-12 lg:px-8 bg-gray-900">
            <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-white">
                    Admin Access
                </h2>
            </div>

            <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <form className="space-y-6" onSubmit={handleSubmit}>
                    <div>
                        <label htmlFor="secret" className="block text-sm font-medium leading-6 text-white">
                            Secret Key
                        </label>
                        <div className="mt-2">
                            <input
                                id="secret"
                                name="secret"
                                type="password"
                                required
                                className="block w-full rounded-md border-0 bg-white/5 py-1.5 text-white shadow-sm ring-1 ring-inset ring-white/10 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6 px-3"
                                value={secret}
                                onChange={(e) => setSecret(e.target.value)}
                            />
                        </div>
                    </div>

                    {error && <div className="text-red-500 text-sm font-bold text-center">{error}</div>}

                    <div>
                        <button
                            type="submit"
                            className="flex w-full justify-center rounded-md bg-indigo-500 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
                        >
                            Enter Control Panel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

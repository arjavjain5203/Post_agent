import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

export default function AddCustomer() {
    const [fullName, setFullName] = useState('');
    const [mobile, setMobile] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await api.post('/customers/', { full_name: fullName, mobile });
            navigate('/customers');
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Failed to create customer');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="space-y-8 divide-y divide-gray-200">
                <div className="space-y-8 divide-y divide-gray-200">
                    <div>
                        <div>
                            <h3 className="text-base font-semibold leading-6 text-gray-900">Add New Customer</h3>
                            <p className="mt-1 text-sm text-gray-500">
                                This information will be encrypted and stored securely.
                            </p>
                        </div>

                        <form onSubmit={handleSubmit} className="mt-6 space-y-6">
                            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
                                <div className="sm:col-span-6">
                                    <label htmlFor="full-name" className="block text-sm font-medium leading-6 text-gray-900">
                                        Full Name
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            type="text"
                                            name="full-name"
                                            id="full-name"
                                            required
                                            value={fullName}
                                            onChange={(e) => setFullName(e.target.value)}
                                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                        />
                                    </div>
                                </div>

                                <div className="sm:col-span-6">
                                    <label htmlFor="mobile" className="block text-sm font-medium leading-6 text-gray-900">
                                        Mobile Number
                                    </label>
                                    <div className="mt-2">
                                        <input
                                            type="text"
                                            name="mobile"
                                            id="mobile"
                                            required
                                            value={mobile}
                                            onChange={(e) => setMobile(e.target.value)}
                                            className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                        />
                                    </div>
                                </div>
                            </div>

                            {error && <div className="text-red-500 text-sm">{error}</div>}

                            <div className="flex items-center justify-end gap-x-6">
                                <button
                                    type="button"
                                    onClick={() => navigate('/customers')}
                                    className="text-sm font-semibold leading-6 text-gray-900"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    disabled={loading}
                                    className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
                                >
                                    {loading ? 'Saving...' : 'Save'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}

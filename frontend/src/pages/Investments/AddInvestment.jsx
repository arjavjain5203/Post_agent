import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const SCHEMES = ['NSC', 'MIS', 'FD', 'KVP'];

export default function AddInvestment() {
    const [customers, setCustomers] = useState([]);
    const [customerId, setCustomerId] = useState('');
    const [schemeType, setSchemeType] = useState('KVP');
    const [principal, setPrincipal] = useState('');
    const [startDate, setStartDate] = useState('');
    const [maturityDate, setMaturityDate] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        try {
            const response = await api.get('/customers/');
            setCustomers(response.data);
            if (response.data.length > 0) {
                setCustomerId(response.data[0].customer_id);
            }
        } catch (err) {
            console.error('Failed to fetch customers');
        }
    };

    const calculateMaturity = (start, scheme) => {
        // Simple Auto-calculation Logic (Approximation)
        if (!start) return '';
        const date = new Date(start);
        if (scheme === 'KVP') {
            // Doubles in ~115 months (9 years 7 months) - Approx 10 years for demo
            date.setMonth(date.getMonth() + 115);
        } else if (scheme === 'NSC') {
            date.setFullYear(date.getFullYear() + 5);
        } else if (scheme === 'MIS') {
            date.setFullYear(date.getFullYear() + 5);
        } else if (scheme === 'FD') {
            date.setFullYear(date.getFullYear() + 1);
        }
        return date.toISOString().split('T')[0];
    };

    const handleStartChange = (e) => {
        const val = e.target.value;
        setStartDate(val);
        if (val) {
            setMaturityDate(calculateMaturity(val, schemeType));
        }
    };

    const handleSchemeChange = (e) => {
        const val = e.target.value;
        setSchemeType(val);
        if (startDate) {
            setMaturityDate(calculateMaturity(startDate, val));
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await api.post('/investments/', {
                customer_id: customerId,
                scheme_type: schemeType,
                principal: parseFloat(principal),
                start_date: startDate,
                maturity_date: maturityDate,
                status: 'ACTIVE'
            });
            navigate('/investments');
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Failed to create investment');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="space-y-8 divide-y divide-gray-200">
                <div>
                    <div>
                        <h3 className="text-base font-semibold leading-6 text-gray-900">New Investment</h3>
                        <p className="mt-1 text-sm text-gray-500">
                            Record a new investment for a customer.
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="mt-6 space-y-6">
                        <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">

                            <div className="sm:col-span-6">
                                <label htmlFor="customer" className="block text-sm font-medium leading-6 text-gray-900">
                                    Customer
                                </label>
                                <div className="mt-2">
                                    <select
                                        id="customer"
                                        name="customer"
                                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                        value={customerId}
                                        onChange={(e) => setCustomerId(e.target.value)}
                                    >
                                        {customers.map((c) => (
                                            <option key={c.customer_id} value={c.customer_id}>
                                                {c.full_name} ({c.mobile})
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div className="sm:col-span-3">
                                <label htmlFor="scheme" className="block text-sm font-medium leading-6 text-gray-900">
                                    Scheme Type
                                </label>
                                <div className="mt-2">
                                    <select
                                        id="scheme"
                                        name="scheme"
                                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                        value={schemeType}
                                        onChange={handleSchemeChange}
                                    >
                                        {SCHEMES.map(s => <option key={s} value={s}>{s}</option>)}
                                    </select>
                                </div>
                            </div>

                            <div className="sm:col-span-3">
                                <label htmlFor="principal" className="block text-sm font-medium leading-6 text-gray-900">
                                    Principal Amount (₹)
                                </label>
                                <div className="mt-2">
                                    <input
                                        type="number"
                                        name="principal"
                                        id="principal"
                                        required
                                        min="1"
                                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                        value={principal}
                                        onChange={(e) => setPrincipal(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div className="sm:col-span-3">
                                <label htmlFor="start-date" className="block text-sm font-medium leading-6 text-gray-900">
                                    Start Date
                                </label>
                                <div className="mt-2">
                                    <input
                                        type="date"
                                        name="start-date"
                                        id="start-date"
                                        required
                                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                        value={startDate}
                                        onChange={handleStartChange}
                                    />
                                </div>
                            </div>

                            <div className="sm:col-span-3">
                                <label htmlFor="maturity-date" className="block text-sm font-medium leading-6 text-gray-900">
                                    Maturity Date
                                </label>
                                <div className="mt-2">
                                    <input
                                        type="date"
                                        name="maturity-date"
                                        id="maturity-date"
                                        required
                                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                        value={maturityDate}
                                        onChange={(e) => setMaturityDate(e.target.value)}
                                    />
                                </div>
                            </div>

                        </div>

                        {error && <div className="text-red-500 text-sm">{error}</div>}

                        <div className="flex items-center justify-end gap-x-6">
                            <button
                                type="button"
                                onClick={() => navigate('/investments')}
                                className="text-sm font-semibold leading-6 text-gray-900"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={loading}
                                className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
                            >
                                {loading ? 'Saving...' : 'Save Investment'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
}

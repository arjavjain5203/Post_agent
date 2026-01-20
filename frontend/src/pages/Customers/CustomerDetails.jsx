
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

const CustomerDetails = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [customer, setCustomer] = useState(null);
    const [investments, setInvestments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch Customer Details
                const custRes = await api.get(`/customers/${id}`);
                setCustomer(custRes.data);

                // Fetch Investments for this Customer
                const invRes = await api.get(`/investments/?customer_id=${id}`);
                setInvestments(invRes.data);
            } catch (err) {
                console.error("Failed to fetch details", err);
                setError("Failed to load customer details.");
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [id]);

    if (loading) return <div className="p-8 text-center">Loading...</div>;
    if (error) return <div className="p-8 text-center text-red-500">{error}</div>;
    if (!customer) return <div className="p-8 text-center">Customer not found</div>;

    return (
        <div className="p-8 space-y-8 animate-fade-in text-gray-800">
            <button onClick={() => navigate('/customers')} className="text-blue-600 hover:text-blue-800 mb-4">
                &larr; Back to List
            </button>

            <div className="bg-white/50 backdrop-blur-sm p-6 rounded-2xl shadow-xl border border-white/20">
                <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 mb-4">
                    {customer.full_name}
                </h1>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <p className="text-lg"><strong>Mobile:</strong> {customer.mobile}</p>
                    <p className="text-lg"><strong>Status:</strong> {customer.consent_flag ? "Consent Given" : "Pending Consent"}</p>
                </div>
            </div>

            <div>
                <h2 className="text-2xl font-semibold mb-4 text-gray-700">Investment Portfolio</h2>
                {investments.length === 0 ? (
                    <p className="text-gray-500 italic">No investments found for this customer.</p>
                ) : (
                    <div className="overflow-x-auto rounded-xl shadow-lg border border-gray-100">
                        <table className="min-w-full bg-white">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="py-4 px-6 text-left font-semibold text-gray-600">Scheme</th>
                                    <th className="py-4 px-6 text-left font-semibold text-gray-600">Uniq ID</th>
                                    <th className="py-4 px-6 text-left font-semibold text-gray-600">Amount</th>
                                    <th className="py-4 px-6 text-left font-semibold text-gray-600">Start Date</th>
                                    <th className="py-4 px-6 text-left font-semibold text-gray-600">Maturity Date</th>
                                    <th className="py-4 px-6 text-left font-semibold text-gray-600">Status</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-100">
                                {investments.map((inv) => (
                                    <tr key={inv.investment_id} className="hover:bg-gray-50 transition-colors">
                                        <td className="py-4 px-6 text-gray-800 font-medium">{inv.scheme_type}</td>
                                        <td className="py-4 px-6 text-gray-500 font-mono text-sm">{inv.investment_id.slice(0, 8)}...</td>
                                        <td className="py-4 px-6 text-gray-800">₹{inv.principal.toLocaleString()}</td>
                                        <td className="py-4 px-6 text-gray-600">{new Date(inv.start_date).toLocaleDateString()}</td>
                                        <td className="py-4 px-6 text-gray-600">{new Date(inv.maturity_date).toLocaleDateString()}</td>
                                        <td className="py-4 px-6">
                                            <span className={`px-3 py-1 rounded-full text-xs font-semibold
                                                ${inv.status === 'ACTIVE' ? 'bg-green-100 text-green-700' :
                                                    inv.status === 'MATURED' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'}`}>
                                                {inv.status}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CustomerDetails;

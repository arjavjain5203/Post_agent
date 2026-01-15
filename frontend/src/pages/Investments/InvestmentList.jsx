import { useState, useEffect } from 'react';
import { PlusIcon } from '@heroicons/react/20/solid';
import { Link } from 'react-router-dom';
import api from '../../services/api';

export default function InvestmentList() {
    const [investments, setInvestments] = useState([]);
    const [customers, setCustomers] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [invRes, custRes] = await Promise.all([
                api.get('/investments/'),
                api.get('/customers/')
            ]);

            setInvestments(invRes.data);

            // Create a map of customer_id -> full_name
            const custMap = {};
            custRes.data.forEach(c => {
                custMap[c.customer_id] = c.full_name;
            });
            setCustomers(custMap);

        } catch (error) {
            console.error('Failed to fetch data', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="px-4 sm:px-6 lg:px-8">
            <div className="sm:flex sm:items-center">
                <div className="sm:flex-auto">
                    <h1 className="text-base font-semibold leading-6 text-gray-900">Investments</h1>
                    <p className="mt-2 text-sm text-gray-700">
                        A list of all active and matured investments for your customers.
                    </p>
                </div>
                <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
                    <Link
                        to="/investments/add"
                        className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    >
                        <PlusIcon className="h-5 w-5 inline-block mr-1" />
                        New Investment
                    </Link>
                </div>
            </div>

            <div className="mt-8 flow-root">
                <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                    <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                        <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
                            <table className="min-w-full divide-y divide-gray-300">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                                            Customer
                                        </th>
                                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                            Scheme
                                        </th>
                                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                            Principal
                                        </th>
                                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                            Maturity Date
                                        </th>
                                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                            Status
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200 bg-white">
                                    {loading ? (
                                        <tr>
                                            <td colSpan="5" className="py-4 text-center text-gray-500">Loading...</td>
                                        </tr>
                                    ) : investments.length === 0 ? (
                                        <tr>
                                            <td colSpan="5" className="py-4 text-center text-gray-500">No investments found.</td>
                                        </tr>
                                    ) : (
                                        investments.map((inv) => (
                                            <tr key={inv.investment_id}>
                                                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                                    {customers[inv.customer_id] || 'Unknown'}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                    {inv.scheme_type}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                    ₹ {inv.principal.toLocaleString()}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                    {new Date(inv.maturity_date).toLocaleDateString()}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                    <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${inv.status === 'ACTIVE' ? 'bg-green-50 text-green-700 ring-green-600/20' :
                                                            inv.status === 'MATURED' ? 'bg-yellow-50 text-yellow-800 ring-yellow-600/20' :
                                                                'bg-gray-50 text-gray-600 ring-gray-500/10'
                                                        }`}>
                                                        {inv.status}
                                                    </span>
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

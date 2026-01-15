import { useState, useEffect } from 'react';
import { PlusIcon, MagnifyingGlassIcon } from '@heroicons/react/20/solid';
import { Link } from 'react-router-dom';
import api from '../../services/api';

export default function CustomerList() {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        try {
            const response = await api.get('/customers/');
            setCustomers(response.data);
        } catch (error) {
            console.error('Failed to fetch customers', error);
        } finally {
            setLoading(false);
        }
    };

    const filteredCustomers = customers.filter((customer) =>
        customer.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        customer.mobile.includes(searchTerm)
    );

    return (
        <div className="px-4 sm:px-6 lg:px-8">
            <div className="sm:flex sm:items-center">
                <div className="sm:flex-auto">
                    <h1 className="text-base font-semibold leading-6 text-gray-900">Customers</h1>
                    <p className="mt-2 text-sm text-gray-700">
                        A list of all your customers including their name and mobile number.
                    </p>
                </div>
                <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
                    <Link
                        to="/customers/add"
                        className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                    >
                        <PlusIcon className="h-5 w-5 inline-block mr-1" />
                        Add Customer
                    </Link>
                </div>
            </div>

            {/* Search Bar */}
            <div className="mt-4 max-w-md">
                <label htmlFor="search" className="sr-only">Search</label>
                <div className="relative rounded-md shadow-sm">
                    <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                        <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
                    </div>
                    <input
                        type="text"
                        name="search"
                        id="search"
                        className="block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                        placeholder="Search by name or mobile"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
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
                                            Name
                                        </th>
                                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                            Mobile
                                        </th>
                                        <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                            Date Added
                                        </th>
                                        <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                                            <span className="sr-only">Edit</span>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200 bg-white">
                                    {loading ? (
                                        <tr>
                                            <td colSpan="4" className="py-4 text-center text-gray-500">Loading...</td>
                                        </tr>
                                    ) : filteredCustomers.length === 0 ? (
                                        <tr>
                                            <td colSpan="4" className="py-4 text-center text-gray-500">No customers found.</td>
                                        </tr>
                                    ) : (
                                        filteredCustomers.map((customer) => (
                                            <tr key={customer.customer_id}>
                                                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                                                    {customer.full_name}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                    {customer.mobile}
                                                </td>
                                                <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                                                    {new Date(customer.created_at).toLocaleDateString()}
                                                </td>
                                                <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                                                    <a href="#" className="text-indigo-600 hover:text-indigo-900">
                                                        View<span className="sr-only">, {customer.full_name}</span>
                                                    </a>
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

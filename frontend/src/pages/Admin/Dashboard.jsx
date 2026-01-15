import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { UsersIcon, BriefcaseIcon, CurrencyRupeeIcon, BellAlertIcon } from '@heroicons/react/24/outline';

export default function AdminDashboard() {
    const { logout } = useAuth();
    const navigate = useNavigate();
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const { data } = await api.get('/admin/stats');
            setStats(data);
        } catch (error) {
            console.error(error);
            if (error.response?.status === 401) {
                logout();
                navigate('/admin/login');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        logout();
        navigate('/admin/login');
    };

    if (loading) return <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">Loading...</div>;

    const items = [
        { name: 'Total Agents', stat: stats?.total_agents, icon: UsersIcon },
        { name: 'Total Customers', stat: stats?.total_customers, icon: UsersIcon },
        { name: 'Total Investments', stat: stats?.total_investments, icon: BriefcaseIcon },
        { name: 'Total Asset Value', stat: `₹ ${stats?.total_investment_value?.toLocaleString()}`, icon: CurrencyRupeeIcon },
        { name: 'Pending Follow-ups', stat: stats?.pending_followups, icon: BellAlertIcon },
    ];

    return (
        <div className="min-h-screen bg-gray-900">
            <nav className="bg-gray-800 border-b border-gray-700">
                <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                    <div className="flex h-16 items-center justify-between">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <span className="text-xl font-bold text-indigo-500">Super Admin</span>
                            </div>
                        </div>
                        <div className="hidden md:block">
                            <div className="ml-4 flex items-center md:ml-6">
                                <button
                                    onClick={handleLogout}
                                    className="rounded-md bg-gray-700 px-3 py-2 text-sm font-medium text-white hover:bg-gray-600"
                                >
                                    Sign out
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>

            <header className="bg-gray-800 shadow">
                <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
                    <h1 className="text-3xl font-bold tracking-tight text-white">System Overview</h1>
                </div>
            </header>
            <main>
                <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                        {items.map((item) => (
                            <div key={item.name} className="relative overflow-hidden rounded-lg bg-gray-800 px-4 pt-5 pb-12 shadow sm:px-6 sm:pt-6">
                                <dt>
                                    <div className="absolute rounded-md bg-indigo-500 p-3">
                                        <item.icon className="h-6 w-6 text-white" aria-hidden="true" />
                                    </div>
                                    <p className="ml-16 truncate text-sm font-medium text-gray-400">{item.name}</p>
                                </dt>
                                <dd className="ml-16 flex items-baseline pb-1 sm:pb-7">
                                    <p className="text-2xl font-semibold text-white">{item.stat}</p>
                                </dd>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
}

import { useState, useEffect } from 'react';
import api from '../../services/api';
import { UserCircleIcon } from '@heroicons/react/24/outline';

export default function Dashboard() {
    const [agent, setAgent] = useState(null);
    const [stats, setStats] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            // ... profile logic handled by AuthContext if we wanted, but local is fine for now
            // Actually, let's use the one from AuthContext if available or fetch
        };
        // Fetch Stats
        const fetchStats = async () => {
            try {
                const { data } = await api.get('/dashboard/stats');
                setStats(data);
            } catch (error) {
                console.error("Failed to fetch dashboard stats", error);
            }
        };

        const loadData = async () => {
            await fetchStats();
            try {
                const { data } = await api.get('/auth/me');
                setAgent(data);
            } catch (error) { console.error(error); }
        };
        loadData();
    }, []);

    return (
        <div>
            {/* Profile Section */}
            {agent && (
                <div className="mb-8 bg-white overflow-hidden shadow rounded-lg animate-fade-in">
                    <div className="px-4 py-5 sm:p-6 flex items-center">
                        <UserCircleIcon className="h-12 w-12 text-indigo-600 mr-4" />
                        <div>
                            <h2 className="text-xl font-bold text-gray-900">Welcome, {agent.name}</h2>
                            <p className="text-gray-500">Agent ID: <span className="font-mono text-xs">{agent.agent_id}</span></p>
                            <p className="text-gray-500">Mobile: {agent.mobile}</p>
                        </div>
                    </div>
                </div>
            )}

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {/* Stats Cards */}
                <div className="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total Customers</dt>
                    <dd className="mt-1 text-3xl font-semibold text-gray-900">{stats?.total_customers ?? '-'}</dd>
                </div>
                <div className="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6 animate-slide-up" style={{ animationDelay: '0.2s' }}>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total Investments</dt>
                    <dd className="mt-1 text-3xl font-semibold text-gray-900">₹ {stats?.total_investment_value?.toLocaleString() ?? '-'}</dd>
                </div>
                <div className="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6 animate-slide-up" style={{ animationDelay: '0.3s' }}>
                    <dt className="text-sm font-medium text-gray-500 truncate">Pending Follow-ups</dt>
                    <dd className="mt-1 text-3xl font-semibold text-red-600">{stats?.pending_followups ?? '-'}</dd>
                </div>
            </div>
        </div>
    )
}

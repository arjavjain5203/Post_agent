import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './pages/Auth/Login';
import Signup from './pages/Auth/Signup';
import VerifyOTP from './pages/Auth/VerifyOTP';
import PrivateRoute from './components/PrivateRoute';
import DashboardLayout from './components/DashboardLayout';
import Dashboard from './pages/Dashboard/Dashboard';
import CustomerList from './pages/Customers/CustomerList';
import AddCustomer from './pages/Customers/AddCustomer';
import InvestmentList from './pages/Investments/InvestmentList';
import AddInvestment from './pages/Investments/AddInvestment';
import BulkUpload from './pages/BulkUpload';

import AdminLogin from './pages/Admin/Login';
import AdminDashboard from './pages/Admin/Dashboard';

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/verify" element={<VerifyOTP />} />

            <Route path="/admin/login" element={<AdminLogin />} />

            {/* Private Routes */}
            <Route element={<PrivateRoute />}>
              {/* Admin Routes (No DashboardLayout) */}
              <Route path="/admin/dashboard" element={<AdminDashboard />} />

              {/* Agent Routes (With Layout) */}
              <Route element={<DashboardLayout />}>
                <Route path="/dashboard" element={<Dashboard />} />

                <Route path="/customers" element={<CustomerList />} />
                <Route path="/customers/add" element={<AddCustomer />} />

                <Route path="/investments" element={<InvestmentList />} />
                <Route path="/investments/add" element={<AddInvestment />} />

                <Route path="/upload" element={<BulkUpload />} />

                {/* Default redirect to dashboard */}
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
              </Route>
            </Route>
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;

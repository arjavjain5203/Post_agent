import { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check session on mount by trying to fetch profile
        loadUser();
    }, []);

    const loadUser = async () => {
        try {
            const { data } = await api.get('/auth/me');
            setUser(data);
        } catch (error) {
            // 401 means not logged in / cookie expired
            // console.error("Failed to load user", error);
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    const login = async (mobile, password) => {
        try {
            // Login sets HttpOnly cookie
            await api.post('/auth/login', { mobile, password });
            await loadUser();
            return { success: true };
        } catch (error) {
            console.error("Login failed", error);
            return {
                success: false,
                message: error.response?.data?.detail || "Login failed",
                status: error.response?.status
            };
        }
    };

    const adminLogin = async (secret_key) => {
        try {
            await api.post('/admin/login', { secret_key });
            // Admin doesn't have a profile endpoint yet per se, 
            // but we can just set a dummy user or fetch something else.
            // For now, let's manually set user state or assume role based on success.
            setUser({ role: 'admin', name: 'Super Admin' });
            // Better: create /admin/me endpoint. But for now this is fine.
            return { success: true };
        } catch (error) {
            console.error("Admin Login failed", error);
            return { success: false, message: error.response?.data?.detail || "Login failed" };
        }
    };

    const logout = async () => {
        try {
            await api.post('/auth/logout');
        } catch (e) {
            console.error(e);
        }
        setUser(null);
    };

    const signup = async (name, mobile, password) => {
        try {
            await api.post('/auth/signup', { name, mobile, password });
            return { success: true };
        } catch (error) {
            return { success: false, message: error.response?.data?.detail || "Signup failed" };
        }
    }

    const verify = async (mobile, otp) => {
        try {
            await api.post('/auth/verify', { mobile, otp });
            await loadUser(); // Auto-login on success
            return { success: true };
        } catch (error) {
            return { success: false, message: error.response?.data?.detail || "Verification failed" };
        }
    }

    const resendOtp = async (mobile) => {
        try {
            await api.post('/auth/resend-otp', { mobile });
            return { success: true };
        } catch (error) {
            return { success: false, message: error.response?.data?.detail || "Resend failed" };
        }
    }

    return (
        <AuthContext.Provider value={{ user, login, logout, signup, verify, resendOtp, adminLogin, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);

import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';

export default function VerifyOTP() {
    const location = useLocation();
    const [mobile, setMobile] = useState(location.state?.mobile || '');
    const [otp, setOtp] = useState('');
    const [resendStatus, setResendStatus] = useState('');
    const [error, setError] = useState('');
    const { verify, resendOtp } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        const res = await verify(mobile, otp);
        if (res.success) {
            navigate('/dashboard');
        } else {
            setError(res.message);
        }
    };

    const handleResend = async () => {
        if (!mobile) {
            setError("Please enter mobile number first.");
            return;
        }
        setResendStatus('Sending...');
        const res = await resendOtp(mobile);
        if (res.success) {
            setResendStatus('OTP sent!');
        } else {
            setResendStatus('Failed to send.');
            setError(res.message);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
            <div className="w-full max-w-md space-y-8 bg-white p-8 shadow-lg rounded-xl">
                <div>
                    <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
                        Verify OTP
                    </h2>
                    <p className="mt-2 text-center text-sm text-gray-600">
                        {mobile ? `Enter the code sent to ${mobile}` : "Enter your mobile number and the OTP sent to it"}
                    </p>
                </div>
                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    <div className="-space-y-px rounded-md shadow-sm">
                        <div>
                            <label htmlFor="mobile" className="sr-only">
                                Mobile Number
                            </label>
                            <input
                                id="mobile"
                                name="mobile"
                                type="text"
                                required
                                className="relative block w-full rounded-t-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                placeholder="Mobile Number"
                                value={mobile}
                                onChange={(e) => setMobile(e.target.value)}
                                disabled={!!location.state?.mobile} // Disable if passed from state
                            />
                        </div>
                        <div>
                            <label htmlFor="otp" className="sr-only">
                                OTP
                            </label>
                            <input
                                id="otp"
                                name="otp"
                                type="text"
                                required
                                className="relative block w-full rounded-b-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 px-3"
                                placeholder="Enter 6-digit OTP"
                                value={otp}
                                onChange={(e) => setOtp(e.target.value)}
                            />
                        </div>
                    </div>

                    {error && (
                        <div className="text-red-500 text-sm text-center">
                            {error}
                        </div>
                    )}

                    {resendStatus && (
                        <div className="text-green-600 text-sm text-center">
                            {resendStatus}
                        </div>
                    )}

                    <div>
                        <button
                            type="submit"
                            className="group relative flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                        >
                            Verify Account
                        </button>
                    </div>
                </form>

                <div className="text-sm text-center">
                    <button
                        type="button"
                        onClick={handleResend}
                        className="font-semibold text-indigo-600 hover:text-indigo-500"
                    >
                        Resend OTP
                    </button>
                </div>
            </div>
        </div>
    );
}

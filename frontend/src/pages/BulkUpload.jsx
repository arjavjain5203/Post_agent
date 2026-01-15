import { useState } from 'react';
import { ArrowUpTrayIcon, DocumentArrowUpIcon } from '@heroicons/react/24/outline';
import api from '../services/api';

export default function BulkUpload() {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        if (e.target.files) {
            setFile(e.target.files[0]);
            setMessage(null);
            setError(null);
        }
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        setUploading(true);
        setMessage(null);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post('/upload/bulk', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setMessage(`Success! Processed ${response.data.total_rows} rows. Created ${response.data.customers_created} customers and ${response.data.investments_created} investments.`);
            setFile(null);
            // Reset file input manually if needed, or rely on state
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Failed to upload file');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="md:flex md:items-center md:justify-between mb-8">
                <div className="min-w-0 flex-1">
                    <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
                        Bulk Upload
                    </h2>
                    <p className="mt-1 text-sm text-gray-500">
                        Upload an Excel or CSV file to add multiple customers and investments at once.
                    </p>
                </div>
            </div>

            <div className="bg-white shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-base font-semibold leading-6 text-gray-900">Upload Data File</h3>
                    <div className="mt-2 max-w-xl text-sm text-gray-500 break-words">
                        <p>
                            Ensure your file has the following columns:
                            <span className="font-mono bg-gray-100 px-1 py-0.5 rounded ml-1">name</span>,
                            <span className="font-mono bg-gray-100 px-1 py-0.5 rounded mx-1">mobile</span>,
                            <span className="font-mono bg-gray-100 px-1 py-0.5 rounded mx-1">scheme_type</span>,
                            <span className="font-mono bg-gray-100 px-1 py-0.5 rounded mx-1">principal</span>,
                            <span className="font-mono bg-gray-100 px-1 py-0.5 rounded mx-1">start_date</span>,
                            <span className="font-mono bg-gray-100 px-1 py-0.5 rounded mx-1">maturity_date</span>.
                        </p>
                    </div>

                    <form onSubmit={handleUpload} className="mt-5 sm:flex sm:items-center">
                        <div className="w-full sm:max-w-xs">
                            <label htmlFor="file-upload" className="sr-only">
                                Choose file
                            </label>
                            <input
                                type="file"
                                name="file-upload"
                                id="file-upload"
                                accept=".xlsx, .xls, .csv"
                                onChange={handleFileChange}
                                className="block w-full text-sm text-slate-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-indigo-50 file:text-indigo-700
                  hover:file:bg-indigo-100
                "
                            />
                        </div>
                        <button
                            type="submit"
                            disabled={!file || uploading}
                            className="mt-3 inline-flex w-full items-center justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:ml-3 sm:mt-0 sm:w-auto disabled:opacity-50"
                        >
                            {uploading ? 'Uploading...' : 'Upload'}
                            <ArrowUpTrayIcon className="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
                        </button>
                    </form>

                    {message && (
                        <div className="mt-4 rounded-md bg-green-50 p-4">
                            <div className="flex">
                                <div className="flex-shrink-0">
                                    <DocumentArrowUpIcon className="h-5 w-5 text-green-400" aria-hidden="true" />
                                </div>
                                <div className="ml-3">
                                    <p className="text-sm font-medium text-green-800">{message}</p>
                                </div>
                            </div>
                        </div>
                    )}

                    {error && (
                        <div className="mt-4 rounded-md bg-red-50 p-4">
                            <div className="flex">
                                <div className="flex-shrink-0">
                                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" clipRule="evenodd" />
                                    </svg>
                                </div>
                                <div className="ml-3">
                                    <h3 className="text-sm font-medium text-red-800">Upload failed</h3>
                                    <div className="mt-2 text-sm text-red-700">
                                        <p>{error}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

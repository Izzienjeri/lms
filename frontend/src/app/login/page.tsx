// src/app/login/page.tsx
"use client";
import { useState } from 'react';
import { fetchAPI } from '@/lib/api';
import Link from 'next/link';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const data = await fetchAPI('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));

      window.location.href = '/'; 
      
    // Fix: Replaced `any` with `unknown` and typechecked it
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    }
  };

  return (
    <div className="max-w-md mx-auto mt-16 bg-white p-8 border border-gray-100 shadow-xl rounded-2xl">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-extrabold text-gray-900">Welcome back</h2>
        <p className="text-gray-500 mt-2">Log in to access your courses</p>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-6 text-sm text-center border border-red-100">
          {error}
        </div>
      )}

      <form onSubmit={handleLogin} className="space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
          <input 
            type="email" 
            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="you@example.com"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input 
            type="password" 
            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="••••••••"
          />
        </div>

        <button 
          type="submit" 
          className="w-full bg-indigo-600 text-white font-bold py-3 rounded-xl hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200 mt-4"
        >
          Sign In
        </button>
      </form>

      <p className="text-center text-gray-500 mt-6 text-sm">
        Don&apos;t have an account? <Link href="/register" className="text-indigo-600 font-semibold hover:underline">Sign up</Link>
      </p>
    </div>
  );
}
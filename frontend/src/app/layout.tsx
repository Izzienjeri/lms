// src/app/layout.tsx
"use client";
import './globals.css';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: string;
  name: string;
  role: string;
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isMounted, setIsMounted] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // We wrap ALL state updates inside setTimeout to make them asynchronous.
    // This perfectly prevents React's cascading render warnings!
    const timeoutId = setTimeout(() => {
      setIsMounted(true);
      
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        setUser(JSON.parse(storedUser));
      }
    }, 0);

    return () => clearTimeout(timeoutId);
  },[]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    router.push('/login');
  };

  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen font-sans text-gray-900">
        <nav className="bg-white shadow-sm sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              
              <Link href="/" className="text-2xl font-extrabold text-indigo-600 tracking-tight">
                Nexus<span className="text-gray-900">Learn</span>
              </Link>

              <div className="flex items-center space-x-4">
                {isMounted && (
                  user ? (
                    <>
                      <span className="text-sm text-gray-500 hidden sm:block">
                        Welcome, <strong className="text-gray-900">{user.name}</strong>
                      </span>
                      <Link href="/dashboard" className="text-gray-600 hover:text-indigo-600 font-medium transition-colors">
                        Dashboard
                      </Link>
                      <button 
                        onClick={handleLogout}
                        className="bg-indigo-50 text-indigo-600 px-4 py-2 rounded-lg font-medium hover:bg-indigo-100 transition"
                      >
                        Logout
                      </button>
                    </>
                  ) : (
                    <>
                      <Link href="/login" className="text-gray-600 hover:text-indigo-600 font-medium transition-colors">
                        Log in
                      </Link>
                      <Link href="/register" className="bg-indigo-600 text-white px-5 py-2 rounded-lg font-medium hover:bg-indigo-700 shadow-md shadow-indigo-200 transition-all">
                        Sign up
                      </Link>
                    </>
                  )
                )}
              </div>
            </div>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
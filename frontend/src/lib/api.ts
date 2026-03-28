// src/lib/api.ts
const API_URL = 'http://127.0.0.1:5000';

export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
    // Get token from localStorage if it exists
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    
    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
    }

    return data;
}
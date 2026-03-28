// src/app/page.tsx
"use client";
import { useEffect, useState } from 'react';
import { fetchAPI } from '@/lib/api';
import Link from 'next/link';

// 1. Define the Course type
interface Course {
  id: string;
  title: string;
  description: string;
  instructor_id: string;
}

export default function Home() {
  // 2. Add the type to the useState hook
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAPI('/courses/')
      .then(data => setCourses(data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  },[]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="text-center mb-16 mt-8">
        <h1 className="text-5xl font-extrabold text-gray-900 mb-4 tracking-tight">
          Master new skills online
        </h1>
        <p className="text-xl text-gray-500 max-w-2xl mx-auto">
          Browse our extensive catalog of beautifully crafted courses designed to help you succeed.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {courses.length === 0 ? (
          <p className="text-gray-500 text-center col-span-full">No published courses available yet.</p>
        ) : (
          /* 3. Replaced (course: any) with (course: Course) */
          courses.map((course: Course) => (
            <div key={course.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col">
              
              <div className="h-48 bg-linear-to-br from-indigo-500 to-purple-600"></div>
              
              <div className="p-6 flex flex-col grow">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{course.title}</h3>
                <p className="text-gray-600 mb-6 line-clamp-3 grow">{course.description}</p>
                
                <Link 
                  href={`/courses/${course.id}`}
                  className="w-full text-center bg-gray-50 text-indigo-600 font-semibold py-3 rounded-xl hover:bg-indigo-50 border border-indigo-100 transition-colors"
                >
                  View Course Details
                </Link>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
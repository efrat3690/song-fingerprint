// components/ProtectedRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';

export default function ProtectedRoute({ children }) {
    const token = localStorage.getItem('admin_token');

    if (!token) {
        return <Navigate to="/" replace />; // חזרה לדף הבית אם אין טוקן
    }

    return children;
}

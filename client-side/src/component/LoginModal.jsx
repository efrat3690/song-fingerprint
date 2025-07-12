import React, { useState } from 'react';
import './AudioRecorder.css'; // נניח שזה אותו קובץ CSS

export default function LoginModal({ onClose, onLoginSuccess }) { // שינוי שם ה-prop
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!username.trim() || !password.trim()) {
            setError('אנא הכנס שם משתמש וסיסמה');
            return;
        }

        setIsLoading(true);
        setError('');

        try {
            // בקשת לוגין לקבלת טוקן
            const loginResponse = await fetch('http://127.0.0.1:8000/admin/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username,
                    password
                }),
            });

            const loginData = await loginResponse.json();

            if (!loginResponse.ok) {
                // הצגת הודעת שגיאה מהשרת אם קיימת
                setError(loginData.detail || 'אימות נכשל. בדוק שם משתמש וסיסמה.');
                return;
            }

            const token = loginData.access_token;

            // שמירה ב-localStorage
            localStorage.setItem("admin_token", token);

            // קריאה לפונקציה מהקומפוננטה ההורה לאחר לוגין מוצלח
            // (הניווט לאזור הניהול יתבצע שם)
            onLoginSuccess();
            onClose(); // סגירת המודאל
            
        } catch (err) {
            console.error("שגיאה בחיבור לשרת או בתהליך הלוגין:", err);
            setError('שגיאה בחיבור לשרת או בתהליך הלוגין. אנא נסה שנית.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>כניסת מנהל</h2>
                    <button className="close-button" onClick={onClose}>×</button>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label htmlFor="username">שם משתמש:</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            disabled={isLoading}
                            placeholder="הכנס שם משתמש"
                            autoFocus
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">סיסמה:</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            disabled={isLoading}
                            placeholder="הכנס סיסמה"
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}

                    <div className="form-actions">
                        <button
                            type="submit"
                            className="submit-button"
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <div className="loading-spinner">
                                    <div className="spinner"></div>
                                    אימות...
                                </div>
                            ) : (
                                'כניסה'
                            )}
                        </button>
                        <button
                            type="button"
                            className="cancel-button"
                            onClick={onClose}
                            disabled={isLoading}
                        >
                            ביטול
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
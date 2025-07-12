import React, { useState, useRef, useEffect } from 'react';
import './AudioRecorder.css';
import LoginModal from './LoginModal';
import { useNavigate } from 'react-router-dom';

export default function AudioRecorder() {
    const [isRecording, setIsRecording] = useState(false);
    const [audioUrl, setAudioUrl] = useState(null);
    const [error, setError] = useState(null);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const [matches, setMatches] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const resultsRef = useRef(null);
    const [currentReview, setCurrentReview] = useState(0);
    const infoSectionRef = useRef(null);
    const overlayRef = useRef(null);
    const [showLoginModal, setShowLoginModal] = useState(false);
    const [title, setTitle] = useState(":תוצאות מתאימות");

    const navigate = useNavigate();

    const reviews = [
        { text: 'מדהים! סוף סוף מצאתי את השיר שלא יצא לי מהראש', name: 'דנה', stars: 5 },
        { text: 'עובד טוב מאוד, ממש שימושי', name: 'נועם', stars: 4 },
        { text: 'התוצאה הייתה מדויקת, אהבתי מאוד', name: 'רועי', stars: 5 },
        { text: 'מהיר ויעיל, חווית משתמש מעולה', name: 'טל', stars: 5 }
    ];

    useEffect(() => {
        const handleMouseMove = (e) => {
            if (!overlayRef.current) return;
            const { innerWidth, innerHeight } = window;
            const moveX = (e.clientX - innerWidth / 2) / 50;
            const moveY = (e.clientY - innerHeight / 2) / 50;
            overlayRef.current.style.transform = `translate(${moveX}px, ${moveY}px)`;
        };
        window.addEventListener("mousemove", handleMouseMove);
        return () => {
            window.removeEventListener("mousemove", handleMouseMove);
        };
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentReview((prevIndex) => (prevIndex + 1) % reviews.length);
        }, 4000);
        return () => clearInterval(interval);
    }, [reviews.length]);

    useEffect(() => {
        if ((matches.length > 0 || title.startsWith("לא נמצאו")) && resultsRef.current) {
            resultsRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [matches, title]);

    const handleRecordClick = async () => {
        setError(null);
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorderRef.current = new MediaRecorder(stream);
                audioChunksRef.current = [];
                mediaRecorderRef.current.addEventListener('dataavailable', event => {
                    if (event.data.size > 0) {
                        audioChunksRef.current.push(event.data);
                    }
                });
                mediaRecorderRef.current.addEventListener('stop', () => {
                    const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                    const url = URL.createObjectURL(blob);
                    setAudioUrl(url);
                    sendRecord(blob);
                });
                mediaRecorderRef.current.start();
                setIsRecording(true);
            } catch (err) {
                console.error("שגיאה בגישה למיקרופון:", err);
                setError("לא ניתן לגשת למיקרופון. ודא שניתנת הרשאה.");
            }
        } else {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };
  
    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setError(null);
        try {
            setIsLoading(true);
            const formData = new FormData();
            formData.append('file', file);
            const response = await fetch('http://127.0.0.1:8000/upload-audio/', {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'שגיאה בשליחת הקובץ לשרת');
            }
            const data = await response.json();
            console.log("[DEBUG] Response:", data);
            if (data.success && data.songs && data.songs.length > 0) {
                setMatches(data.songs);
                setTitle(":תוצאות מתאימות");
            } else {
                setMatches([]);
                setTitle(" .לא נמצאו תוצאות מתאימות, אנא נסה שנית");
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };
  
    const sendRecord = async (blob) => {
        setError(null);
        try {
            setIsLoading(true);
            const formData = new FormData();
            formData.append('file', blob, 'recording.webm');
            const response = await fetch('http://127.0.0.1:8000/upload-audio/', {
                method: 'POST',
                body: formData,
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'שגיאה בשליחת הקובץ לשרת');
            }
            const data = await response.json();
            console.log("[DEBUG] Response:", data);
            if (data.success && data.songs && data.songs.length > 0) {
                setMatches(data.songs);
                setTitle(":תוצאות מתאימות");
            } else {
                setMatches([]);
                setTitle(" .לא נמצאו תוצאות מתאימות, אנא נסה שנית");
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };
  
    const handleAdminLoginSuccess = () => {
        setShowLoginModal(false);
        navigate('/admin');
    };
  
    return (
        <div className="recorder-wrapper">
            <div className="top-bar">
                <img src="/logo-fingerprint.jpg" alt="לוגו טביעת אצבע" className="top-bar-logo" />
                <div className="login-container">
                    <button className="login-button" onClick={() => setShowLoginModal(true)}>כניסת מנהל</button>
                </div>
            </div>
            <header className="hero-section">
                <h1 className="main-title rainbow-text">ברוכים הבאים לאתר זיהוי שירים</h1>
                <p className="instructions-text">🎧 להתחלת הזיהוי, העלה קובץ או לחץ על הכפתור, הקלט כ-20 שניות והמתן לתוצאה</p>
                <br />
                <div className="button-group">
                    <label htmlFor="file-upload" className="upload-button">העלאת קובץ</label>
                    <input id="file-upload" type="file" accept="audio/*" onChange={handleFileUpload} style={{ display: 'none' }} />
                    <button onClick={handleRecordClick} className={`record-button ${isRecording ? 'recording' : ''}`} >
                        <img src="/logo-fingerprint.jpg" alt="לוגו" className="logo-inside-button" />
                    </button>
                </div>
                <br />
                {isRecording && <p className="recording-status">...מקליט עכשיו🎙️</p>}
                {isLoading && <p className="loading-text">...טוען תוצאות</p>}
                {audioUrl && (
                    <section className="audio-player">
                        <h3 className="audio-title">🎧 שמע שנקלט</h3><br />
                        <audio controls src={audioUrl}></audio><br />
                        <a href={audioUrl} download="recording.webm" className="download-link">הורד הקלטה</a>
                    </section>
                )}
                {error && <p className="error-text">{error}</p>}
            </header>

            <section className="info-section" ref={infoSectionRef}>
                <div className="info-overlay" ref={overlayRef}>
                    <h2>.המוזיקה היא שפה אוניברסלית שלא זקוקה לתרגום</h2>
                    <p>.היא פורטת על נימי הלב, מעוררת זיכרונות, מחברת בין תרבויות ומספרת סיפור בלי מילים. צליל יכול פשוט להעביר תחושת שמחה, עצב, געגוע או התרגשות – ולפעמים, שיר אחד יכול לשנות מצב רוח שלם. בעולם מלא רעשים, המוזיקה היא הפסקול שמלווה אותנו אמיתיים באמת</p>
                </div>
            </section>

            <section className="results-section" ref={resultsRef}>
                {(matches.length > 0 || title.startsWith("לא נמצאו")) && (
                    <div className="matches-list">
                        <h2>{title}</h2>
                        {matches.length > 0 ? (
                            <ul className="song-list">
                                {matches.map((match, index) => (
                                    <li key={index} className="match-item">
                                        <div className="song-title">{match.song_name}</div>
                                        <div className="song-info">ציון התאמה: {match.score}%</div>
                                        <audio controls src={match.file_path}></audio><br />
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="no-results-text">כאן יופיעו התוצאות כאשר יהיו התאמות לשירים שלכם</p>
                        )}
                    </div>
                )}
            </section>

            <section className="reviews-section">
                <h3>ביקורות הלקוחות שלנו</h3>
                <div className="review-carousel">
                    <div className="review-slide" style={{ transform: `translateX(-${currentReview * 100}%)` }}>
                        {reviews.map((review, index) => (
                            <div key={index} className="review">
                                <blockquote>״{review.text}״</blockquote>
                                <cite>– {review.name}</cite>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="share-us">
                    <p><a href="mailto:music_massage@gmail.com">music_massage@gmail.com</a> :נהניתם? שתפו אותנו</p>
                </div>
            </section>

            {showLoginModal && (
                <LoginModal
                    onClose={() => setShowLoginModal(false)}
                    onLoginSuccess={handleAdminLoginSuccess}
                />
            )}
        </div>
    );
}

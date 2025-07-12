import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminPanel.css';
import { FiMusic, FiLogOut, FiPlus, FiEdit3, FiSave, FiTrash2, FiX } from 'react-icons/fi';

export default function AdminPanel() {
    const [songs, setSongs] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [editingSong, setEditingSong] = useState(null);
    const [editForm, setEditForm] = useState({ song_name: '', file_path: '' });
    const [showAddForm, setShowAddForm] = useState(false);
    const [newSong, setNewSong] = useState({ song_name: '', file_path: '' });
    const [isDeleting, setIsDeleting] = useState(null);
    const [isUpdating, setIsUpdating] = useState(null);
    const [isAdding, setIsAdding] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const fileInputRef = useRef(null);

    useEffect(() => {
        fetchSongs();
    }, []);

    const getAuthHeaders = () => {
        const token = localStorage.getItem('admin_token');
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    };

    const fetchSongs = async () => {
        setError(null);
        try {
            setIsLoading(true);
            const response = await fetch('http://127.0.0.1:8000/admin/songs/', {
                method: 'GET',
                headers: getAuthHeaders(),
            });

            if (response.ok) {
                const data = await response.json();
                setSongs(data.songs || []);
            } else if (response.status === 401) {
                alert('פג תוקף ההתחברות או שאין לך הרשאה. אנא התחבר מחדש.');
                localStorage.removeItem('admin_token');
                navigate('/');
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'שגיאה בשליפת השירים מהשרת');
            }
        } catch (error) {
            console.error('Error fetching songs:', error);
            setError('שגיאה בחיבור לשרת או בשליפת השירים.');
        } finally {
            setIsLoading(false);
        }
    };


    const handleQuickUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const songName = file.name.replace(/\.[^/.]+$/, ""); // מוריד את הסיומת

        setIsAdding(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('song_name', songName);

            const response = await fetch('http://127.0.0.1:8000/admin/add_song_file', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (response.ok && result.success) {
                await fetchSongs();
            } else {
                setError(result.message || 'שגיאה בהוספת השיר');
            }
        } catch (error) {
            console.error('Error adding song:', error);
            setError('שגיאה בחיבור לשרת או בהוספת השיר.');
        } finally {
            setIsAdding(false);
        }
    };

    // הוספת שיר - שולח JSON, לא FormData
    const handleAdd = async () => {
        if (!newSong.song_name.trim() || !newSong.file_path.trim()) {
            alert('אנא מלא את כל השדות');
            return;
        }

        setIsAdding(true);
        setError(null);
        try {
            const response = await fetch('http://127.0.0.1:8000/admin/add_songs', {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({
                    song_name: newSong.song_name,
                    file_path: newSong.file_path,
                }),
            });

            if (response.ok) {
                await fetchSongs();
                setNewSong({ song_name: '', file_path: '' });
                setShowAddForm(false);
            } else if (response.status === 401) {
                alert('פג תוקף ההתחברות או שאין לך הרשאה. אנא התחבר מחדש.');
                localStorage.removeItem('admin_token');
                navigate('/');
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'שגיאה בהוספת השיר');
            }
        } catch (error) {
            console.error('Error adding song:', error);
            setError('שגיאה בחיבור לשרת או בהוספת השיר.');
        } finally {
            setIsAdding(false);
        }
    };

    // עדכון שיר - שולח JSON
    const handleUpdate = async () => {
        if (!editForm.song_name.trim() || !editForm.file_path.trim()) {
            alert('אנא מלא את כל השדות');
            return;
        }

        setIsUpdating(editingSong);
        setError(null);
        try {
            const response = await fetch(`http://127.0.0.1:8000/admin/update_songs/${editingSong}`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify({
                    song_name: editForm.song_name,
                    file_path: editForm.file_path,
                }),
            });

            if (response.ok) {
                setSongs(songs.map(song =>
                    song.id === editingSong
                        ? { ...song, song_name: editForm.song_name, file_path: editForm.file_path }
                        : song
                ));
                setEditingSong(null);
                setEditForm({ song_name: '', file_path: '' });
            } else if (response.status === 401) {
                alert('פג תוקף ההתחברות או שאין לך הרשאה. אנא התחבר מחדש.');
                localStorage.removeItem('admin_token');
                navigate('/');
            } else {
                const errorData = await response.json();
                const firstError = Array.isArray(errorData.detail)
                    ? errorData.detail[0].msg
                    : errorData.detail;
                setError(firstError || 'שגיאה בעדכון השיר');
            }
        } catch (error) {
            console.error('Error updating song:', error);
            setError('שגיאה בחיבור לשרת או בעדכון השיר.');
        } finally {
            setIsUpdating(null);
        }
    };

    // מחיקת שיר
    const handleDelete = async (songId) => {
        if (!window.confirm('האם אתה בטוח שברצונך למחוק את השיר?')) return;
        setIsDeleting(songId);
        setError(null);
        try {
            const response = await fetch(`http://127.0.0.1:8000/admin/delete_songs/${songId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('admin_token')}`,
                },
            });

            if (response.ok) {
                setSongs(songs.filter(song => song.id !== songId));
            } else if (response.status === 401) {
                alert('פג תוקף ההתחברות או שאין לך הרשאה. אנא התחבר מחדש.');
                localStorage.removeItem('admin_token');
                navigate('/');
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'שגיאה במחיקת השיר');
            }
        } catch (error) {
            console.error('Error deleting song:', error);
            setError('שגיאה בחיבור לשרת או במחיקת השיר.');
        } finally {
            setIsDeleting(null);
        }
    };

    const handleEdit = (song) => {
        setShowAddForm(false);
        setEditingSong(song.id);
        setEditForm({ song_name: song.song_name, file_path: song.file_path });
    };

    const cancelEdit = () => {
        setEditingSong(null);
        setEditForm({ song_name: '', file_path: '' });
    };

    const onLogout = () => {
        localStorage.removeItem('admin_token');
        navigate('/');
    };

    if (isLoading) {
        return (
            <div className="admin-loading">
                <div className="loading-content">
                    <div className="admin-spinner"></div>
                    <p>טוען נתונים...</p>
                </div>
            </div>
        );
    }

    const isBusy = isAdding || isUpdating !== null || isDeleting !== null;

    return (
        <div className="admin-panel">
            <header className="admin-header">
                <h1 className="admin-title"><FiMusic className="title-icon" /> לוח בקרת מנהל</h1>
                <button className="logout-button" onClick={onLogout} disabled={isBusy}>
                    <FiLogOut size={20} /> יציאה
                </button>
            </header>

            <div className="admin-actions">
                <input
                    type="file"
                    accept=".mp3,.wav"
                    style={{ display: 'none' }}
                    ref={fileInputRef}
                    onChange={handleQuickUpload}
                    disabled={isBusy}
                />

                <button
                    className="add-song-button"
                    onClick={() => {
                        setShowAddForm(false); // סוגר טופס טקסט אם פתוח
                        setEditingSong(null);
                        fileInputRef.current.click(); // פותח את הדיאלוג של הקובץ
                    }}
                    disabled={isBusy}
                >
                    <FiPlus size={18} /> הוסף שיר חדש
                </button>
            </div>


            <div className="songs-container">
                <h2>רשימת שירים ({songs.length})</h2>
                {songs.length === 0 ? (
                    <div className="empty-state">
                        <FiMusic size={48} />
                        <p>אין שירים במערכת</p>
                        <p>לחץ על "הוסף שיר חדש" כדי להתחיל</p>
                    </div>
                ) : (
                    <div className="songs-grid">
                        {songs.map((song) => (
                            <div key={song.id} className="song-card">
                                {editingSong === song.id ? (
                                    <div className="edit-form">
                                        <div className="form-group">
                                            <label>שם השיר:</label>
                                            <input
                                                type="text"
                                                value={editForm.song_name}
                                                onChange={(e) => setEditForm({ ...editForm, song_name: e.target.value })}
                                                disabled={isBusy}
                                            />
                                        </div>
                                        <div className="form-group">
                                            <label>כתובת הקובץ:</label>
                                            <input
                                                type="text"
                                                value={editForm.file_path}
                                                onChange={(e) => setEditForm({ ...editForm, file_path: e.target.value })}
                                                disabled={isBusy}
                                            />
                                        </div>
                                        <div className="edit-actions">
                                            <button
                                                className="save-button"
                                                onClick={handleUpdate}
                                                disabled={isBusy}
                                            >
                                                <FiSave size={16} />
                                                {isUpdating === song.id ? 'שומר...' : 'שמור'}
                                            </button>
                                            <button
                                                className="cancel-edit-button"
                                                onClick={cancelEdit}
                                                disabled={isBusy}
                                            >
                                                <FiX size={16} /> ביטול
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <>
                                        <div className="song-info">
                                            <h3 className="song-name">{song.song_name}</h3>
                                            <p className="song-path">{song.file_path}</p>
                                        </div>
                                        <div className="song-actions">
                                            <button
                                                className="edit-button"
                                                onClick={() => handleEdit(song)}
                                                title="עריכה"
                                                disabled={isBusy}
                                            >
                                                <FiEdit3 size={16} />
                                            </button>
                                            <button
                                                className="delete-button"
                                                onClick={() => handleDelete(song.id)}
                                                title="מחיקה"
                                                disabled={isBusy}
                                            >
                                                {isDeleting === song.id ? <div className="button-spinner"></div> : <FiTrash2 size={16} />}
                                            </button>
                                        </div>
                                    </>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}
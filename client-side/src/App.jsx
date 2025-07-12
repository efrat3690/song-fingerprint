import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AudioRecorder from './component/AudioRecorder';
import AdminPanel from './component/AdminPanel';
import ProtectedRoute from './component/ProtectedRoute'; // יישאר ProtectedRoute

function App() {
    return (
        <Router>
            <Routes>
                {/* נתיב דף הבית */}
                <Route path="/" element={<AudioRecorder />} />
                {/* נתיב מוגן לאזור הניהול */}
                <Route
                    path="/admin"
                    element={
                        <ProtectedRoute>
                            <AdminPanel />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App; 
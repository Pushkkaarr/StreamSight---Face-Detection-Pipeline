import React from 'react';
import VideoFeed from './components/VideoFeed';
import ROIOverlay from './components/ROIOverlay';
import './App.css';

const App: React.FC = () => {
    return (
        <div className="app-container">
            <header className="app-header">
                <h1>MEGA AI StreamSight</h1>
            </header>
            <main className="app-content">
                <div className="left-column">
                    <VideoFeed />
                </div>
                <div className="right-column">
                    <ROIOverlay />
                </div>
            </main>
        </div>
    );
};

export default App;

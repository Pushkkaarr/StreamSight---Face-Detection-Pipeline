import React from 'react';
import { useVideoStream } from '../hooks/useVideoStream';
import './VideoFeed.css';

const VideoFeed: React.FC = () => {
    const { status, frameUrl, fps } = useVideoStream('/ws/stream');

    return (
        <div className="video-feed-container">
            <div className="video-header">
                <h2>Live Feed</h2>
                <div className="status-indicators">
                    <span className={`status-dot ${status === 'Connected' ? 'connected' : 'disconnected'}`}></span>
                    <span>{status}</span>
                    {status === 'Connected' && <span className="fps-counter">{fps} FPS</span>}
                </div>
            </div>
            <div className="video-content">
                {frameUrl ? (
                    <img src={frameUrl} alt="Live Video Feed" className="video-image" />
                ) : (
                    <div className="video-placeholder">
                        <p>{status}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default VideoFeed;

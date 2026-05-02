import React from 'react';
import { useROIData } from '../hooks/useROIData';
import './ROIOverlay.css';

const ROIOverlay: React.FC = () => {
    const data = useROIData('/api/roi');

    return (
        <div className="roi-overlay-container">
            <h2>ROI Detections</h2>
            <div className="roi-list">
                {data.map((roi, index) => (
                    <div key={roi.id} className={`roi-item ${index === 0 ? 'highlighted' : ''}`}>
                        <div className="roi-time">
                            {new Date(roi.detected_at).toLocaleTimeString()}
                        </div>
                        <div className="roi-details">
                            <span className="roi-confidence">{(roi.confidence * 100).toFixed(1)}% Conf</span>
                            <span className="roi-bbox">
                                Box: [{roi.x}, {roi.y}, {roi.width}, {roi.height}]
                            </span>
                            <span className="roi-frame">
                                Frame: {roi.frame_width}x{roi.frame_height}
                            </span>
                        </div>
                    </div>
                ))}
                {data.length === 0 && <div className="no-data">No detections yet.</div>}
            </div>
        </div>
    );
};

export default ROIOverlay;

import { useState, useEffect } from 'react';

export interface ROIData {
    id: string;
    detected_at: string;
    confidence: number;
    x: number;
    y: number;
    width: number;
    height: number;
    frame_width: number;
    frame_height: number;
}

export const useROIData = (apiUrl: string) => {
    const [data, setData] = useState<ROIData[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${apiUrl}?limit=10`);
                if (response.ok) {
                    const result = await response.json();
                    setData(result);
                }
            } catch (error) {
                console.error("Failed to fetch ROI data:", error);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 2000);
        return () => clearInterval(interval);
    }, [apiUrl]);

    return data;
};

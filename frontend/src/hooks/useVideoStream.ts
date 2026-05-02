import { useState, useEffect, useRef, useCallback } from 'react';

export const useVideoStream = (url: string) => {
    const [status, setStatus] = useState<'Connecting…' | 'Connected' | 'No signal'>('Connecting…');
    const [frameUrl, setFrameUrl] = useState<string | null>(null);
    const [fps, setFps] = useState<number>(0);
    const wsRef = useRef<WebSocket | null>(null);
    const reconnectAttempts = useRef<number>(0);
    const frameTimes = useRef<number[]>([]);

    const connect = useCallback(() => {
        setStatus('Connecting…');
        const wsUrl = url.startsWith('/') 
            ? `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}${url}` 
            : url;
            
        const ws = new WebSocket(wsUrl);
        ws.binaryType = 'blob';

        ws.onopen = () => {
            setStatus('Connected');
            reconnectAttempts.current = 0;
        };

        ws.onmessage = (event) => {
            if (event.data instanceof Blob) {
                const urlObj = URL.createObjectURL(event.data);
                setFrameUrl(prev => {
                    if (prev) URL.revokeObjectURL(prev);
                    return urlObj;
                });
                
                const now = performance.now();
                frameTimes.current.push(now);
                const oneSecondAgo = now - 1000;
                frameTimes.current = frameTimes.current.filter(t => t > oneSecondAgo);
                setFps(frameTimes.current.length);
            } else {
                // keepalive or other string message
            }
        };

        ws.onclose = () => {
            setStatus('No signal');
            if (reconnectAttempts.current < 5) {
                const backoff = Math.pow(2, reconnectAttempts.current) * 1000;
                reconnectAttempts.current++;
                setTimeout(connect, backoff);
            }
        };

        wsRef.current = ws;
    }, [url]);

    useEffect(() => {
        connect();
        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
        };
    }, [connect]);

    return { status, frameUrl, fps };
};

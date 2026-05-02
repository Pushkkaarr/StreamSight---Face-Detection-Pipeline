# MEGA AI — Real-Time Face Detection Video Streaming System

A production-ready, fully containerised system for real-time face detection in video streams. 

## Architecture Overview
The system uses a React+Vite frontend to connect via WebSockets to a FastAPI backend. The frontend sends raw video frames (or another client could), which the backend processes using Google's MediaPipe for face detection. If a face is found, the backend uses Pillow (PIL) to draw a minimal matrix-green bounding box around it. The processed frames are placed in an `asyncio.Queue`, acting as a bridge, to be broadcasted instantly to all connected viewers on the stream WebSocket endpoint. Simultaneously, ROI detection metadata is asynchronously persisted to a PostgreSQL database via SQLAlchemy and Alembic, allowing the frontend to poll and display the latest detection statistics alongside the live video feed.

## Prerequisites
- Docker Desktop ≥ 4.x
- No other dependencies are required.

## Quick Start
Run the following exactly 4 commands to get the system up and running:
```bash
git clone <repository_url> .
cp .env.example .env
docker compose up --build
# Open http://localhost
```

## API Reference

| Endpoint | Method | Description | Example Response Shape |
|----------|--------|-------------|------------------------|
| `/ws/ingest` | WS | Ingest raw video frames | N/A (WebSocket) |
| `/ws/stream` | WS | Stream processed frames | N/A (WebSocket) |
| `/api/roi` | GET | List ROI detections | `[{"id": "...", "confidence": 0.9, "x": 10, ...}]` |
| `/api/roi/stats` | GET | Aggregate ROI stats | `{"total_detections": 100, "average_confidence": 0.85, ...}` |
| `/api/roi/{id}` | GET | Single ROI by ID | `{"id": "...", "confidence": 0.9, ...}` |

## Testing
To run the backend tests:
```bash
docker compose exec backend pytest
```

To run the frontend tests:
```bash
docker compose exec frontend npm run test
```

## Design Decisions
- **Why MediaPipe:** MediaPipe provides highly accurate, lightweight, and performant face detection. It's cross-platform and natively returns robust bounding box metadata, making it ideal for real-time constraints. Crucially, it replaces `cv2` completely.
- **Why Pillow for drawing:** Pillow is straightforward and efficient for basic image manipulation like drawing bounding boxes. It does not carry the large, complex dependencies of OpenCV and perfectly fulfills the strict constraint of avoiding `cv2`.
- **Why asyncio.Queue for frame bridging:** It provides a simple, thread-safe, and asynchronous way to decouple the ingest and stream WebSockets. Multiple viewers can receive the frame without blocking the ingestion process, preventing backpressure.
- **Why PostgreSQL over Redis for ROI persistence:** PostgreSQL provides ACID compliance and persistent storage. We need to query historical ROI data, paginate, and generate statistics, which relational databases excel at via efficient indexing.

## Known Limitations & Future Work
- The current fan-out implementation sends frames to all connected clients. In a massive scale scenario, a pub/sub system like Redis or Kafka would be more appropriate.
- Video ingest currently only accepts raw frames (JPEG/PNG) which is bandwidth intensive. Support for compressed video streams (e.g., WebRTC) would improve performance.

"""initial

Revision ID: 001
Revises: 
Create Date: 2026-05-02 23:55:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('''
        CREATE TABLE roi_detections (
            id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id    UUID NOT NULL,
            frame_index   INTEGER NOT NULL,
            detected_at   TIMESTAMP WITH TIME ZONE DEFAULT now(),
            x             INTEGER NOT NULL,
            y             INTEGER NOT NULL,
            width         INTEGER NOT NULL,
            height        INTEGER NOT NULL,
            confidence    FLOAT NOT NULL,
            frame_width   INTEGER NOT NULL,
            frame_height  INTEGER NOT NULL
        );
    ''')
    op.execute('CREATE INDEX idx_roi_session ON roi_detections(session_id);')
    op.execute('CREATE INDEX idx_roi_detected_at ON roi_detections(detected_at);')

def downgrade() -> None:
    op.execute('DROP TABLE roi_detections;')

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

global.fetch = vi.fn(() => 
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve([])
  })
) as any;

class MockWebSocket {
  onopen = null;
  onmessage = null;
  onclose = null;
  close = vi.fn();
}
global.WebSocket = MockWebSocket as any;

describe('App', () => {
  it('renders the title', () => {
    render(<App />);
    expect(screen.getByText('MEGA AI StreamSight')).toBeDefined();
  });
});

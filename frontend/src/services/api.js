/**
 * API client for the Creative Copilot backend.
 * Two main calls matching the agentic graph flow:
 *   1. /api/brief — runs idea → brief → brainstorm ↔ review loop → returns concepts
 *   2. /api/script — user picks concept → script → panels (all in one)
 */

const API_BASE = import.meta.env.VITE_API_BASE || '';

async function apiCall(endpoint, body) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Step 1: Submit idea → runs autonomous agent loop → returns brief + reviewed concepts.
 * The backend agents (Creative Director → Brainstormer ↔ Reviewer) run without human input.
 */
export const generateBriefAndConcepts = async (idea) => {
  const data = await apiCall('/api/brief', { idea });
  return {
    thread_id: data.thread_id,
    brief: data.brief,
    concepts: data.concepts,
    revision_count: data.revision_count,
    reviewer_feedback: data.reviewer_feedback,
    reviewer_reasoning: data.reviewer_reasoning,
    concepts_approved: data.concepts_approved,
  };
};

/**
 * Step 2: User picked a concept → runs screenwriter + storyboard artist → returns script + panels.
 */
export const generateScriptAndPanels = async (concept, thread_id) => {
  const data = await apiCall('/api/script', { concept, thread_id });
  return {
    shots: data.shots,
    panels: data.panels,
  };
};

/**
 * Export PDF storyboard.
 */
export const exportStoryboardPdf = async (brief, panels) => {
  const payload = { brief, panels };
  const response = await fetch(`${API_BASE}/api/export-pdf`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || 'Failed to export PDF');
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `storyboard-${brief?.title?.replace(/[^a-zA-Z0-9]/g, '_') || 'export'}.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
};

/**
 * Health check — verify backend connectivity.
 */
export async function checkHealth() {
  const response = await fetch(`${API_BASE}/api/health`);
  return response.json();
}

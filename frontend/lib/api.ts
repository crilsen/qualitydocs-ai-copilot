export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function api(path: string, opts: RequestInit = {}) {
  const res = await fetch(`${API}${path}`, opts);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text.slice(0, 300)}`);
  }
  return res.json();
}

export const MODES = [
  { id: "executive_summary", label: "Executive Summary" },
  { id: "document_comparison", label: "Document / Version Comparison" },
  { id: "missing_items", label: "Missing Items" },
  { id: "divergence", label: "Divergences & Inconsistencies" },
  { id: "risk", label: "Risks & Nonconformities" },
  { id: "action_plan", label: "Suggested Action Plan" },
];

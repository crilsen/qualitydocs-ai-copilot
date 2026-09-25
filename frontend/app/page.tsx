"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "../lib/api";

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    Promise.all([api("/api/documents"), api("/api/history")])
      .then(([d, h]) => setStats({ docs: d.documents?.length || 0, runs: h.runs?.length || 0 }))
      .catch((e) => setError(String(e)));
  }, []);
  return (
    <div className="grid gap-4">
      <h2 className="text-xl font-semibold">Dashboard</h2>
      {error && <p className="text-red-600 text-sm">Backend not reachable: {error} — start it with docker compose or uvicorn.</p>}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-white border rounded p-4"><div className="text-3xl font-bold">{stats?.docs ?? "—"}</div><div className="text-sm text-slate-600">Processed documents</div></div>
        <div className="bg-white border rounded p-4"><div className="text-3xl font-bold">{stats?.runs ?? "—"}</div><div className="text-sm text-slate-600">Analysis runs</div></div>
        <div className="bg-white border rounded p-4"><div className="text-3xl font-bold">6</div><div className="text-sm text-slate-600">Analysis modes</div></div>
        <div className="bg-white border rounded p-4"><div className="text-3xl font-bold">4</div><div className="text-sm text-slate-600">Synthetic demo docs</div></div>
      </div>
      <div className="flex gap-2">
        <Link href="/upload" className="px-4 py-2 rounded bg-slate-900 text-white text-sm">Upload documents</Link>
        <Link href="/analysis" className="px-4 py-2 rounded bg-white border text-sm">Choose analysis mode</Link>
        <Link href="/governance" className="px-4 py-2 rounded bg-white border text-sm">Governance</Link>
      </div>
      <div className="bg-white border rounded p-4 text-sm">
        <h3 className="font-semibold mb-1">Flow</h3>
        <p>1. Upload 2–5 PDF/DOCX → 2. Pick a mode + prompt version → 3. Review structured findings with evidence → 4. Human review (Accept / Edit / Reject) → 5. Track history.</p>
      </div>
    </div>
  );
}

"use client";
import { useState } from "react";
import { api } from "../../lib/api";

export default function ReviewPage() {
  const [runId, setRunId] = useState("");
  const [data, setData] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [msg, setMsg] = useState("");

  async function load() {
    setMsg("");
    try {
      setData(await api(`/api/analyses/${runId}`));
      setSummary(await api(`/api/analyses/${runId}/review-summary`));
    } catch (e: any) { setMsg(String(e.message || e).slice(0, 300)); }
  }

  async function review(fid: number, status: string) {
    const comment = prompt(`Reviewer comment for finding #${fid}:`) || "";
    let extra: any = {};
    if (status === "edited") {
      const title = prompt("Edited title (empty = keep):") || undefined;
      const description = prompt("Edited description (empty = keep):") || undefined;
      const recommended_action = prompt("Edited recommended action (empty = keep):") || undefined;
      extra = { title, description, recommended_action };
    }
    await api(`/api/findings/${fid}/review`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status, reviewer_comment: comment, ...extra }) });
    load();
  }

  return (
    <div className="grid gap-4">
      <h2 className="text-xl font-semibold">Human review</h2>
      <div className="flex gap-2 text-sm">
        <input value={runId} onChange={(e) => setRunId(e.target.value)} placeholder="Run ID" className="border rounded p-1" />
        <button onClick={load} className="px-3 py-1 rounded bg-slate-900 text-white">Load</button>
      </div>
      {summary && <p className="text-sm">Total {summary.total} — accepted {summary.counts.accepted}, edited {summary.counts.edited}, rejected {summary.counts.rejected}, pending {summary.counts.pending}</p>}
      {data?.findings.map((f: any) => (
        <div key={f.id} className="bg-white border rounded p-3 text-sm">
          <div className="font-medium">#{f.id} [{f.severity}/{f.category}] {f.title} — <span className="text-slate-500">{f.status}</span></div>
          <p className="text-xs text-slate-600 mt-1">{f.description}</p>
          {f.reviewer_comment && <p className="text-xs mt-1">Reviewer: {f.reviewer_comment}</p>}
          <div className="flex gap-2 mt-2">
            {(["accepted", "edited", "rejected"] as const).map((s) => (
              <button key={s} onClick={() => review(f.id, s)} className="px-2 py-1 border rounded text-xs capitalize">{s}</button>
            ))}
          </div>
        </div>
      ))}
      {msg && <p className="text-sm">{msg}</p>}
    </div>
  );
}

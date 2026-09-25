"use client";
import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api } from "../../lib/api";

function ResultsInner() {
  const params = useSearchParams();
  const runId = params.get("run");
  const [data, setData] = useState<any>(null);
  const [sev, setSev] = useState("");
  const [cat, setCat] = useState("");
  const [open, setOpen] = useState<number | null>(null);
  const [msg, setMsg] = useState("");

  function load() {
    if (!runId) return;
    api(`/api/analyses/${runId}?severity=${sev}&category=${cat}`).then(setData).catch((e) => setMsg(String(e)));
  }
  useEffect(load, [runId, sev, cat]);

  if (!runId) return <p className="text-sm">Run an analysis first from the Analysis page.</p>;
  if (!data) return <p className="text-sm">{msg || "Loading…"}</p>;

  return (
    <div className="grid gap-4">
      <h2 className="text-xl font-semibold">Results — run #{data.run.id} ({data.run.mode})</h2>
      <p className="text-xs text-slate-500">Model: {data.run.model} · Prompt: {data.run.prompt_version} · Latency: {data.run.latency_ms} ms</p>
      <div className="bg-white border rounded p-3 text-sm"><h3 className="font-semibold">Executive summary</h3><p>{data.run.executive_summary}</p></div>
      <div className="flex gap-2 text-sm">
        <select value={sev} onChange={(e) => setSev(e.target.value)} className="border rounded p-1"><option value="">All severities</option><option value="low">low</option><option value="medium">medium</option><option value="high">high</option></select>
        <select value={cat} onChange={(e) => setCat(e.target.value)} className="border rounded p-1"><option value="">All categories</option><option value="missing_item">missing_item</option><option value="divergence">divergence</option><option value="risk">risk</option><option value="nonconformity">nonconformity</option><option value="recommendation">recommendation</option></select>
        <button onClick={load} className="px-3 py-1 border rounded bg-white">Filter</button>
      </div>
      <div className="bg-white border rounded">
        <table className="w-full text-sm">
          <thead><tr className="text-left border-b"><th className="p-2">Severity</th><th className="p-2">Category</th><th className="p-2">Title</th><th className="p-2">Status</th><th className="p-2"></th></tr></thead>
          <tbody>{data.findings.map((f: any) => (
            <>
              <tr key={f.id} className="border-b"><td className="p-2">{f.severity}</td><td className="p-2">{f.category}</td><td className="p-2">{f.title}</td><td className="p-2">{f.status}</td>
                <td className="p-2"><button onClick={() => setOpen(open === f.id ? null : f.id)} className="underline">Evidence</button></td></tr>
              {open === f.id && <tr><td colSpan={5} className="p-3 bg-slate-50 text-xs">
                <p className="mb-1">{f.description}</p>
                {f.evidence.map((e: any, i: number) => <p key={i} className="mb-1"><b>{e.document_name}</b> [{e.page_or_section}]: “{e.excerpt}”</p>)}
                <p className="mt-1"><b>Recommended:</b> {f.recommended_action}</p>
              </td></tr>}
            </>
          ))}</tbody>
        </table>
      </div>
      <div className="bg-white border rounded p-3 text-sm"><h3 className="font-semibold">Limitations</h3><ul className="list-disc ml-5">{data.run.limitations.map((l: string, i: number) => <li key={i}>{l}</li>)}</ul></div>
    </div>
  );
}

export default function ResultsPage() {
  return <Suspense fallback={<p className="text-sm">Loading…</p>}><ResultsInner /></Suspense>;
}

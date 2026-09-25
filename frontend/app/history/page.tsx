"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "../../lib/api";

export default function HistoryPage() {
  const [runs, setRuns] = useState<any[]>([]);
  useEffect(() => { api("/api/history").then((h) => setRuns(h.runs)).catch(() => {}); }, []);
  return (
    <div className="grid gap-4">
      <h2 className="text-xl font-semibold">Run history</h2>
      <div className="bg-white border rounded">
        <table className="w-full text-sm">
          <thead><tr className="text-left border-b"><th className="p-2">Run</th><th className="p-2">Mode</th><th className="p-2">Prompt</th><th className="p-2">Model</th><th className="p-2">Latency</th><th className="p-2">Findings</th></tr></thead>
          <tbody>{runs.map((r) => (
            <tr key={r.id} className="border-b"><td className="p-2"><Link className="underline" href={`/results?run=${r.id}`}>#{r.id}</Link></td><td className="p-2">{r.mode}</td><td className="p-2">{r.prompt_version}</td><td className="p-2">{r.model}</td><td className="p-2">{r.latency_ms} ms</td><td className="p-2">{r.findings_count}</td></tr>
          ))}</tbody>
        </table>
      </div>
      {!runs.length && <p className="text-sm text-slate-500">No runs yet.</p>}
    </div>
  );
}

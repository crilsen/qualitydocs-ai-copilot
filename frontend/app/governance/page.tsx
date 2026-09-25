"use client";
import { useEffect, useState } from "react";
import { api } from "../../lib/api";

export default function GovernancePage() {
  const [g, setG] = useState<any>(null);
  useEffect(() => { api("/api/governance").then(setG).catch(() => {}); }, []);
  if (!g) return <p className="text-sm">Loading…</p>;
  return (
    <div className="grid gap-4 text-sm">
      <h2 className="text-xl font-semibold">Governance & Responsible Use</h2>
      <div className="p-3 rounded bg-amber-100 border border-amber-300">{g.notice}</div>
      <div className="bg-white border rounded p-4"><h3 className="font-semibold">Principles</h3><ul className="list-disc ml-5">{g.principles.map((p: string, i: number) => <li key={i}>{p}</li>)}</ul></div>
      <div className="bg-white border rounded p-4"><h3 className="font-semibold">Allowed data</h3><ul className="list-disc ml-5">{g.allowed_data.map((p: string, i: number) => <li key={i}>{p}</li>)}</ul></div>
      <div className="bg-white border rounded p-4"><h3 className="font-semibold">Prohibited data</h3><ul className="list-disc ml-5">{g.prohibited_data.map((p: string, i: number) => <li key={i}>{p}</li>)}</ul></div>
      <div className="bg-white border rounded p-4"><h3 className="font-semibold">AI limits</h3><ul className="list-disc ml-5">{g.ai_limits.map((p: string, i: number) => <li key={i}>{p}</li>)}</ul></div>
    </div>
  );
}

"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, MODES } from "../../lib/api";

export default function AnalysisPage() {
  const [docs, setDocs] = useState<any[]>([]);
  const [sel, setSel] = useState<number[]>([]);
  const [mode, setMode] = useState(MODES[0].id);
  const [version, setVersion] = useState("v1.0.0");
  const [versions, setVersions] = useState<any[]>([]);
  const [msg, setMsg] = useState("");
  const router = useRouter();

  useEffect(() => {
    api("/api/documents").then((d) => setDocs(d.documents)).catch((e) => setMsg(String(e)));
    api("/api/prompts").then((p) => setVersions(p.prompts)).catch(() => {});
  }, []);

  function toggle(id: number) {
    setSel((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id].slice(0, 5)));
  }

  async function run() {
    setMsg("");
    try {
      const r = await api("/api/analyses/run", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ mode, document_ids: sel, prompt_version: version }) });
      router.push(`/results?run=${r.run_id}`);
    } catch (e: any) { setMsg(`Analysis failed: ${e.message?.slice(0, 400)}`); }
  }

  return (
    <div className="grid gap-4">
      <h2 className="text-xl font-semibold">Choose analysis mode</h2>
      <div className="grid md:grid-cols-2 gap-3">
        {MODES.map((m) => (
          <button key={m.id} onClick={() => setMode(m.id)} className={`text-left p-3 rounded border bg-white ${mode === m.id ? "ring-2 ring-slate-900" : ""}`}>
            <div className="font-medium text-sm">{m.label}</div>
            <div className="text-xs text-slate-500">{m.id}</div>
          </button>
        ))}
      </div>
      <div>
        <label className="text-sm font-medium">Prompt version</label>
        <select value={version} onChange={(e) => setVersion(e.target.value)} className="ml-2 border rounded p-1 text-sm">
          {Array.from(new Set(versions.map((v) => v.version))).map((v) => <option key={v} value={v}>{v}</option>)}
          {!versions.length && <option value="v1.0.0">v1.0.0</option>}
        </select>
      </div>
      <div>
        <h3 className="text-sm font-medium mb-1">Documents ({sel.length}/5, need 2–5)</h3>
        {docs.map((d) => (
          <label key={d.id} className="flex items-center gap-2 text-sm bg-white border rounded p-2 mb-1">
            <input type="checkbox" checked={sel.includes(d.id)} onChange={() => toggle(d.id)} /> {d.filename} <span className="text-slate-500">({d.pages_or_sections})</span>
          </label>
        ))}
        {!docs.length && <p className="text-sm text-slate-500">No documents yet — upload some first.</p>}
      </div>
      <button disabled={sel.length < 2} onClick={run} className="px-4 py-2 rounded bg-slate-900 text-white text-sm disabled:opacity-40 w-fit">Run analysis</button>
      {msg && <p className="text-sm">{msg}</p>}
    </div>
  );
}

"use client";
import { useEffect, useState } from "react";
import { api } from "../../lib/api";

export default function UploadPage() {
  const [docs, setDocs] = useState<any[]>([]);
  const [msg, setMsg] = useState("");
  const refresh = () => api("/api/documents").then((d) => setDocs(d.documents)).catch((e) => setMsg(String(e)));
  useEffect(() => { refresh(); }, []);

  async function onFiles(e: React.ChangeEvent<HTMLInputElement>) {
    setMsg("");
    const files = e.target.files;
    if (!files || files.length === 0) return;
    if (files.length > 5) { setMsg("Select at most 5 files."); return; }
    const fd = new FormData();
    for (const f of Array.from(files)) fd.append("files", f);
    try {
      const r = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/documents/upload`, { method: "POST", body: fd });
      if (!r.ok) throw new Error(await r.text());
      const body = await r.json();
      setMsg(`Processed ${body.documents.length} document(s).`);
      refresh();
    } catch (err: any) { setMsg(`Upload failed: ${err.message?.slice(0, 300)}`); }
  }

  return (
    <div className="grid gap-4">
      <h2 className="text-xl font-semibold">Upload documents (2–5 PDF/DOCX)</h2>
      <input type="file" accept=".pdf,.docx" multiple onChange={onFiles} className="text-sm" />
      {msg && <p className="text-sm">{msg}</p>}
      <div className="bg-white border rounded">
        <table className="w-full text-sm">
          <thead><tr className="text-left border-b"><th className="p-2">File</th><th className="p-2">Type</th><th className="p-2">Pages/Sections</th><th className="p-2">Chars</th><th className="p-2">Flag</th></tr></thead>
          <tbody>{docs.map((d) => (
            <tr key={d.id} className="border-b"><td className="p-2">{d.filename}</td><td className="p-2">{d.file_type}</td><td className="p-2">{d.pages_or_sections}</td><td className="p-2">{d.char_count}</td><td className="p-2">{d.suspicious_flag ? "suspicious text (data-only)" : "—"}</td></tr>
          ))}</tbody>
        </table>
      </div>
      <p className="text-xs text-slate-500">Demo ships with 4 synthetic documents (procedures, specification, nonconformity report). Only synthetic data — never upload real or confidential files.</p>
    </div>
  );
}

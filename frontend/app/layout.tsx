import "./globals.css";
import Link from "next/link";

const NAV = [
  ["Dashboard", "/"],
  ["Upload", "/upload"],
  ["Analysis", "/analysis"],
  ["Results", "/results"],
  ["History", "/history"],
  ["Review", "/review"],
  ["Governance", "/governance"],
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <header className="flex flex-wrap items-center gap-3 justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold">Document Quality AI Copilot</h1>
              <p className="text-sm text-slate-600">Consolidate, compare and validate quality documents with generative AI.</p>
            </div>
            <nav className="flex flex-wrap gap-2">
              {NAV.map(([label, href]) => (
                <Link key={href + label} href={href} className="px-3 py-1.5 rounded bg-white border text-sm hover:bg-slate-100">
                  {label}
                </Link>
              ))}
            </nav>
          </header>
          <div className="mb-6 p-3 rounded bg-amber-100 border border-amber-300 text-sm">
            AI-generated results must be reviewed before any decision.
          </div>
          <main>{children}</main>
          <footer className="mt-10 text-xs text-slate-500">MVP v0.1.0 — synthetic demo data only. No real or confidential data.</footer>
        </div>
      </body>
    </html>
  );
}

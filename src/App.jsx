import { useState } from "react";

export default function App() {

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  async function analyzeCode() {

    if (!code.trim()) return;

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            code,
          }),
        }
      );

      const data = await response.json();

      setResult(data);

    } catch (error) {

      console.error(error);

      alert("Backend connection error");

    } finally {

      setLoading(false);
    }
  }

  return (

    <div className="min-h-screen bg-[#0f172a] text-white p-10">

      <div className="max-w-7xl mx-auto">

        {/* HEADER */}

        <div className="mb-10">

          <h1 className="text-5xl font-bold mb-3">
            AI Security Analyzer
          </h1>

          <p className="text-slate-400 text-lg">
            Transformer-based vulnerability detection system
          </p>

        </div>

        {/* MAIN GRID */}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          {/* LEFT PANEL */}

          <div className="bg-[#1e293b] rounded-3xl p-6 shadow-2xl">

            <div className="flex items-center justify-between mb-4">

              <h2 className="text-2xl font-semibold">
                Source Code
              </h2>

              <button
                onClick={analyzeCode}
                disabled={loading}
                className="
                  bg-cyan-500
                  hover:bg-cyan-400
                  transition
                  px-6
                  py-3
                  rounded-xl
                  font-semibold
                  text-black
                "
              >
                {
                  loading
                    ? "Analyzing..."
                    : "Analyze"
                }
              </button>

            </div>

            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste vulnerable code here..."
              className="
                w-full
                h-[600px]
                bg-[#020617]
                border
                border-slate-700
                rounded-2xl
                p-5
                outline-none
                resize-none
                font-mono
                text-sm
              "
            />

          </div>

          {/* RIGHT PANEL */}

          <div className="space-y-6">

            {/* LANGUAGE */}

            <div className="bg-[#1e293b] rounded-3xl p-6 shadow-xl">

              <h3 className="text-xl font-semibold mb-4">
                Language Detection
              </h3>

              {
                result && (

                  <div>

                    <div className="flex justify-between mb-2">

                      <span className="text-slate-300">
                        {result.language.label}
                      </span>

                      <span className="text-cyan-400 font-bold">
                        {result.language.confidence}%
                      </span>

                    </div>

                    <div className="w-full bg-slate-700 rounded-full h-3">

                      <div
                        className="bg-cyan-400 h-3 rounded-full"
                        style={{
                          width: `${result.language.confidence}%`
                        }}
                      />

                    </div>

                  </div>
                )
              }

            </div>

            {/* VULNERABILITY */}

            <div className="bg-[#1e293b] rounded-3xl p-6 shadow-xl">

              <h3 className="text-xl font-semibold mb-4">
                Vulnerability Analysis
              </h3>

              {
                result && (

                  <div className="space-y-4">

                    <div className="flex justify-between">

                      <span className="text-slate-400">
                        Vulnerability
                      </span>

                      <span className="font-bold text-red-400">
                        {result.vulnerability}
                      </span>

                    </div>

                    <div className="flex justify-between">

                      <span className="text-slate-400">
                        Confidence
                      </span>

                      <span className="font-bold">
                        {result.confidence}%
                      </span>

                    </div>

                    <div className="flex justify-between">

                      <span className="text-slate-400">
                        Risk
                      </span>

                      <span className="
                        bg-red-500/20
                        text-red-400
                        px-3
                        py-1
                        rounded-xl
                        font-semibold
                      ">
                        {result.risk}
                      </span>

                    </div>

                  </div>
                )
              }

            </div>

            {/* EXPLANATION */}

            <div className="bg-[#1e293b] rounded-3xl p-6 shadow-xl">

              <h3 className="text-xl font-semibold mb-4">
                Explanation
              </h3>

              <p className="text-slate-300 leading-7">

                {
                  result
                    ? result.explanation
                    : "No analysis yet."
                }

              </p>

            </div>

            {/* FIXED CODE */}

            <div className="bg-[#1e293b] rounded-3xl p-6 shadow-xl">

              <h3 className="text-xl font-semibold mb-4">
                Suggested Fix
              </h3>

              <pre className="
                bg-[#020617]
                rounded-2xl
                p-5
                overflow-auto
                text-sm
                text-green-400
                font-mono
              ">
                {
                  result
                    ? result.fixed_code
                    : "// fixed code appears here"
                }
              </pre>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
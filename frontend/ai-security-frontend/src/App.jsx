import "./App.css";

import { useState } from "react";

import CodeEditor from "./components/CodeEditor";
import ResultPanel from "./components/ResultPanel";

const API_URL =
    "http://127.0.0.1:8000/analyze";

function App() {

    const [code, setCode] = useState(
`import os

user_input = input()

os.system(user_input)`
    );

    const [result, setResult] = useState(null);

    const [loading, setLoading] = useState(false);

    const analyzeCode = async () => {

        if (!code?.trim()) {

            alert("Code is empty");

            return;
        }

        setLoading(true);

        setResult(null);

        try {

            const controller =
                new AbortController();

            const timeout = setTimeout(
                () => controller.abort(),
                15000
            );

            const response = await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify({
                        code: code
                    }),

                    signal: controller.signal
                }
            );

            clearTimeout(timeout);

            if (!response.ok) {

                const errorText =
                    await response.text();

                console.error(
                    "Backend Error:",
                    errorText
                );

                throw new Error(
                    "Analysis failed"
                );
            }

            const data =
                await response.json();

            console.log(
                "Analysis Result:",
                data
            );

            setResult(data);

        } catch (err) {

            console.error(err);

            if (
                err.name === "AbortError"
            ) {

                alert(
                    "Request timeout"
                );

            } else {

                alert(
                    "Backend error. Check logs."
                );
            }

        } finally {

            setLoading(false);
        }
    };

    return (

        <div className="app">

            {/* ========================= */}
            {/* TOPBAR */}
            {/* ========================= */}

            <header className="topbar">

                <div>

                    <h1>
                        AI Security Analysis Platform
                    </h1>

                    <p>
                        Semantic vulnerability
                        detection engine
                    </p>

                </div>

                <button
                    className="analyze-button"
                    onClick={analyzeCode}
                    disabled={loading}
                >

                    {
                        loading
                            ? "Analyzing..."
                            : "Run Analysis"
                    }

                </button>

            </header>

            {/* ========================= */}
            {/* WORKSPACE */}
            {/* ========================= */}

            <main className="workspace">

                {/* ========================= */}
                {/* EDITOR */}
                {/* ========================= */}

                <section className="editor-section">

                    <div className="panel-title">
                        Source Code
                    </div>

                    <CodeEditor
                        code={code}
                        setCode={setCode}
                    />

                </section>

                {/* ========================= */}
                {/* RESULTS */}
                {/* ========================= */}

                <section className="results-section">

                    <div className="panel-title">
                        Analysis
                    </div>

                    <ResultPanel
                        result={result}
                        loading={loading}
                    />

                </section>

            </main>

        </div>
    );
}

export default App;
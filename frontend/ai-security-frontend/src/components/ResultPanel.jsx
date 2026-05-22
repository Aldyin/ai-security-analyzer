import "./ResultPanel.css";

function ResultPanel({ result, loading }) {

    if (loading) {

        return (

            <div className="result-panel">

                <div className="loading">
                    Running semantic analysis...
                </div>

            </div>
        );
    }

    if (!result) {

        return (

            <div className="result-panel empty">

                <div className="empty-state">

                    <h2>
                        AI Security Engine
                    </h2>

                    <p>
                        Submit source code for
                        semantic vulnerability analysis.
                    </p>

                </div>

            </div>
        );
    }

    const language =
        result.language?.label ||
        result.language ||
        "Unknown";

    const vulnerability =
        result.vulnerability ||
        "SAFE";

    const confidence =
        result.confidence || 0;

    const risk =
        result.risk || "LOW";

    const explanation =
        result.explanation ||
        "No explanation available.";

    const fixedCode =
        result.fixed_code ||
        "// No remediation generated";

    const detectionSource =
        result.detection_source ||
        "AI_MODEL";

    const riskClass =
        risk === "CRITICAL"
            ? "red"
            : risk === "HIGH"
            ? "orange"
            : "green";

    return (

        <div className="result-panel">

            <div className="result-grid">

                <div className="result-card">

                    <span className="label">
                        Language
                    </span>

                    <span className="value blue">
                        {language}
                    </span>

                </div>

                <div className="result-card">

                    <span className="label">
                        Threat
                    </span>

                    <span className="value red">
                        {vulnerability}
                    </span>

                </div>

                <div className="result-card">

                    <span className="label">
                        Confidence
                    </span>

                    <span className="value">
                        {confidence}%
                    </span>

                </div>

                <div className="result-card">

                    <span className={`value ${riskClass}`}>
                        {risk}
                    </span>

                </div>

            </div>

            <div className="analysis-box">

                <h3>
                    Detection Source
                </h3>

                <p>
                    {detectionSource}
                </p>

            </div>

            <div className="analysis-box">

                <h3>
                    Semantic Analysis
                </h3>

                <p>
                    {explanation}
                </p>

            </div>

            <div className="analysis-box">

                <h3>
                    Secure Remediation
                </h3>

                <pre>
                    {fixedCode}
                </pre>

            </div>

        </div>
    );
}

export default ResultPanel;
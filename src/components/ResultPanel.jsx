function ResultPanel({ result }) {

    if (!result) {

        return (
            <div>
                No analysis yet.
            </div>
        );
    }

    return (

        <div>

            <h2>Language</h2>
            <p>{result.language}</p>

            <h2>Vulnerability</h2>
            <p>{result.vulnerability}</p>

            <h2>Risk</h2>
            <p>{result.risk}</p>

            <h2>Confidence</h2>
            <p>{result.confidence}</p>

            <h2>Explanation</h2>
            <p>{result.explanation}</p>

            <h2>Fixed Code</h2>

            <pre>
                {result.fixed_code}
            </pre>

        </div>
    );
}


export default ResultPanel;
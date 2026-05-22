import Editor from "@monaco-editor/react";

function CodeEditor({ code, setCode }) {

    return (
        <Editor
            height="700px"
            defaultLanguage="python"
            value={code}
            onChange={(value) => setCode(value || "")}
            theme="vs-dark"
            options={{
                fontSize: 15,
                minimap: {
                    enabled: false,
                },
                fontFamily: "JetBrains Mono",
                smoothScrolling: true,
                padding: {
                    top: 20,
                },
            }}
        />
    );
}

export default CodeEditor;
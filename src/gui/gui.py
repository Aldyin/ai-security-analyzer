import tkinter as tk

from src.application.pipeline.auto_analyze import auto_analyze

from src.gui.components.editor import CodeEditor
from src.gui.components.charts import ProbabilityChart

from src.gui.widgets.fix_panel import FixPanel
from src.gui.widgets.risk_panel import RiskPanel
from src.gui.widgets.explanation_panel import ExplanationPanel


class SecurityAnalyzerGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AI Secure Code Analyzer"
        )

        self.root.geometry("1600x950")

        # =====================================
        # TOP BAR
        # =====================================

        top = tk.Frame(root)

        top.pack(
            fill=tk.X,
            padx=5,
            pady=5
        )

        self.analyze_btn = tk.Button(
            top,
            text="Analyze Code",
            command=self.analyze_code,
            bg="#1976D2",
            fg="white",
            font=("Arial", 11, "bold")
        )

        self.analyze_btn.pack(
            side=tk.LEFT,
            padx=5
        )

        self.status_label = tk.Label(
            top,
            text="READY",
            font=("Arial", 11, "bold")
        )

        self.status_label.pack(
            side=tk.RIGHT,
            padx=10
        )

        # =====================================
        # MAIN
        # =====================================

        main = tk.PanedWindow(
            root,
            orient=tk.HORIZONTAL,
            sashrelief=tk.RAISED
        )

        main.pack(
            fill=tk.BOTH,
            expand=True
        )

        # =====================================
        # LEFT PANEL
        # =====================================

        left = tk.Frame(main)

        main.add(
            left,
            stretch="always"
        )

        self.editor = CodeEditor(left)

        self.editor.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        # =====================================
        # RIGHT PANEL
        # =====================================

        right = tk.Frame(main)

        main.add(
            right,
            stretch="always"
        )

        # =====================================
        # RESULT
        # =====================================

        result_frame = tk.LabelFrame(
            right,
            text="Analysis Result",
            font=("Arial", 12, "bold")
        )

        result_frame.pack(
            fill=tk.X,
            padx=5,
            pady=5
        )

        self.result_text = tk.Text(
            result_frame,
            height=12,
            font=("Consolas", 11)
        )

        self.result_text.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        # =====================================
        # RISK PANEL
        # =====================================

        self.risk_panel = RiskPanel(right)

        self.risk_panel.pack(
            fill=tk.X,
            padx=5,
            pady=5
        )

        # =====================================
        # CHART
        # =====================================

        chart_frame = tk.LabelFrame(
            right,
            text="Confidence",
            font=("Arial", 12, "bold")
        )

        chart_frame.pack(
            fill=tk.BOTH,
            expand=False,
            padx=5,
            pady=5
        )

        self.chart = ProbabilityChart(
            chart_frame
        )

        self.chart.pack(
            fill=tk.BOTH,
            expand=True
        )

        # =====================================
        # EXPLANATION PANEL
        # =====================================

        self.explanation_panel = ExplanationPanel(
            right
        )

        self.explanation_panel.pack(
            fill=tk.BOTH,
            expand=False,
            padx=5,
            pady=5,
            ipady=40
        )

        # =====================================
        # FIX PANEL
        # =====================================

        self.fix_panel = FixPanel(right)

        self.fix_panel.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

    # =========================================
    # ANALYZE
    # =========================================

    def analyze_code(self):

        code = self.editor.get_code()

        if not code.strip():
            return

        self.status_label.config(
            text="ANALYZING..."
        )

        try:

            result = auto_analyze(code)

            # =================================
            # RESULT TEXT
            # =================================

            output = f"""
Language: {result['language']}

Vulnerability: {result['vulnerability']}

Confidence: {result['confidence']}%

Risk: {result['risk']}

Message:
{result['message']}
"""

            self.result_text.delete(
                "1.0",
                tk.END
            )

            self.result_text.insert(
                tk.END,
                output
            )

            # =================================
            # RISK
            # =================================

            self.risk_panel.set_risk(
                result["risk"]
            )

            # =================================
            # EXPLANATION
            # =================================

            self.explanation_panel.set_explanation(
                result["explanation"]
            )

            # =================================
            # FIX
            # =================================

            self.fix_panel.set_fix(
                result["fixed_code"]
            )

            # =================================
            # CHART
            # =================================

            labels = [
                result["vulnerability"]
            ]

            probs = [
                result["confidence"]
            ]

            self.chart.update_chart(
                labels,
                probs
            )

            self.status_label.config(
                text="DONE"
            )

        except Exception as e:

            self.status_label.config(
                text="ERROR"
            )

            self.result_text.delete(
                "1.0",
                tk.END
            )

            self.result_text.insert(
                tk.END,
                str(e)
            )


def main():

    root = tk.Tk()

    app = SecurityAnalyzerGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
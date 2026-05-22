import tkinter as tk

from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from src.api.analyzer import analyze_code

from src.gui.widgets.fix_panel import (
    FixPanel
)

from src.gui.widgets.risk_panel import (
    RiskPanel
)

from src.gui.widgets.explanation_panel import (
    ExplanationPanel
)

from src.config.gui import *


class SecurityAnalyzerGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Hybrid AI Security Analyzer"
        )

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.build_ui()

    # ==========================================
    # UI
    # ==========================================

    def build_ui(self):

        # ======================================
        # TOP
        # ======================================

        top_frame = ttk.Frame(
            self.root
        )

        top_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            top_frame,
            text="Source Code",
            font=TITLE_FONT
        ).pack(
            anchor="w"
        )

        # ======================================
        # EDITOR
        # ======================================

        self.editor = ScrolledText(
            self.root,
            font=EDITOR_FONT,
            height=20
        )

        self.editor.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ======================================
        # BUTTONS
        # ======================================

        button_frame = ttk.Frame(
            self.root
        )

        button_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        analyze_btn = ttk.Button(
            button_frame,
            text="Analyze",
            command=self.run_analysis
        )

        analyze_btn.pack(
            side="left"
        )

        clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_editor
        )

        clear_btn.pack(
            side="left",
            padx=5
        )

        # ======================================
        # RESULTS
        # ======================================

        results_frame = ttk.Frame(
            self.root
        )

        results_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # LEFT
        left_frame = ttk.Frame(
            results_frame
        )

        left_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        # RIGHT
        right_frame = ttk.Frame(
            results_frame
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ======================================
        # RESULT LABELS
        # ======================================

        self.language_var = tk.StringVar()

        self.vuln_var = tk.StringVar()

        self.confidence_var = tk.StringVar()

        ttk.Label(
            left_frame,
            textvariable=self.language_var,
            font=UI_FONT
        ).pack(
            anchor="w",
            pady=5
        )

        ttk.Label(
            left_frame,
            textvariable=self.vuln_var,
            font=UI_FONT
        ).pack(
            anchor="w",
            pady=5
        )

        ttk.Label(
            left_frame,
            textvariable=self.confidence_var,
            font=UI_FONT
        ).pack(
            anchor="w",
            pady=5
        )

        # ======================================
        # PANELS
        # ======================================

        self.risk_panel = RiskPanel(
            left_frame
        )

        self.risk_panel.pack(
            fill="x",
            pady=10
        )

        self.explanation_panel = (
            ExplanationPanel(
                left_frame
            )
        )

        self.explanation_panel.pack(
            fill="both",
            expand=True,
            pady=10
        )

        self.fix_panel = FixPanel(
            right_frame
        )

        self.fix_panel.pack(
            fill="both",
            expand=True
        )

    # ==========================================
    # ACTIONS
    # ==========================================

    def run_analysis(self):

        code = self.editor.get(
            "1.0",
            tk.END
        )

        try:

            result = analyze_code(
                code
            )

            self.language_var.set(
                f"Language: {result.language}"
            )

            self.vuln_var.set(
                f"Vulnerability: {result.vulnerability}"
            )

            self.confidence_var.set(
                f"Confidence: {result.confidence:.2f}%"
            )

            self.risk_panel.update_risk(
                result.risk
            )

            self.explanation_panel.update_explanation(
                result.explanation
            )

            self.fix_panel.update_fix(
                result.fixed_code
            )

        except Exception as e:

            self.language_var.set(
                "Analysis failed"
            )

            self.vuln_var.set(
                str(e)
            )

    def clear_editor(self):

        self.editor.delete(
            "1.0",
            tk.END
        )

        self.language_var.set("")
        self.vuln_var.set("")
        self.confidence_var.set("")

        self.risk_panel.update_risk(
            ""
        )

        self.explanation_panel.update_explanation(
            ""
        )

        self.fix_panel.update_fix(
            ""
        )


def main():

    root = tk.Tk()

    app = SecurityAnalyzerGUI(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()
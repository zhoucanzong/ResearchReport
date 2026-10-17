/* MathJax + Mermaid 初始化（vendored，零外链）
   配色按站点靛蓝调手校；mermaid 用 base 主题，浅靛底 + 深字 + 透明背景，
   保证浅色/深色模式下都可读。 */
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  },
  svg: {
    scale: 0.98,
    fontCache: "local"
  }
};

document.addEventListener("DOMContentLoaded", function () {
  if (typeof mermaid !== "undefined") {
    mermaid.initialize({
      startOnLoad: true,
      securityLevel: "strict",
      theme: "base",
      themeVariables: {
        background: "transparent",
        primaryColor: "#e8eaf6",
        primaryTextColor: "#1a1a2e",
        primaryBorderColor: "#5c6bc0",
        lineColor: "#7986cb",
        secondaryColor: "#f3e5f5",
        tertiaryColor: "#e3f2fd",
        fontFamily: "inherit"
      },
      flowchart: { curve: "basis", htmlLabels: true }
    });
  }
});

/* MkDocs Material instant navigation：页面无刷新切换后重排版公式 */
if (typeof document$ !== "undefined") {
  document$.subscribe(function () {
    if (window.MathJax && MathJax.startup && MathJax.startup.output) {
      MathJax.startup.output.clearCache();
      MathJax.typesetClear();
      MathJax.texReset();
      MathJax.typesetPromise();
    }
    if (typeof mermaid !== "undefined") {
      mermaid.run({ querySelector: ".mermaid" });
    }
  });
}

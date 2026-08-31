"""Generate a Mermaid + PNG visualization of the agent graph.

Usage:
    python visualize.py

Outputs `graph.mmd` (Mermaid source) and `graph.png` (rendered image) in
the current directory. This only inspects the compiled graph structure —
it does not call any LLM, so no API key is required.
"""

from agents.graph import app


def main() -> None:
    graph = app.get_graph()

    mermaid_source = graph.draw_mermaid()
    with open("graph.mmd", "w") as f:
        f.write(mermaid_source)
    print("Wrote graph.mmd")

    try:
        png_bytes = graph.draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(png_bytes)
        print("Wrote graph.png")
    except Exception as exc:  # pragma: no cover - requires network access to render
        print(f"Skipped graph.png (rendering service unreachable): {exc}")

    print("\n--- Mermaid source ---\n")
    print(mermaid_source)


if __name__ == "__main__":
    main()

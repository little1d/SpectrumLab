import gradio as gr
import pandas as pd


def create_leaderboard():
    # 模拟数据
    data = {
        "Model": ["GPT-4V", "Claude-3", "Random"],
        "Overall Accuracy": [0.85, 0.82, 0.25],
        "IR Accuracy": [0.87, 0.85, 0.24],
        "NMR Accuracy": [0.83, 0.79, 0.26],
    }

    df = pd.DataFrame(data)

    with gr.Blocks(title="Spectral Hub Leaderboard") as demo:
        gr.Markdown("# 🏆 Spectral Hub 排行榜")
        gr.Dataframe(df, interactive=False)

    return demo


if __name__ == "__main__":
    app = create_leaderboard()
    app.launch(server_name="0.0.0.0", server_port=7860)

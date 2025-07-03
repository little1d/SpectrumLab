import gradio as gr
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Optional


class SpectralLeaderboard:
    def __init__(self, data_file: str = "../leaderboard.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """加载排行榜数据"""
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _format_accuracy(self, accuracy: Optional[float]) -> str:
        """格式化准确率显示"""
        if accuracy is None:
            return "-"
        return f"{accuracy:.1f}%"

    def _calculate_average(self, results: Dict) -> Optional[float]:
        """计算平均准确率，忽略null值"""
        valid_accuracies = []
        for level_data in results.values():
            if level_data["accuracy"] is not None:
                valid_accuracies.append(level_data["accuracy"])

        if valid_accuracies:
            return sum(valid_accuracies) / len(valid_accuracies)
        return None

    def _get_model_type_icon(self, model_type: str) -> str:
        """获取模型类型图标"""
        icons = {"open_source": "🔓", "proprietary": "🔒", "baseline": "📊"}
        return icons.get(model_type, "❓")

    def _get_multimodal_icon(self, is_multimodal: bool) -> str:
        """获取多模态图标"""
        return "👁️" if is_multimodal else "📝"

    def _get_rank_display(self, rank: int) -> str:
        """获取排名显示，前三名显示奖牌"""
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        return medals.get(rank, str(rank))

    def _create_link(self, text: str, url: str) -> str:
        """创建HTML链接"""
        if url and url.strip():
            return f'<a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">{text}</a>'
        return text

    def get_leaderboard_df(
        self,
        model_type_filter: str = "All",
        multimodal_filter: str = "All",
        sort_by: str = "Average",
        ascending: bool = False,
    ) -> pd.DataFrame:
        """生成排行榜DataFrame"""

        models = self.data["models"]

        # 筛选模型
        filtered_models = []
        for model in models:
            # 模型类型筛选
            if model_type_filter != "All" and model["model_type"] != model_type_filter:
                continue

            # 多模态筛选
            if multimodal_filter == "Multimodal Only" and not model["is_multimodal"]:
                continue
            elif multimodal_filter == "Text Only" and model["is_multimodal"]:
                continue

            filtered_models.append(model)

        # 构建DataFrame数据
        data = []
        for model in filtered_models:
            results = model["results"]

            # 计算平均分
            avg_accuracy = self._calculate_average(results)

            # 创建带链接的模型名和提交者
            model_name_display = self._create_link(
                model["name"], model.get("name_link", "")
            )
            submitter_display = self._create_link(
                model["submitter"], model.get("submitter_link", "")
            )

            row = {
                "Type": self._get_model_type_icon(model["model_type"]),
                "Model": model_name_display,
                "Size": model["model_size"],
                "MM": self._get_multimodal_icon(model["is_multimodal"]),
                "Average": self._format_accuracy(avg_accuracy),
                "Signal": self._format_accuracy(results["Signal"]["accuracy"]),
                "Perception": self._format_accuracy(results["Perception"]["accuracy"]),
                "Semantic": self._format_accuracy(results["Semantic"]["accuracy"]),
                "Generation": self._format_accuracy(results["Generation"]["accuracy"]),
                "Submitter": submitter_display,
                "Date": (
                    model["submission_time"][:10] if model["submission_time"] else "-"
                ),
                # 用于排序的数值列
                "avg_val": avg_accuracy or 0,
                "signal_val": results["Signal"]["accuracy"] or 0,
                "perception_val": results["Perception"]["accuracy"] or 0,
                "semantic_val": results["Semantic"]["accuracy"] or 0,
                "generation_val": results["Generation"]["accuracy"] or 0,
            }
            data.append(row)

        df = pd.DataFrame(data)

        if len(df) == 0:
            return df

        # 排序
        sort_mapping = {
            "Average": "avg_val",
            "Signal": "signal_val",
            "Perception": "perception_val",
            "Semantic": "semantic_val",
            "Generation": "generation_val",
            "Model": "Model",
            "Date": "Date",
        }

        sort_col = sort_mapping.get(sort_by, "avg_val")
        df = df.sort_values(by=sort_col, ascending=ascending)

        # 添加带奖牌的排名
        ranks = []
        for i in range(len(df)):
            rank_num = i + 1
            ranks.append(self._get_rank_display(rank_num))

        df.insert(0, "Rank", ranks)

        # 移除用于排序的辅助列
        display_columns = [
            "Rank",
            "Type",
            "Model",
            "Size",
            "MM",
            "Average",
            "Signal",
            "Perception",
            "Semantic",
            "Generation",
            "Submitter",
            "Date",
        ]
        return df[display_columns]

    def get_subcategory_details(self, model_name: str) -> pd.DataFrame:
        """获取模型的子类别详细结果"""
        # 移除HTML标签进行匹配
        clean_model_name = model_name
        if "<a href=" in model_name:
            # 提取链接中的文本
            import re

            match = re.search(r">([^<]+)<", model_name)
            if match:
                clean_model_name = match.group(1)

        for model in self.data["models"]:
            if model["name"] == clean_model_name:
                data = []
                for level, level_data in model["results"].items():
                    for subcat, subcat_data in level_data["subcategories"].items():
                        data.append(
                            {
                                "Level": level,
                                "Subcategory": subcat,
                                "Accuracy": self._format_accuracy(
                                    subcat_data["accuracy"]
                                ),
                            }
                        )
                return pd.DataFrame(data)
        return pd.DataFrame()


def create_leaderboard():
    """创建排行榜Gradio界面"""

    leaderboard = SpectralLeaderboard()

    with gr.Blocks(
        title="🔬 Spectral Hub Leaderboard",
        theme=gr.themes.Default(),
        css="""
        .gradio-container {
            max-width: 1400px !important;
        }
        .dataframe table {
            border-collapse: collapse !important;
        }
        .dataframe td, .dataframe th {
            padding: 8px 12px !important;
            border: 1px solid #e1e5e9 !important;
        }
        .dataframe th {
            background-color: #f8f9fa !important;
            font-weight: 600 !important;
        }
        .dataframe tr:nth-child(even) {
            background-color: #f8f9fa !important;
        }
        .dataframe tr:hover {
            background-color: #e8f4f8 !important;
        }
        """,
    ) as demo:
        gr.Markdown(
            """
            # 🏆 Spectral Hub Leaderboard
            
            A comprehensive benchmark for evaluating large language models on **spectroscopic analysis tasks**.
            
            📊 **Evaluation Levels**: Signal Processing, Perception, Semantic Understanding, Generation  
            🔬 **Domains**: IR, NMR, UV-Vis, Mass Spectrometry and more  
            🌟 **Multimodal**: Support for both text-only and vision-language models
            """
        )

        with gr.Row():
            info = leaderboard.data["leaderboard_info"]
            gr.Markdown(
                f"""
                **📈 Stats**: {info["total_models"]} models evaluated  
                **🏅 Rankings**: 🥇🥈🥉 medals for top performers  
                **🔗 Submit**: Send evaluation results to contribute your model!
                """
            )

        with gr.Row():
            with gr.Column(scale=2):
                model_type_filter = gr.Dropdown(
                    choices=["All", "open_source", "proprietary", "baseline"],
                    value="All",
                    label="🏷️ Model Type",
                )

            with gr.Column(scale=2):
                multimodal_filter = gr.Dropdown(
                    choices=["All", "Multimodal Only", "Text Only"],
                    value="All",
                    label="👁️ Modality",
                )

            with gr.Column(scale=2):
                sort_by = gr.Dropdown(
                    choices=[
                        "Average",
                        "Signal",
                        "Perception",
                        "Semantic",
                        "Generation",
                        "Model",
                        "Date",
                    ],
                    value="Average",
                    label="📊 Sort By",
                )

            with gr.Column(scale=1):
                ascending = gr.Checkbox(value=False, label="⬆️ Ascending")

            with gr.Column(scale=1):
                refresh_btn = gr.Button("🔄 Refresh", variant="secondary")

        # 主排行榜表格
        leaderboard_table = gr.Dataframe(
            value=leaderboard.get_leaderboard_df(),
            interactive=False,
            wrap=True,
            datatype=["html"] * 12,
            column_widths=[
                "6%",
                "5%",
                "18%",
                "8%",
                "5%",
                "10%",
                "10%",
                "10%",
                "10%",
                "10%",
                "16%",
                "10%",
            ],
            label="🏆 Model Rankings",
        )

        # 模型详细信息
        with gr.Accordion("📋 Model Details", open=False):
            model_select = gr.Dropdown(
                choices=[model["name"] for model in leaderboard.data["models"]],
                label="Select Model for Details",
            )

            with gr.Row():
                with gr.Column():
                    subcategory_table = gr.Dataframe(label="📊 Subcategory Results")

                with gr.Column():
                    model_info = gr.Markdown(label="ℹ️ Model Information")

        # 图例说明
        with gr.Accordion("📖 Legend & Info", open=False):
            gr.Markdown(
                """
                ### 🔍 Column Explanations
                
                - **Rank**: 🥇 1st place, 🥈 2nd place, 🥉 3rd place, then numbers
                - **Type**: 🔓 Open Source, 🔒 Proprietary, 📊 Baseline
                - **MM**: 👁️ Multimodal, 📝 Text-only  
                - **Average**: Average accuracy across all evaluated levels
                - **Signal**: Low-level signal processing tasks
                - **Perception**: Mid-level feature extraction tasks  
                - **Semantic**: High-level understanding tasks
                - **Generation**: Spectrum generation tasks
                
                ### 📝 Notes
                - "-" indicates the model was not evaluated on that benchmark
                - Rankings are based on average performance across evaluated tasks
                - Multimodal models can process both text and images
                - Click on model names and submitters to visit their pages
                """
            )

        def update_leaderboard(model_type, multimodal, sort_by_val, asc):
            """更新排行榜"""
            return leaderboard.get_leaderboard_df(
                model_type_filter=model_type,
                multimodal_filter=multimodal,
                sort_by=sort_by_val,
                ascending=asc,
            )

        def update_model_details(model_name):
            """更新模型详细信息"""
            if not model_name:
                return pd.DataFrame(), ""

            # 获取子类别详情
            subcategory_df = leaderboard.get_subcategory_details(model_name)

            # 获取模型基本信息
            for model in leaderboard.data["models"]:
                if model["name"] == model_name:
                    info_md = f"""
                    ### {model["name"]}
                    
                    **👤 Submitter**: {model["submitter"]}  
                    **📅 Submission**: {model["submission_time"][:10] if model["submission_time"] else "Unknown"}  
                    **🏷️ Type**: {model["model_type"]}  
                    **📏 Size**: {model["model_size"]}  
                    **👁️ Multimodal**: {"Yes" if model["is_multimodal"] else "No"}  
                    
                    **📝 Description**: {model["model_info"]["description"]}
                    
                    **🔗 Links**:  
                    - [Homepage]({model["model_info"]["homepage"]}) {model["model_info"]["homepage"]}
                    - [Paper]({model["model_info"]["paper"]}) {model["model_info"]["paper"]}  
                    - [Code]({model["model_info"]["code"]}) {model["model_info"]["code"]}
                    """
                    return subcategory_df, info_md

            return pd.DataFrame(), ""

        # 事件绑定
        for component in [model_type_filter, multimodal_filter, sort_by, ascending]:
            component.change(
                fn=update_leaderboard,
                inputs=[model_type_filter, multimodal_filter, sort_by, ascending],
                outputs=[leaderboard_table],
            )

        refresh_btn.click(
            fn=update_leaderboard,
            inputs=[model_type_filter, multimodal_filter, sort_by, ascending],
            outputs=[leaderboard_table],
        )

        model_select.change(
            fn=update_model_details,
            inputs=[model_select],
            outputs=[subcategory_table, model_info],
        )

    return demo


if __name__ == "__main__":
    app = create_leaderboard()
    print("🚀 Starting Spectral Hub Leaderboard...")
    app.launch(
        server_name="0.0.0.0",
        share=True,
        show_api=False,
        inbrowser=True,
    )

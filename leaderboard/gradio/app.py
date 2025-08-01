import gradio as gr
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Optional


class SpectralLeaderboard:
    def __init__(self, data_file: str = "../leaderboard_v_1.0.json"):
        # 获取当前脚本的目录
        current_dir = Path(__file__).parent
        # 构建正确的数据文件路径
        if data_file.startswith("../"):
            self.data_file = current_dir.parent / data_file[3:]
        else:
            self.data_file = Path(data_file)

        print(f"🔍 Looking for data file at: {self.data_file}")
        print(f"📂 Current working directory: {Path.cwd()}")
        print(f"📄 Script location: {Path(__file__).parent}")
        print(f"✅ Data file exists: {self.data_file.exists()}")

        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """加载排行榜数据"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(
                    f"✅ Successfully loaded {data['leaderboard_info']['total_models']} models from {self.data_file}"
                )
                return data
        except FileNotFoundError:
            print(
                f"❌ Data file {self.data_file} not found. Creating empty leaderboard."
            )
            return {"leaderboard_info": {"total_models": 0}, "models": []}
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return {"leaderboard_info": {"total_models": 0}, "models": []}

    def _format_accuracy(self, accuracy: Optional[float]) -> str:
        """格式化准确率显示"""
        if accuracy is None:
            return "-"
        return f"{accuracy:.1f}"

    def _calculate_average(self, results: Dict) -> Optional[float]:
        """计算平均准确率，使用overall_accuracy字段"""
        return results.get("overall_accuracy")

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
        sort_by: str = "Overall",
        ascending: bool = False,
    ) -> pd.DataFrame:
        """生成排行榜DataFrame"""

        models = self.data.get("models", [])
        print(f"📊 Processing {len(models)} models")

        # 筛选模型
        filtered_models = []
        for model in models:
            # 模型类型筛选
            if (
                model_type_filter != "All"
                and model.get("model_type", "") != model_type_filter
            ):
                continue

            # 多模态筛选
            if multimodal_filter == "Multimodal Only" and not model.get(
                "is_multimodal", False
            ):
                continue
            elif multimodal_filter == "Text Only" and model.get("is_multimodal", False):
                continue

            filtered_models.append(model)

        print(f"🔍 After filtering: {len(filtered_models)} models")

        # 构建DataFrame数据
        data = []
        for model in filtered_models:
            try:
                results = model.get("results", {})

                # 获取各项准确率
                overall_accuracy = self._calculate_average(results)
                signal_acc = results.get("Signal", {}).get("accuracy")
                perception_acc = results.get("Perception", {}).get("accuracy")
                semantic_acc = results.get("Semantic", {}).get("accuracy")
                generation_acc = results.get("Generation", {}).get("accuracy")

                # 创建带链接的模型名和提交者
                model_name_display = self._create_link(
                    model.get("name", "Unknown"), model.get("name_link", "")
                )
                submitter_display = self._create_link(
                    model.get("submitter", "Unknown"), model.get("submitter_link", "")
                )

                row = {
                    "Type": self._get_model_type_icon(
                        model.get("model_type", "unknown")
                    ),
                    "Model": model_name_display,
                    "Size": model.get("model_size", "Unknown"),
                    "MM": self._get_multimodal_icon(model.get("is_multimodal", False)),
                    "Overall": self._format_accuracy(overall_accuracy),
                    "Signal": self._format_accuracy(signal_acc),
                    "Perception": self._format_accuracy(perception_acc),
                    "Semantic": self._format_accuracy(semantic_acc),
                    "Generation": self._format_accuracy(generation_acc),
                    "Submitter": submitter_display,
                    "Date": (
                        model.get("submission_time", "")[:10]
                        if model.get("submission_time")
                        else "-"
                    ),
                    # 用于排序的数值列
                    "overall_val": overall_accuracy or 0,
                    "signal_val": signal_acc or 0,
                    "perception_val": perception_acc or 0,
                    "semantic_val": semantic_acc or 0,
                    "generation_val": generation_acc or 0,
                }
                data.append(row)
            except Exception as e:
                print(f"⚠️ Error processing model {model.get('name', 'Unknown')}: {e}")
                continue

        df = pd.DataFrame(data)
        print(f"📋 Created DataFrame with {len(df)} rows")

        if len(df) == 0:
            print("📋 Empty DataFrame, returning empty table")
            return pd.DataFrame(
                columns=[
                    "Rank",
                    "Type",
                    "Model",
                    "Size",
                    "MM",
                    "Overall",
                    "Signal",
                    "Perception",
                    "Semantic",
                    "Generation",
                    "Submitter",
                    "Date",
                ]
            )

        # 排序
        sort_mapping = {
            "Overall": "overall_val",
            "Signal": "signal_val",
            "Perception": "perception_val",
            "Semantic": "semantic_val",
            "Generation": "generation_val",
            "Model": "Model",
            "Date": "Date",
        }

        sort_col = sort_mapping.get(sort_by, "overall_val")
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
            "Overall",
            "Signal",
            "Perception",
            "Semantic",
            "Generation",
            "Submitter",
            "Date",
        ]
        result_df = df[display_columns]
        print(f"✅ Returning DataFrame with {len(result_df)} rows")
        return result_df

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

        for model in self.data.get("models", []):
            if model.get("name") == clean_model_name:
                data = []
                results = model.get("results", {})
                for level, level_data in results.items():
                    if level == "overall_accuracy":  # 跳过总体准确率字段
                        continue

                    subcategories = level_data.get("subcategories", {})
                    for subcat, subcat_data in subcategories.items():
                        data.append(
                            {
                                "Level": level,
                                "Subcategory": subcat,
                                "Accuracy": self._format_accuracy(
                                    subcat_data.get("accuracy")
                                ),
                            }
                        )
                return pd.DataFrame(data)
        return pd.DataFrame()


def create_leaderboard():
    """创建排行榜Gradio界面"""

    leaderboard = SpectralLeaderboard()

    with gr.Blocks(
        title="🔬 SpectrumLab Leaderboard",
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
            # 🏆 SpectrumLab Leaderboard
            
            A comprehensive benchmark for evaluating large language models on **spectroscopic analysis tasks**.
            
            📊 **Evaluation Levels**: Signal Processing, Perception, Semantic Understanding, Generation  
            🔬 **Domains**: IR, NMR, UV-Vis, Mass Spectrometry and more  
            🌟 **Multimodal**: Support for both text-only and vision-language models
            """
        )

        with gr.Row():
            info = leaderboard.data.get("leaderboard_info", {"total_models": 0})
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
                        "Overall",
                        "Signal",
                        "Perception",
                        "Semantic",
                        "Generation",
                        "Model",
                        "Date",
                    ],
                    value="Overall",
                    label="📊 Sort By",
                )

            with gr.Column(scale=1):
                ascending = gr.Checkbox(value=False, label="⬆️ Ascending")

            with gr.Column(scale=1):
                refresh_btn = gr.Button("🔄 Refresh", variant="secondary")

        # 主排行榜表格
        initial_df = leaderboard.get_leaderboard_df()
        leaderboard_table = gr.Dataframe(
            value=initial_df,
            interactive=False,
            wrap=True,
            datatype=["html"] * len(initial_df.columns)
            if len(initial_df.columns) > 0
            else ["html"] * 12,
            column_widths=(
                [
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
                ]
                if len(initial_df.columns) > 0
                else None
            ),
            label="🏆 Model Rankings",
        )

        # 模型详细信息
        with gr.Accordion("📋 Model Details", open=False):
            model_choices = [
                model.get("name", "Unknown")
                for model in leaderboard.data.get("models", [])
            ]
            model_select = gr.Dropdown(
                choices=model_choices,
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
                - **Overall**: Average accuracy across all evaluated levels
                - **Signal**: Low-level signal processing tasks
                - **Perception**: Mid-level feature extraction tasks
                - **Semantic**: High-level understanding tasks
                - **Generation**: Spectrum generation tasks
                
                ### 📝 Notes
                - "-" indicates the model was not evaluated on that benchmark
                - Rankings are based on overall performance across all evaluated tasks
                - Multimodal models can process both text and spectroscopic images
                - Click on model names and submitters to visit their pages
                
                ### 📊 Task Categories
                
                **Signal Level:**
                - Spectrum Type Classification (TC)
                - Spectrum Quality Assessment (QE)
                - Basic Feature Extraction (FE)
                - Impurity Peak Detection (ID)
                
                **Perception Level:**
                - Functional Group Recognition (GR)
                - Elemental Compositional Prediction (EP)
                - Peak Assignment (PA)
                - Basic Property Prediction (PP)
                
                **Semantic Level:**
                - Molecular Structure Elucidation (SE)
                - Fusing Spectroscopic Modalities (FM)
                - Multimodal Molecular Reasoning (MR)
                
                **Generation Level:**
                - Forward Problems (FP)
                - Inverse Problems (IP)
                - De Novo Generation (DnG)
                """
            )

        def update_leaderboard(model_type, multimodal, sort_by_val, asc):
            """更新排行榜"""
            print(
                f"🔄 Updating leaderboard with filters: {model_type}, {multimodal}, {sort_by_val}, {asc}"
            )
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
            for model in leaderboard.data.get("models", []):
                if model.get("name") == model_name:
                    # 处理链接显示
                    def format_link(name, url):
                        if url and url.strip():
                            return f"[{name}]({url})"
                        return "Not provided"

                    model_info_dict = model.get("model_info", {})
                    results = model.get("results", {})

                    info_md = f"""
                    ### {model.get("name", "Unknown")}
                    
                    **👤 Submitter**: {model.get("submitter", "Unknown")}  
                    **📅 Submission**: {model.get("submission_time", "")[:10] if model.get("submission_time") else "Unknown"}  
                    **🏷️ Type**: {model.get("model_type", "Unknown")}  
                    **📏 Size**: {model.get("model_size", "Unknown")}  
                    **👁️ Multimodal**: {"Yes" if model.get("is_multimodal", False) else "No"}  
                    
                    **📝 Description**: {model_info_dict.get("description", "") or "No description provided"}
                    
                    **🔗 Links**:  
                    - **Homepage**: {format_link("Visit", model_info_dict.get("homepage", ""))}
                    - **Paper**: {format_link("Read", model_info_dict.get("paper", ""))}  
                    - **Code**: {format_link("View", model_info_dict.get("code", ""))}
                    
                    **📊 Performance Summary**:
                    - **Overall**: {leaderboard._format_accuracy(results.get("overall_accuracy"))}%
                    - **Signal**: {leaderboard._format_accuracy(results.get("Signal", {}).get("accuracy"))}%
                    - **Perception**: {leaderboard._format_accuracy(results.get("Perception", {}).get("accuracy"))}%
                    - **Semantic**: {leaderboard._format_accuracy(results.get("Semantic", {}).get("accuracy"))}%
                    - **Generation**: {leaderboard._format_accuracy(results.get("Generation", {}).get("accuracy"))}%
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
    print("🚀 Starting SpectrumLab Leaderboard...")
    app.launch(
        server_name="0.0.0.0",
        share=True,
        show_api=False,
        inbrowser=True,
    )

# Tutorial

Welcome to use SpectrumLab! This tutorial will help you quickly understand spectroscopy analysis, the SpectrumLab platform, and how to use it to evaluate the performance of large language models on spectroscopy tasks.

## What is spectroscopy?

Spectroscopy is a branch of science that studies the interaction between matter and electromagnetic radiation. By analyzing the spectra of absorption, emission, or scattering of matter, we can obtain detailed information about the structure, composition, and properties of matter.

## The importance of spectroscopy

Spectroscopy plays an important role in modern science. By analyzing the interaction between matter and electromagnetic radiation, it provides a key means to understand the composition, structure, and properties of matter. In chemistry, spectroscopy is used for molecular structure analysis and reaction mechanism research. In materials science, it can characterize nanomaterials and conduct surface analysis. In biology, it is used to study protein folding and metabolite detection. At the same time, spectroscopy is also widely used in clinical medicine. For example, non-invasive diagnosis and early disease detection can be achieved through spectroscopic techniques, making it an indispensable tool in modern scientific research and applications.

## Common spectroscopic techniques

- **Infrared spectrum（IR）**：Analyze molecular vibrations and identify functional groups. The characteristic absorption peaks in the IR spectrum (such as C=O, O–H, C–H, etc.) are iconic within the characteristic frequency range and are the core tools for determining functional groups.
- **Nuclear Magnetic Resonance（NMR）**：Provide information about the atomic environment and structural connectivity in a molecule through chemical shift, signal intensity, and coupling constants, which is often used to determine the molecular structure (especially for organic compounds).
- **Ultraviolet - Visible Spectroscopy（UV-Vis）**：Study the electronic transitions and conjugated systems of molecules, especially for determining the electronic structure, conjugation length, and optical properties, without directly providing structural connectivity information.
- **Mass Spectrometry (MS)**：Determining the molecular weight and inferring the molecular structure through fragment combination are important tools for determining the molecular composition and secondary structure.
- **Raman spectroscopy (Raman)**：Provides molecular vibration information, can identify chemical bond vibrations similar to IR, is particularly sensitive to symmetric molecules and non - polar bonds, and is often used as a complementary method to IR.
- **HSQC spectrum**：A two-dimensional NMR (^1H–^13C or ^1H–^15N) experiment where each cross peak represents a directly bonded proton-heteroatom pair. It can be used to unambiguously assign ^1H–^13C (or ^15N) one-bond correlations, assist in peak assignment, and structure elucidation.

## What is SpectrumLab？

### Overview

SpectrumLab is a groundbreaking unified platform and comprehensive toolkit designed to accelerate and systematize deep learning research in the field of chemical spectroscopy. It aims to streamline the entire AI - driven spectroscopy research lifecycle, from data pre - processing to model evaluation. It provides researchers and developers with a modular, scalable, and easy - to - use ecosystem of Python libraries and tools to drive artificial intelligence research and applications in the field of spectroscopy.

### Core functions

#### Modular and extensible architecture

SpectrumLab Adopt a flexible modular design, and its core components include:

- **Benchmark Group**：Hierarchically organize the SpectrumBench dataset to support multiple spectral modalities and task types, and allow users to flexibly combine according to their needs to create customized evaluation tasks.
- **Model Integration**：Provide a unified framework and standardized API that can seamlessly integrate and evaluate various external models, whether they are commercial closed - source models (such as GPT - 4o) or open - source models deployed locally.
- **Evaluator**：As the core of the evaluation engine, it supports the customization of evaluation indicators and protocols according to different tasks (such as multiple-choice questions, generation questions), ensuring the rigor of evaluation and task adaptability.

#### A comprehensive toolchain ecosystem

Provide a Python library distributed through PyPI that integrates core modules such as data processing, model development, automatic evaluation, and visualization, greatly simplifying the entire research workflow.

#### SpectrumAnnotator

It is closely integrated with the innovative SpectrumAnnotator component, which can utilize the reasoning capabilities of advanced multimodal large models to automatically generate high-quality and diverse benchmark test data from the seed dataset, and efficiently build evaluation tasks.

#### Leaderboards

To ensure transparency and reproducibility, SpectrumLab has established a public leaderboard system. This system systematically tracks and compares the performance of various models on all 14 tasks, promoting fair competition and the common progress of the field.

## Related links

- [API Reference](/zh/api) - Understand the detailed interface description and code examples
- [Benchmark test](/zh/benchmark) - View the details of evaluation metrics and the dataset
- [Leaderboard](https://huggingface.co/spaces/SpectrumWorld/SpectrumLeaderboard) - View the comparison of model performance

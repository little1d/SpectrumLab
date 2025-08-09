# Benchmark 
## Benchmark Overview

The Benchmark of SpectrumLab adopts a hierarchical architecture design, comprehensively evaluating the model's capabilities in spectroscopy tasks from signal processing to advanced semantic understanding. The benchmark test consists of four main levels, with each level containing multiple sub - tasks, suitable for different types of spectral analysis.

## Benchmark Details

### 1. Signal layer（Signal Level）

Basic spectral signal processing and analysis, including the following subtasks:

- **Spectrum Type Classification**：Identify different types of spectra (infrared, nuclear magnetic resonance, Raman, etc.).
- **Spectrum Quality Assessment**：Identify whether the spectrogram is clear, complete, and whether there is obvious noise.
- **Basic Feature Extraction**：Identify basic features such as baselines, peaks, peak positions, and peak intensities in the spectrogram.
- **Impurity Peak Detection**：Identify impurity peaks and abnormal signals in the spectrogram.

### 2. Perception Level

Further spectral visual understanding and pattern recognition, covering:

- **Basic Property Prediction**：Predict properties directly related to molecular ion peaks, solubility, acidity and alkalinity based on spectral graph features.
- **Elemental Compositional Prediction**：Identify elemental composition and isotope patterns from mass spectrometry, etc.
- **Functional Group Recognition**：Predict the possible functional groups of a molecule based on spectral characteristics (especially characteristic peak positions).
- **Peak Assignment**：Preliminarily assign the main peaks in the spectrum to corresponding chemical groups.

### 3. Semantic Level

Deep spectral semantic understanding and chemical knowledge reasoning, including:

- **Fusing Spectroscopic Modalitie）**：Make comprehensive judgments by combining multiple spectral or molecular information.
- **Molecular Structure Elucidation**：Match the correct molecular structure from multiple candidates based on spectral information.
- **Multimodal Molecular Reasoning**：Conduct complex chemical reasoning and answering based on spectral and textual information.

### 4. Generation Level

Generate new chemical information creatively. The main tasks are:

- **Forward Problems**：Infer the molecular structure from spectra, SMILES, or a combination of both.
- **Inverse Problems**：Generate spectra, SMILES, etc. for molecular structures.
- **De Novo Generation**：Generate novel, diverse, and reasonable molecular structures (SMILES, 2D diagrams) and/or predicted multimodal information (spectra, properties) from scratch according to specific targets, such as molecules with specific properties or ligands for specific targets.

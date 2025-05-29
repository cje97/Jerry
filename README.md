# Intelligent Variant (VCF) Annotation Tool with Interactive Dashboard

## Description

This tool provides a fast and intelligent way to annotate Variant Call Format (VCF) files. It aims to reduce annotation time significantly and provide an interactive dashboard for visualizing and prioritizing variants. This tool is being developed with organizations like Génome Québec in mind.

## Features

### Core Features
*   VCF file upload.
*   Annotation with ClinVar and gnomAD.
*   Simple filtering (e.g., by gnomAD frequency and ClinVar status).
*   Basic Streamlit interface for upload, initiating annotation, displaying results (simple table), and export.

### "Wow" Features (Planned)
*   **AI Prioritization:** A scoring system to prioritize variants (can start as rule-based).
*   **Interactive Dashboard:** Advanced visualizations (e.g., variant types, frequencies).
*   **Expanded Database Integration:** dbSNP, COSMIC, etc.
*   **PDF Report Generation:** For clinical transferability.
*   **REST API:** For programmatic access to annotation features.

## Tech Stack
*   Python (Flask/FastAPI for backend/API)
*   Streamlit (or Dash) for the frontend
*   SQLite (for caching)
*   Docker (for containerization)
*   Streamlit Cloud (for deployment)

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```
Then, open your browser and navigate to the URL provided by Streamlit to upload your VCF file and start the annotation.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details. (Note: A `LICENSE` file will be added later).

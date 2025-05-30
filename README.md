# deepQC: A Bioinformatics Quality Control Pipeline

## Overview

`deepQC` is a bioinformatics pipeline designed for comprehensive quality control (QC) and preliminary analysis of genome assemblies. It integrates several standard bioinformatics tools to assess assembly quality, completeness, contamination, annotation, and more. The pipeline primarily uses Bash for orchestration (`run_deepqc.sh`) and Python for generating an interactive HTML summary report (`report.py`).

It is designed with High-Performance Computing (HPC) environments in mind, leveraging Conda and Bioconda for robust dependency management. An example Slurm submission script is provided to facilitate deployment on clusters.

## Features

*   **Comprehensive QC**: Integrates multiple tools for a holistic view of assembly quality.
*   **Automated Workflow**: Orchestrated via a main Bash script (`run_deepqc.sh`).
*   **Interactive Reporting**: Generates a dynamic HTML report using Python with Plotly and Jinja2, summarizing key findings and visualizations.
*   **Reproducibility**: Packaged with Conda/Bioconda for consistent environments (`environment.yml`).
*   **HPC Ready**: Includes an example Slurm submission script (`deepqc_job.sbatch`) for easy deployment on compute clusters.
*   **Modular Design**: Output directories are organized by tool, making it easy to inspect individual results.

## Tools Included

The pipeline utilizes the following bioinformatics tools:

| Step                      | Tool                       | Usage                                      |
| :------------------------ | :------------------------- | :----------------------------------------- |
| Assembly Quality          | QUAST                      | N50, L50, # contigs, total length, GC%, etc. |
| Genome Completeness       | BUSCO                      | Percentage of universal single-copy orthologs found |
| Contamination/Taxonomy    | Kraken2                    | Taxonomic classification and abundance estimation |
| Annotation (Prokaryotic)  | Prokka                     | Predicts CDS, rRNA, tRNA, and other features |
| Pangenome Analysis        | Roary                      | Core, accessory, and unique genes (for multiple genomes) |
| Whole Genome Alignment    | ProgressiveMauve           | Synteny and structural variant analysis (for multiple genomes) |
| Reporting                 | Python (Plotly + Jinja2)   | Generates an interactive HTML summary report |

## Installation

### Prerequisites

*   **Conda / Miniconda**: Ensure you have Conda or Miniconda installed. If not, you can download it from [here](https://docs.conda.io/en/latest/miniconda.html).

### Steps

1.  **Clone the repository**:
    ```bash
    git clone https://your-repository-url/deepQC.git # Replace with actual repository URL
    cd deepQC
    ```

2.  **Create and activate Conda environment**:
    This will install all necessary tools and Python libraries defined in `environment.yml`.
    ```bash
    conda env create -f environment.yml
    conda activate deepQC
    ```
    *Note: The environment creation might take some time as it downloads and installs several packages.*

3.  **Make scripts executable**:
    (The scripts `run_deepqc.sh` and `report.py` should already be executable if you followed previous steps in the development, but it's good practice to ensure.)
    ```bash
    chmod +x run_deepqc.sh report.py
    ```

## Usage

### Direct Execution (`run_deepqc.sh`)

The main pipeline script `run_deepqc.sh` orchestrates all the bioinformatics tool executions.

**Command Syntax**:
```bash
bash run_deepqc.sh <input_fasta_dir> <output_dir> <threads>
```

*   `input_fasta_dir`: Path to the directory containing your input FASTA files (e.g., `*.fasta`, `*.fna`, `*.fa`).
*   `output_dir`: Path to the directory where all results will be stored. This directory will be created if it doesn't exist.
*   `threads`: Number of threads to use for multi-threaded tools.

**Example**:
```bash
bash run_deepqc.sh /data/my_genomes /results/deepqc_run_01 16
```

### HPC Job Submission (Slurm Example)

For running on an HPC cluster using Slurm, a template submission script `deepqc_job.sbatch` is provided.

1.  **Modify `deepqc_job.sbatch`**:
    You **must** edit this file to set:
    *   `INPUT_FASTA_DIR`: Correct path to your input FASTA files.
    *   `OUTPUT_DIR`: Correct path for your results.
    *   `THREADS`: Match this with `#SBATCH --cpus-per-task`.
    *   Conda module loading command (e.g., `module load anaconda`): This might vary based on your HPC system's configuration.
    *   Optionally, adjust SBATCH directives like `--mem`, `--time`, `--cpus-per-task` as needed.

2.  **Submit the job**:
    ```bash
    sbatch deepqc_job.sbatch
    ```
    This will queue your job, and Slurm will execute it when resources are available. Output and error logs (`deepqc-%j.out`, `deepqc-%j.err`) will be created in the submission directory.

## Output Structure

The pipeline will generate an `output_dir` (specified by you) with the following structure:

```
<output_dir>/
├── busco_results/      # BUSCO outputs for each sample
├── kraken_results/     # Kraken2 outputs for each sample
├── mauve_results/      # ProgressiveMauve alignment outputs
├── prokka_results/     # Prokka annotation outputs for each sample
├── quast_results/      # QUAST QC reports for each sample
├── roary_results/      # Roary pangenome analysis results (if multiple genomes)
├── deepqc_report.html  # Final interactive HTML summary report
└── *.log               # Logs from the main script and potentially report generation
```

Each tool-specific subdirectory will contain the native output files generated by that tool for each input sample. The `deepqc_report.html` provides a summary and visualizations from these results.

## Snakemake Integration (Future Work)

While `run_deepqc.sh` provides basic orchestration, this pipeline could be enhanced by converting it into a `Snakefile`. This would offer more advanced workflow management features, such as:
*   Better dependency handling between jobs.
*   Improved parallelization and resource management on HPCs.
*   Easier re-running of specific parts of the pipeline (e.g., if only one input file changes).
*   Enhanced portability and reproducibility.

The `environment.yml` already includes `snakemake` as an optional dependency for users interested in this.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please:
1.  Open an issue to discuss the changes.
2.  Fork the repository and create a new branch for your feature.
3.  Submit a pull request with a clear description of your changes.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details (if one is added, otherwise assume MIT).

#!/usr/bin/env bash
#SBATCH --job-name=deepQC
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=12:00:00       # Adjust time based on expected runtime
#SBATCH --output=deepqc-%j.out # Standard output log, %j is the job ID
#SBATCH --error=deepqc-%j.err  # Standard error log

# --- User specific parameters ---
# IMPORTANT: Replace these paths with your actual data locations.
# Path to the directory containing your input FASTA files.
INPUT_FASTA_DIR="/path/to/your/genomes" 
# Path to the directory where all results will be stored.
OUTPUT_DIR="/path/to/your/results"
# Number of threads for multi-threaded tools. 
# Ideally, this should match --cpus-per-task requested above for efficiency.
THREADS=16
# --- End User specific parameters ---

echo "------------------------------------"
echo "Starting deepQC Slurm Job"
echo "Job ID: $SLURM_JOB_ID"
echo "Hostname: $(hostname)"
echo "------------------------------------"

# --- Environment Setup ---

# Load Conda module
# The exact command to load Conda/Anaconda can vary between HPC systems.
# Common examples: 'module load anaconda', 'module load anaconda3', 'module load miniconda'.
# Check your HPC's documentation or use 'module avail' to find the correct module name.
echo "Loading Conda module..."
module load anaconda # Adjust this line if necessary for your HPC system
if [ $? -ne 0 ]; then
    echo "Error: Failed to load Conda module. Please check the module name and availability."
    exit 1
fi
echo "Conda module loaded."

# Activate the Conda environment
# Option 1: If the environment was created with '--prefix ./env' in the project directory.
# This makes the environment self-contained within your project.
ENV_PATH="./environment.yml" # Path to your environment file, assuming it's named 'environment.yml'
ENV_NAME="deepQC"            # Name of the environment as defined in environment.yml

# It's good practice to ensure the environment yml file exists where expected.
if [ ! -f "$ENV_PATH" ]; then
    echo "Error: Conda environment file '$ENV_PATH' not found in $(pwd)."
    echo "Please ensure the environment.yml is in the correct location."
    exit 1
fi

# Activate by name. If you created the environment globally or by name (e.g., `conda env create -f environment.yml`)
echo "Activating deepQC Conda environment by name '$ENV_NAME'..."
conda activate $ENV_NAME

# Check if environment activation was successful
# $CONDA_DEFAULT_ENV should be the name of the activated environment.
# Some systems might use $CONDA_PREFIX to point to the path.
if [ -z "$CONDA_DEFAULT_ENV" ] || [[ "$CONDA_DEFAULT_ENV" != *"$ENV_NAME"* ]]; then
    echo "Error: Failed to activate Conda environment '$ENV_NAME'."
    echo "Attempted to activate '$ENV_NAME'. Currently active: '$CONDA_DEFAULT_ENV'."
    echo "Please ensure the environment '$ENV_NAME' exists and was created correctly from '$ENV_PATH'."
    echo "You can check available environments with 'conda env list'."
    exit 1
fi
echo "Conda environment '$CONDA_DEFAULT_ENV' activated successfully."
echo "Conda prefix: $CONDA_PREFIX"


# Navigate to the submission directory (where sbatch was run from)
# This is good practice as it ensures that relative paths (like for run_deepqc.sh) are correct.
echo "Changing to Slurm submission directory: $SLURM_SUBMIT_DIR"
cd "$SLURM_SUBMIT_DIR" || { echo "Error: Failed to change to $SLURM_SUBMIT_DIR"; exit 1; }
echo "Current working directory: $(pwd)"


# --- Log User Parameters ---
echo "------------------------------------"
echo "User Parameters:"
echo "Input FASTA directory: $INPUT_FASTA_DIR"
echo "Output directory:      $OUTPUT_DIR"
echo "Number of threads:     $THREADS"
echo "------------------------------------"


# --- Sanity Checks ---
# Check if the main pipeline script exists and is executable
PIPELINE_SCRIPT="run_deepqc.sh"
if [ ! -f "$PIPELINE_SCRIPT" ]; then
    echo "Error: Pipeline script '$PIPELINE_SCRIPT' not found in $(pwd)."
    echo "Make sure you are submitting the job from the root of the DeepQC repository."
    exit 1
fi
if [ ! -x "$PIPELINE_SCRIPT" ]; then
    echo "Error: Pipeline script '$PIPELINE_SCRIPT' is not executable."
    echo "Please make it executable by running: chmod +x $PIPELINE_SCRIPT"
    exit 1
fi
echo "Pipeline script '$PIPELINE_SCRIPT' found and is executable."

# Check if input directory exists
if [ ! -d "$INPUT_FASTA_DIR" ]; then
    echo "Error: Input FASTA directory '$INPUT_FASTA_DIR' does not exist."
    echo "Please verify the INPUT_FASTA_DIR path in this sbatch script."
    exit 1
fi
echo "Input FASTA directory '$INPUT_FASTA_DIR' found."

# --- Launch the Pipeline ---
echo "------------------------------------"
echo "Launching DeepQC pipeline (run_deepqc.sh)..."
echo "Command: bash $PIPELINE_SCRIPT \"$INPUT_FASTA_DIR\" \"$OUTPUT_DIR\" \"$THREADS\""
echo "------------------------------------"

bash "$PIPELINE_SCRIPT" "$INPUT_FASTA_DIR" "$OUTPUT_DIR" "$THREADS"
PIPELINE_EXIT_STATUS=$? # Capture the exit status of the pipeline

# --- Post-Execution ---
if [ $PIPELINE_EXIT_STATUS -eq 0 ]; then
    echo "------------------------------------"
    echo "DeepQC pipeline completed successfully."
    echo "Output results are in: $OUTPUT_DIR"
    echo "------------------------------------"
else
    echo "------------------------------------"
    echo "Error: DeepQC pipeline failed with exit status: $PIPELINE_EXIT_STATUS."
    echo "Check the error log: deepqc-$SLURM_JOB_ID.err"
    echo "Also check tool-specific logs within the output directory: $OUTPUT_DIR"
    echo "------------------------------------"
    exit $PIPELINE_EXIT_STATUS # Exit with the pipeline's error code
fi

echo "Slurm job finished."
exit 0

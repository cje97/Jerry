#!/usr/bin/env python3

import argparse
import os
import pandas as pd
import plotly.express as px
from jinja2 import Environment, FileSystemLoader, select_autoescape # FileSystemLoader if template is separate

# --- Placeholder Parsing Functions ---

def parse_quast_output(quast_dir):
    """
    Parses QUAST output.
    For now, returns a placeholder DataFrame.
    Actual implementation will read 'report.tsv' or similar.
    """
    print(f"Parsing QUAST output from {quast_dir}...")
    # In a real scenario, you'd find the relevant report file (e.g., report.tsv)
    # for each sample within quast_dir and concatenate them.
    # Example:
    # report_file = os.path.join(quast_dir, "some_sample_specific_dir", "report.tsv")
    # if os.path.exists(report_file):
    #     return pd.read_csv(report_file, sep='\t')
    # else:
    #     print(f"Warning: QUAST report not found in {quast_dir}")
    #     return pd.DataFrame({'Metric': ['N50', 'Total length'], 'Value': [0, 0]})
    
    # Simplified placeholder for multiple samples:
    data = []
    for item in os.listdir(quast_dir):
        sample_dir = os.path.join(quast_dir, item)
        if os.path.isdir(sample_dir):
            # In reality, you'd look for a specific report file like 'report.tsv'
            # For this placeholder, we just simulate some data
            print(f"  Simulating QUAST data for sample: {item}")
            data.append({'Sample': item, 'N50': 50000, 'Total length': 4000000, '# contigs': 10})
    if not data:
        return pd.DataFrame(columns=['Sample', 'N50', 'Total length', '# contigs'])
    return pd.DataFrame(data)


def parse_busco_output(busco_dir):
    """
    Parses BUSCO output.
    For now, returns a placeholder DataFrame.
    Actual implementation will read 'short_summary.specific.<lineage>.<sample>.txt'.
    """
    print(f"Parsing BUSCO output from {busco_dir}...")
    busco_data_list = []
    for item in os.listdir(busco_dir):
        sample_dir = os.path.join(busco_dir, item)
        if os.path.isdir(sample_dir):
            summary_file = None
            for f in os.listdir(sample_dir):
                if f.startswith("short_summary.specific.") and f.endswith(f"{item}.txt"):
                    summary_file = os.path.join(sample_dir, f)
                    break
            
            if summary_file and os.path.exists(summary_file):
                print(f"  Parsing BUSCO summary: {summary_file}")
                with open(summary_file, 'r') as f:
                    content = f.read()
                    # This is a very basic parsing, real parsing would be more robust
                    complete_buscos = "C:0.0%"
                    single_copy = "S:0.0%"
                    duplicated = "D:0.0%"
                    fragmented = "F:0.0%"
                    missing = "M:0.0%"
                    total_buscos = "n:0"

                    for line in content.splitlines():
                        if "Complete BUSCOs (C)" in line:
                            complete_buscos = line.split('\t')[1]
                        elif "Complete and single-copy BUSCOs (S)" in line:
                            single_copy = line.split('\t')[1]
                        elif "Complete and duplicated BUSCOs (D)" in line:
                            duplicated = line.split('\t')[1]
                        elif "Fragmented BUSCOs (F)" in line:
                            fragmented = line.split('\t')[1]
                        elif "Missing BUSCOs (M)" in line:
                            missing = line.split('\t')[1]
                        elif "Total searched BUSCO sets" in line:
                            total_buscos = line.split('\t')[1]
                    
                    busco_data_list.append({
                        'Sample': item,
                        'Complete': complete_buscos,
                        'Single-copy': single_copy,
                        'Duplicated': duplicated,
                        'Fragmented': fragmented,
                        'Missing': missing,
                        'Total': total_buscos
                    })
            else:
                print(f"  Warning: BUSCO summary not found for sample {item} in {sample_dir}")
                busco_data_list.append({'Sample': item, 'Complete': 'N/A', 'Total': 0})

    if not busco_data_list:
        return pd.DataFrame(columns=['Sample', 'Complete', 'Single-copy', 'Duplicated', 'Fragmented', 'Missing', 'Total'])
    return pd.DataFrame(busco_data_list)


def parse_kraken_output(kraken_dir):
    """
    Parses Kraken2 output.
    For now, returns a placeholder dictionary mapping sample name to a DataFrame.
    Actual implementation will read '*.report' files.
    """
    print(f"Parsing Kraken2 output from {kraken_dir}...")
    kraken_reports = {}
    for item in os.listdir(kraken_dir):
        if item.endswith(".report"):
            sample_name = item.replace(".report", "")
            report_file = os.path.join(kraken_dir, item)
            print(f"  Parsing Kraken2 report: {report_file}")
            # Placeholder: Simulate reading top N taxa
            # A real parser would read the Kraken2 report format correctly
            data = {
                'Percentage': [50.0, 20.0, 10.0, 5.0, 15.0],
                'Reads': [5000, 2000, 1000, 500, 1500],
                'Taxonomic Level': ['S', 'S', 'G', 'F', 'S'],
                'Taxon': ['Escherichia coli', 'Klebsiella pneumoniae', 'Enterobacter', 'Enterobacteriaceae', 'Salmonella enterica']
            }
            kraken_reports[sample_name] = pd.DataFrame(data)
        # Also consider .kraken files for direct read classifications if needed
    if not kraken_reports:
         # Return a dict with a placeholder if no reports found
        return {"no_sample": pd.DataFrame(columns=['Percentage', 'Reads', 'Taxonomic Level', 'Taxon'])}
    return kraken_reports


def parse_prokka_output(prokka_dir):
    """
    Parses Prokka output.
    For now, returns a placeholder DataFrame.
    Actual implementation will read '*.txt' or '*.tsv' summary files from each sample's Prokka directory.
    """
    print(f"Parsing Prokka output from {prokka_dir}...")
    prokka_data = []
    for sample_id in os.listdir(prokka_dir):
        sample_prokka_dir = os.path.join(prokka_dir, sample_id)
        if os.path.isdir(sample_prokka_dir):
            # Prokka produces a .txt file with summary stats, e.g., <prefix>.txt
            # For this placeholder, we look for any .txt file.
            summary_file = None
            for f in os.listdir(sample_prokka_dir):
                if f.endswith(".txt"): # This is a guess, actual file might be <prefix>.txt
                    summary_file = os.path.join(sample_prokka_dir, f)
                    break 
            
            if summary_file and os.path.exists(summary_file):
                print(f"  Parsing Prokka summary: {summary_file}")
                # Placeholder: Extract some common metrics
                # Real parsing would involve reading key-value pairs or specific lines
                stats = {'Sample': sample_id, 'CDS': 0, 'rRNA': 0, 'tRNA': 0, 'Signal Peptides': 0}
                with open(summary_file, 'r') as sf:
                    for line in sf: # Simplified parsing
                        if "CDS:" in line: stats['CDS'] = int(line.split(':')[1].strip())
                        elif "rRNA:" in line: stats['rRNA'] = int(line.split(':')[1].strip())
                        elif "tRNA:" in line: stats['tRNA'] = int(line.split(':')[1].strip())
                prokka_data.append(stats)
            else:
                print(f"  Warning: Prokka summary .txt file not found for {sample_id} in {sample_prokka_dir}")
                prokka_data.append({'Sample': sample_id, 'CDS': 'N/A'})
                
    if not prokka_data:
        return pd.DataFrame(columns=['Sample', 'CDS', 'rRNA', 'tRNA'])
    return pd.DataFrame(prokka_data)


def parse_roary_output(roary_dir):
    """
    Parses Roary output.
    For now, returns a placeholder DataFrame.
    Actual implementation will read 'summary_statistics.txt'.
    """
    print(f"Parsing Roary output from {roary_dir}...")
    summary_file = os.path.join(roary_dir, "summary_statistics.txt")
    if os.path.exists(summary_file):
        # This is a very simplified parser. Roary's summary is key: value
        data = {}
        with open(summary_file, 'r') as f:
            for line in f:
                if ":" in line:
                    key, value = line.split(":", 1)
                    data[key.strip()] = value.strip()
        return pd.DataFrame([data]) # Convert dict to DataFrame
    else:
        print(f"Warning: Roary summary_statistics.txt not found in {roary_dir}")
        return pd.DataFrame({'Core genes': [0], 'Total genes': [0]})


def parse_mauve_output(mauve_dir):
    """
    Parses ProgressiveMauve output.
    For now, returns a placeholder message.
    Actual parsing would be complex (e.g., XML output or alignment stats).
    """
    print(f"Parsing ProgressiveMauve output from {mauve_dir}...")
    # Mauve output parsing can be very complex (e.g., backbone files, LCBs)
    # For now, just acknowledge its existence.
    # Example: Check if alignment file exists
    alignment_file = os.path.join(mauve_dir, "mauve_alignment") # As per run_deepqc.sh
    if os.path.exists(alignment_file):
        return {"status": "Mauve alignment file present.", "file": alignment_file}
    else:
        print(f"Warning: Mauve alignment file not found in {mauve_dir}")
        return {"status": "Mauve alignment file not found."}

# --- Placeholder Plotting Functions ---

def create_quast_plots(quast_data):
    """Creates plots from QUAST data."""
    print("Creating QUAST plots...")
    if quast_data.empty or 'N50' not in quast_data.columns :
        print("  QUAST data is empty or N50 column missing, skipping plot.")
        return None
    fig = px.bar(quast_data, x='Sample', y='N50', title="QUAST: N50 per Sample")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def create_busco_plot(busco_data):
    """Creates a plot from BUSCO data."""
    print("Creating BUSCO plots...")
    if busco_data.empty or 'Complete' not in busco_data.columns:
        print("  BUSCO data is empty or Complete column missing, skipping plot.")
        return None
    
    # BUSCO data might have percentages as strings like "C:98.0%". Need to parse this.
    # For this placeholder, we'll assume it's already numerical or can be simplified.
    # A more robust parser would handle the 'C:xx%', 'S:xx%' format.
    # Simplified: let's try to plot 'Complete' if it exists and looks plottable.
    try:
        # Attempt to clean up percentage strings if they exist (e.g., "98.0%")
        if busco_data['Complete'].dtype == 'object':
             busco_data['Complete_numeric'] = busco_data['Complete'].str.extract(r'(\d+\.?\d*)').astype(float)
        else:
             busco_data['Complete_numeric'] = busco_data['Complete']

        fig = px.bar(busco_data, x='Sample', y='Complete_numeric', title="BUSCO: Completeness per Sample")
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    except Exception as e:
        print(f"  Error creating BUSCO plot: {e}. Data might not be in expected format.")
        return None


def create_kraken_plot(kraken_data_dict):
    """Creates plots from Kraken2 data for each sample."""
    print("Creating Kraken2 plots...")
    plots = {}
    if not kraken_data_dict or "no_sample" in kraken_data_dict:
        print("  Kraken data is empty or contains no samples, skipping plots.")
        return plots
    for sample_name, df in kraken_data_dict.items():
        if not df.empty and 'Percentage' in df.columns and 'Taxon' in df.columns:
            print(f"  Creating Kraken plot for {sample_name}")
            fig = px.bar(df.head(10), x='Taxon', y='Percentage', title=f"Kraken2: Top Taxa for {sample_name}")
            plots[sample_name] = fig.to_html(full_html=False, include_plotlyjs='cdn')
        else:
            print(f"  Kraken data for sample {sample_name} is empty or has missing columns, skipping plot.")
            plots[sample_name] = "<p>No Kraken data to plot for this sample.</p>"
    return plots


def create_prokka_plot(prokka_data):
    """Creates plots from Prokka data."""
    print("Creating Prokka plots...")
    if prokka_data.empty or 'CDS' not in prokka_data.columns:
        print("  Prokka data is empty or CDS column missing, skipping plot.")
        return None
    try:
        # Ensure CDS is numeric for plotting
        prokka_data['CDS_numeric'] = pd.to_numeric(prokka_data['CDS'], errors='coerce')
        prokka_data_cleaned = prokka_data.dropna(subset=['CDS_numeric'])
        if prokka_data_cleaned.empty:
            print("  Prokka CDS data is not numeric or all values are N/A after conversion.")
            return None
        fig = px.bar(prokka_data_cleaned, x='Sample', y='CDS_numeric', title="Prokka: CDS Count per Sample")
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    except Exception as e:
        print(f"  Error creating Prokka plot: {e}")
        return None

def create_roary_plot(roary_data):
    """Creates plots from Roary data."""
    print("Creating Roary plots...")
    if roary_data.empty or 'Core genes' not in roary_data.columns or 'Total genes' not in roary_data.columns:
        print("  Roary data is empty or key columns missing, skipping plot.")
        return None
    
    # Roary data is often a single row summary. We can display it or make a simple bar chart.
    # For this placeholder, let's try to make a bar chart of gene categories.
    try:
        # Extract relevant numbers. Ensure they are numeric.
        core_genes = pd.to_numeric(roary_data['Core genes'].iloc[0], errors='coerce')
        soft_core_genes = pd.to_numeric(roary_data.get('Soft core genes', pd.Series([0])).iloc[0], errors='coerce') # Use .get for optional columns
        shell_genes = pd.to_numeric(roary_data.get('Shell genes', pd.Series([0])).iloc[0], errors='coerce')
        cloud_genes = pd.to_numeric(roary_data.get('Cloud genes', pd.Series([0])).iloc[0], errors='coerce')
        total_genes = pd.to_numeric(roary_data['Total genes'].iloc[0], errors='coerce')

        df_plot = pd.DataFrame({
            'Category': ['Core', 'Soft Core', 'Shell', 'Cloud'],
            'Count': [core_genes, soft_core_genes, shell_genes, cloud_genes]
        }).dropna(subset=['Count'])


        if not df_plot.empty:
            fig = px.bar(df_plot, x='Category', y='Count', title=f"Roary: Pan-genome Categories (Total Genes: {total_genes})")
            return fig.to_html(full_html=False, include_plotlyjs='cdn')
        else:
            print("  Not enough numeric data for Roary plot.")
            return "<p>Roary data not available for plotting.</p>"
    except Exception as e:
        print(f"  Error creating Roary plot: {e}")
        return "<p>Error generating Roary plot.</p>"


# --- HTML Template ---
# For simplicity, keeping it as a multiline string here.
# Could be moved to a separate template.html file.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepQC Analysis Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        h1 { color: #333; }
        h2 { color: #555; border-bottom: 1px solid #eee; padding-bottom: 5px; }
        .content { margin-left: 20px; }
        .plotly-graph-div { margin-bottom: 30px; }
        table { border-collapse: collapse; width: auto; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .tool-section { margin-bottom: 40px; padding: 15px; border: 1px solid #ccc; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>DeepQC Analysis Report</h1>

    <div class="tool-section">
        <h2>Overall Summary</h2>
        <p>This report summarizes the quality control and analysis results from the DeepQC pipeline.</p>
        <p>Output directory: <code>{{ output_dir }}</code></p>
    </div>

    {% if quast_data is not none and not quast_data.empty %}
    <div class="tool-section">
        <h2>QUAST Results</h2>
        <div class="content">
            <p>QUAST (Quality Assessment Tool for Genome Assemblies) provides metrics on assembly quality.</p>
            <h3>Summary Table:</h3>
            {{ quast_data.to_html(classes='table table-striped', index=False) | safe if quast_data is not none else '<p>No QUAST data available.</p>' }}
            <h3>Plots:</h3>
            {% if quast_plot %}
                <div>{{ quast_plot | safe }}</div>
            {% else %}
                <p>No QUAST plot available.</p>
            {% endif %}
        </div>
    </div>
    {% endif %}

    {% if busco_data is not none and not busco_data.empty %}
    <div class="tool-section">
        <h2>BUSCO Results</h2>
        <div class="content">
            <p>BUSCO (Benchmarking Universal Single-Copy Orthologs) assesses genome assembly and annotation completeness.</p>
            <h3>Summary Table:</h3>
            {{ busco_data.to_html(classes='table table-striped', index=False) | safe if busco_data is not none else '<p>No BUSCO data available.</p>' }}
            <h3>Plots:</h3>
            {% if busco_plot %}
                <div>{{ busco_plot | safe }}</div>
            {% else %}
                <p>No BUSCO plot available.</p>
            {% endif %}
        </div>
    </div>
    {% endif %}

    {% if kraken_data is not none and kraken_data %}
    <div class="tool-section">
        <h2>Kraken2 Results</h2>
        <div class="content">
            <p>Kraken2 performs taxonomic classification of sequences.</p>
            {% for sample_name, plot_html in kraken_plots.items() %}
                <h3>{{ sample_name }}</h3>
                {% if kraken_data[sample_name] is not none and not kraken_data[sample_name].empty %}
                    {{ kraken_data[sample_name].head(10).to_html(classes='table table-striped', index=False) | safe }}
                {% else %}
                    <p>No data table for {{ sample_name }}.</p>
                {% endif %}
                {% if plot_html %}
                    <div>{{ plot_html | safe }}</div>
                {% else %}
                    <p>No Kraken plot for {{ sample_name }}.</p>
                {% endif %}
            {% endfor %}
        </div>
    </div>
    {% endif %}

    {% if prokka_data is not none and not prokka_data.empty %}
    <div class="tool-section">
        <h2>Prokka Results</h2>
        <div class="content">
            <p>Prokka (Rapid Prokaryotic Genome Annotation) annotates bacterial and archaeal genomes.</p>
            <h3>Summary Table:</h3>
            {{ prokka_data.to_html(classes='table table-striped', index=False) | safe if prokka_data is not none else '<p>No Prokka data available.</p>' }}
            <h3>Plots:</h3>
            {% if prokka_plot %}
                <div>{{ prokka_plot | safe }}</div>
            {% else %}
                <p>No Prokka plot available.</p>
            {% endif %}
        </div>
    </div>
    {% endif %}

    {% if roary_data is not none and not roary_data.empty %}
    <div class="tool-section">
        <h2>Roary Results</h2>
        <div class="content">
            <p>Roary (Rapid Core Gene Analysis) identifies the pan-genome from multiple prokaryotic genome annotations.</p>
            <h3>Summary Table:</h3>
            {{ roary_data.to_html(classes='table table-striped', index=False) | safe if roary_data is not none else '<p>No Roary data available.</p>' }}
            <h3>Plots:</h3>
            {% if roary_plot %}
                <div>{{ roary_plot | safe }}</div>
            {% else %}
                <p>No Roary plot available.</p>
            {% endif %}
        </div>
    </div>
    {% endif %}

    {% if mauve_data is not none %}
    <div class="tool-section">
        <h2>ProgressiveMauve Results</h2>
        <div class="content">
            <p>ProgressiveMauve performs multiple genome alignment.</p>
            <p>{{ mauve_data.status }}</p>
            {% if mauve_data.file %}
            <p>Alignment file (or related output): <code>{{ mauve_data.file }}</code></p>
            {% endif %}
            <!-- Actual Mauve visualization is complex and typically done with its own viewer -->
            <!-- Could potentially include a link to a pre-generated image or summary if available -->
        </div>
    </div>
    {% endif %}

</body>
</html>
"""

# --- Main Function ---

def main(output_dir, report_html_path):
    """
    Generates the DeepQC HTML report.
    """
    print(f"Starting report generation. Output directory: {output_dir}")

    # Define tool output subdirectories
    quast_dir = os.path.join(output_dir, "quast_results")
    busco_dir = os.path.join(output_dir, "busco_results")
    kraken_dir = os.path.join(output_dir, "kraken_results")
    prokka_dir = os.path.join(output_dir, "prokka_results")
    roary_dir = os.path.join(output_dir, "roary_results")
    mauve_dir = os.path.join(output_dir, "mauve_results")

    # --- 1. Parse Tool Outputs ---
    quast_data = pd.DataFrame()
    if os.path.exists(quast_dir) and os.listdir(quast_dir):
        quast_data = parse_quast_output(quast_dir)
    else:
        print(f"QUAST output directory not found or empty: {quast_dir}")
    
    busco_data = pd.DataFrame()
    if os.path.exists(busco_dir) and os.listdir(busco_dir):
        busco_data = parse_busco_output(busco_dir)
    else:
        print(f"BUSCO output directory not found or empty: {busco_dir}")

    kraken_data = {} # Dict of DataFrames
    if os.path.exists(kraken_dir) and os.listdir(kraken_dir):
        kraken_data = parse_kraken_output(kraken_dir)
    else:
        print(f"Kraken2 output directory not found or empty: {kraken_dir}")

    prokka_data = pd.DataFrame()
    if os.path.exists(prokka_dir) and os.listdir(prokka_dir):
        prokka_data = parse_prokka_output(prokka_dir)
    else:
        print(f"Prokka output directory not found or empty: {prokka_dir}")

    roary_data = pd.DataFrame()
    if os.path.exists(roary_dir) and os.listdir(roary_dir): # Check if Roary ran (dir exists and is not empty)
        roary_data = parse_roary_output(roary_dir)
    else:
        print(f"Roary output directory not found or empty: {roary_dir}. Skipping Roary parsing.")
        
    mauve_data = {} # Dict
    if os.path.exists(mauve_dir) and os.listdir(mauve_dir):
        mauve_data = parse_mauve_output(mauve_dir)
    else:
        print(f"Mauve output directory not found or empty: {mauve_dir}")


    # --- 2. Generate Plots ---
    quast_plot_html = create_quast_plots(quast_data)
    busco_plot_html = create_busco_plot(busco_data)
    kraken_plots_html = create_kraken_plot(kraken_data) # Returns a dict of html strings
    prokka_plot_html = create_prokka_plot(prokka_data)
    roary_plot_html = create_roary_plot(roary_data)
    # Mauve plots are typically interactive and complex; not generating a simple Plotly one here.

    # --- 3. Render HTML Report ---
    # Using an inline template string
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__) if os.path.dirname(__file__) else '.'), # For finding template if separate
                      autoescape=select_autoescape(['html', 'xml']))
    
    # If HTML_TEMPLATE is a string:
    from jinja2 import Template
    template = Template(HTML_TEMPLATE)


    report_vars = {
        "output_dir": output_dir,
        "quast_data": quast_data,
        "quast_plot": quast_plot_html,
        "busco_data": busco_data,
        "busco_plot": busco_plot_html,
        "kraken_data": kraken_data, # Pass the dict of DFs
        "kraken_plots": kraken_plots_html, # Pass the dict of plot HTMLs
        "prokka_data": prokka_data,
        "prokka_plot": prokka_plot_html,
        "roary_data": roary_data,
        "roary_plot": roary_plot_html,
        "mauve_data": mauve_data,
    }

    print("Rendering HTML report...")
    html_output = template.render(report_vars)

    try:
        with open(report_html_path, "w") as f:
            f.write(html_output)
        print(f"Report successfully generated: {report_html_path}")
    except IOError as e:
        print(f"Error writing HTML report to {report_html_path}: {e}")

# --- Command-line Argument Parsing ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an HTML report from DeepQC pipeline outputs.")
    parser.add_argument("output_dir", help="Directory containing all tool results from run_deepqc.sh.")
    parser.add_argument("report_html_path", help="Path to save the final HTML report.")
    
    args = parser.parse_args()
    
    main(args.output_dir, args.report_html_path)

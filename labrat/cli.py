# -*- coding: utf-8 -*-
"""Command-line interface for labrat."""
import json

import click
from pathlib import Path
from labrat.project import ProjectManager
from labrat.filemanager import Archiver, FileOrganizer


@click.group()
def main():
    """Labrat - A basic science lab framework for reproducibility and lab management."""
    pass


# =============================================================================
# Gene and Variant Lookup Commands
# =============================================================================


@main.group()
def gene():
    """Gene lookup and annotation commands."""
    pass


@gene.command("info")
@click.argument("gene_id")
@click.option(
    "--species", "-s", default=None, help="Species filter (e.g., human, mouse)"
)
@click.option(
    "--fields",
    "-f",
    default=None,
    help="Comma-separated list of fields to retrieve",
)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def gene_info(gene_id, species, fields, output_json):
    """Get information about a gene by ID or symbol.

    Examples:
        labrat gene info BRCA1
        labrat gene info BRCA1 --species human
        labrat gene info 672 --fields symbol,name,summary
    """
    try:
        from labrat.bioinformatics import get_gene_info

        field_list = fields.split(",") if fields else None
        result = get_gene_info(gene_id, fields=field_list, species=species)

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"\n{'='*60}")
            click.echo(f"Gene: {result.get('symbol', gene_id)}")
            click.echo(f"{'='*60}")
            if "name" in result:
                click.echo(f"Name: {result['name']}")
            if "entrezgene" in result:
                click.echo(f"Entrez ID: {result['entrezgene']}")
            if "ensembl" in result:
                ensembl = result["ensembl"]
                if isinstance(ensembl, dict):
                    click.echo(f"Ensembl ID: {ensembl.get('gene', 'N/A')}")
            if "type_of_gene" in result:
                click.echo(f"Type: {result['type_of_gene']}")
            if "summary" in result:
                click.echo(f"\nSummary:\n{result['summary'][:500]}...")
            click.echo()
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@gene.command("search")
@click.argument("query")
@click.option(
    "--species", "-s", default=None, help="Species filter (e.g., human, mouse)"
)
@click.option("--limit", "-n", default=10, help="Number of results to return")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def gene_search(query, species, limit, output_json):
    """Search for genes matching a query.

    Examples:
        labrat gene search BRCA
        labrat gene search "kinase" --species human --limit 5
    """
    try:
        from labrat.bioinformatics import query_genes

        results = query_genes(query, species=species, size=limit)

        if output_json:
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"\nFound {len(results)} results for '{query}':\n")
            for i, hit in enumerate(results, 1):
                symbol = hit.get("symbol", "N/A")
                name = hit.get("name", "N/A")
                entrez = hit.get("entrezgene", "N/A")
                click.echo(f"{i}. {symbol} (Entrez: {entrez})")
                click.echo(f"   {name[:60]}..." if len(str(name)) > 60 else f"   {name}")
            click.echo()
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@main.group()
def variant():
    """Variant lookup and annotation commands."""
    pass


@variant.command("info")
@click.argument("variant_id")
@click.option(
    "--assembly",
    "-a",
    default="hg38",
    help="Genome assembly (hg19 or hg38)",
)
@click.option(
    "--fields",
    "-f",
    default=None,
    help="Comma-separated list of fields to retrieve",
)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def variant_info(variant_id, assembly, fields, output_json):
    """Get information about a variant by HGVS notation or rsID.

    Examples:
        labrat variant info rs113488022
        labrat variant info "chr7:g.140453136A>T" --assembly hg38
    """
    try:
        from labrat.bioinformatics import get_variant_info

        field_list = fields.split(",") if fields else None
        result = get_variant_info(variant_id, fields=field_list, assembly=assembly)

        if output_json:
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"\n{'='*60}")
            click.echo(f"Variant: {result.get('_id', variant_id)}")
            click.echo(f"{'='*60}")
            if "dbsnp" in result:
                dbsnp = result["dbsnp"]
                if isinstance(dbsnp, dict):
                    click.echo(f"rsID: {dbsnp.get('rsid', 'N/A')}")
            if "clinvar" in result:
                clinvar = result["clinvar"]
                if isinstance(clinvar, dict):
                    rcv = clinvar.get("rcv", {})
                    if isinstance(rcv, list):
                        sig = rcv[0].get("clinical_significance", "N/A") if rcv else "N/A"
                    else:
                        sig = rcv.get("clinical_significance", "N/A")
                    click.echo(f"ClinVar Significance: {sig}")
            if "cadd" in result:
                cadd = result["cadd"]
                if isinstance(cadd, dict):
                    click.echo(f"CADD Score: {cadd.get('phred', 'N/A')}")
            click.echo()
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@variant.command("search")
@click.argument("query")
@click.option("--limit", "-n", default=10, help="Number of results to return")
@click.option(
    "--assembly",
    "-a",
    default="hg38",
    help="Genome assembly (hg19 or hg38)",
)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def variant_search(query, limit, assembly, output_json):
    """Search for variants matching a query.

    Examples:
        labrat variant search BRCA1
        labrat variant search "clinvar.gene.symbol:BRAF" --limit 5
    """
    try:
        from labrat.bioinformatics import query_variants

        results = query_variants(query, size=limit, assembly=assembly)

        if output_json:
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"\nFound {len(results)} results for '{query}':\n")
            for i, hit in enumerate(results, 1):
                var_id = hit.get("_id", "N/A")
                rsid = hit.get("dbsnp", {}).get("rsid", "") if isinstance(hit.get("dbsnp"), dict) else ""
                click.echo(f"{i}. {var_id}")
                if rsid:
                    click.echo(f"   rsID: {rsid}")
            click.echo()
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


# =============================================================================
# Enrichment Analysis Commands
# =============================================================================


@main.group()
def enrichment():
    """Gene set enrichment analysis commands."""
    pass


@enrichment.command("run")
@click.argument("genes", nargs=-1, required=True)
@click.option(
    "--type",
    "-t",
    "analysis_type",
    default="pathway",
    type=click.Choice(["pathway", "go", "disease", "tf", "all"]),
    help="Type of enrichment analysis",
)
@click.option("--organism", "-o", default="human", help="Organism for analysis")
@click.option("--cutoff", "-c", default=0.05, help="P-value cutoff")
@click.option("--output", "-O", type=click.Path(), help="Output file path (CSV)")
def enrichment_run(genes, analysis_type, organism, cutoff, output):
    """Run enrichment analysis on a list of genes.

    Examples:
        labrat enrichment run BRCA1 BRCA2 TP53 EGFR
        labrat enrichment run BRCA1 BRCA2 TP53 --type go --cutoff 0.01
        labrat enrichment run BRCA1 BRCA2 TP53 --output results.csv
    """
    try:
        from labrat.bioinformatics import run_enrichment

        gene_list = list(genes)
        click.echo(f"Running {analysis_type} enrichment for {len(gene_list)} genes...")

        results = run_enrichment(
            gene_list,
            analysis_type=analysis_type,
            organism=organism,
            cutoff=cutoff,
        )

        if output:
            results.to_csv(output, index=False)
            click.echo(f"✓ Results saved to {output}")
        else:
            # Display top results
            if len(results) == 0:
                click.echo("No significant enrichment found.")
            else:
                click.echo(f"\nTop {min(10, len(results))} enriched terms:\n")
                for _, row in results.head(10).iterrows():
                    term = row.get("Term", "N/A")
                    pval = row.get("Adjusted P-value", row.get("P-value", "N/A"))
                    click.echo(f"  • {term[:60]}...")
                    click.echo(f"    P-value: {pval:.2e}")
                click.echo()
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@enrichment.command("libraries")
@click.option("--organism", "-o", default="human", help="Organism to list libraries for")
def enrichment_libraries(organism):
    """List available gene set libraries.

    Examples:
        labrat enrichment libraries
        labrat enrichment libraries --organism mouse
    """
    try:
        from labrat.bioinformatics import EnrichmentClient

        libraries = EnrichmentClient.list_libraries(organism=organism)
        click.echo(f"\nAvailable libraries for {organism} ({len(libraries)} total):\n")
        for lib in sorted(libraries):
            click.echo(f"  • {lib}")
        click.echo()
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


# =============================================================================
# Wet Lab Utilities Commands
# =============================================================================


@main.group()
def wetlab():
    """Wet lab calculation utilities."""
    pass


@wetlab.command("mastermix")
@click.option("--reactions", "-n", required=True, type=int, help="Number of reactions")
@click.option("--volume", "-v", default=25.0, help="Volume per reaction (µL)")
@click.option("--extra", "-e", default=10.0, help="Extra percentage for pipetting error")
@click.option(
    "--polymerase",
    "-p",
    default="taq",
    type=click.Choice(["taq", "high_fidelity"]),
    help="Polymerase type",
)
@click.option("--save", "-s", is_flag=True, help="Save output to dated text file")
@click.option("--save-csv", is_flag=True, help="Save output to dated CSV file")
@click.option("--output", "-o", type=click.Path(), help="Custom output file path")
def mastermix(reactions, volume, extra, polymerase, save, save_csv, output):
    """Calculate PCR master mix volumes.

    Examples:
        labrat wetlab mastermix --reactions 10
        labrat wetlab mastermix --reactions 24 --volume 50 --polymerase high_fidelity
        labrat wetlab mastermix --reactions 10 --save
        labrat wetlab mastermix --reactions 10 --save-csv
        labrat wetlab mastermix --reactions 10 --output my_mastermix.csv
    """
    try:
        from labrat.wetlab import (
            calculate_mastermix,
            save_text_output,
            save_csv_output,
            format_mastermix_for_csv,
        )

        mm = calculate_mastermix(
            reactions=reactions,
            volume=volume,
            extra_percent=extra,
            polymerase_type=polymerase,
        )

        # Always display to terminal
        click.echo(f"\n{mm}\n")

        # Save if requested
        if save or save_csv or output:
            if output and output.endswith((".csv", ".tsv")):
                save_csv = True

            if save_csv or (output and output.endswith((".csv", ".tsv"))):
                data = format_mastermix_for_csv(mm)
                delimiter = "\t" if output and output.endswith(".tsv") else ","
                path = save_csv_output(data, output_path=output, base_name="mastermix", delimiter=delimiter)
                click.echo(f"✓ CSV saved to: {path}")
            else:
                path = save_text_output(str(mm), output_path=output, base_name="mastermix")
                click.echo(f"✓ Output saved to: {path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@wetlab.command("tm")
@click.argument("sequence")
@click.option(
    "--method",
    "-m",
    default="wallace",
    type=click.Choice(["wallace", "gc_content", "nearest_neighbor"]),
    help="Calculation method",
)
def primer_tm(sequence, method):
    """Calculate primer melting temperature.

    Examples:
        labrat wetlab tm ATGCGATCGATCGATCG
        labrat wetlab tm ATGCGATCGATCGATCG --method nearest_neighbor
    """
    try:
        from labrat.wetlab import calculate_tm

        tm = calculate_tm(sequence, method=method)
        click.echo(f"\nSequence: {sequence}")
        click.echo(f"Length: {len(sequence)} bp")
        click.echo(f"Method: {method}")
        click.echo(f"Tm: {tm}°C\n")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@wetlab.command("dilution")
@click.option("--initial", "-i", required=True, type=float, help="Initial concentration")
@click.option("--final", "-f", required=True, type=float, help="Final concentration")
@click.option("--volume", "-v", required=True, type=float, help="Final volume")
@click.option("--unit", "-u", default="", help="Concentration unit (e.g., µM, ng/µL)")
@click.option("--save", "-s", is_flag=True, help="Save output to dated text file")
@click.option("--save-csv", is_flag=True, help="Save output to dated CSV file")
@click.option("--output", "-o", type=click.Path(), help="Custom output file path")
def dilution(initial, final, volume, unit, save, save_csv, output):
    """Calculate dilution volumes (C1V1 = C2V2).

    Examples:
        labrat wetlab dilution --initial 100 --final 10 --volume 1000
        labrat wetlab dilution --initial 100 --final 10 --volume 1000 --unit µM
        labrat wetlab dilution --initial 100 --final 10 --volume 1000 --save
        labrat wetlab dilution --initial 100 --final 10 --volume 1000 --save-csv
    """
    try:
        from labrat.wetlab import (
            calculate_dilution,
            save_text_output,
            save_csv_output,
            format_dilution_for_csv,
        )

        result = calculate_dilution(initial, final, volume)

        # Format output text
        output_text = f"""Dilution Calculation
{'='*50}
Initial concentration: {initial} {unit}
Final concentration: {final} {unit}
Final volume: {volume}

Result:
Stock volume: {result['stock_volume']}
Diluent volume: {result['diluent_volume']}
Dilution factor: {result['dilution_factor']:.1f}x
"""

        # Display to terminal
        click.echo(f"\n{output_text}")

        # Save if requested
        if save or save_csv or output:
            if output and output.endswith((".csv", ".tsv")):
                save_csv = True

            if save_csv or (output and output.endswith((".csv", ".tsv"))):
                data = format_dilution_for_csv(result, initial, final, volume, unit)
                delimiter = "\t" if output and output.endswith(".tsv") else ","
                path = save_csv_output(data, output_path=output, base_name="dilution", delimiter=delimiter)
                click.echo(f"✓ CSV saved to: {path}")
            else:
                path = save_text_output(output_text, output_path=output, base_name="dilution")
                click.echo(f"✓ Output saved to: {path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@wetlab.command("serial")
@click.option("--initial", "-i", required=True, type=float, help="Initial concentration")
@click.option("--factor", "-f", default=10.0, help="Dilution factor")
@click.option("--dilutions", "-n", default=6, help="Number of dilutions")
@click.option("--transfer", "-t", default=100.0, help="Transfer volume (µL)")
@click.option("--final-volume", "-v", default=1000.0, help="Final volume per tube (µL)")
@click.option("--unit", "-u", default="µM", help="Concentration unit")
@click.option("--save", "-s", is_flag=True, help="Save output to dated text file")
@click.option("--save-csv", is_flag=True, help="Save output to dated CSV file")
@click.option("--output", "-o", type=click.Path(), help="Custom output file path")
def serial(initial, factor, dilutions, transfer, final_volume, unit, save, save_csv, output):
    """Calculate serial dilution series.

    Examples:
        labrat wetlab serial --initial 100 --factor 10 --dilutions 5
        labrat wetlab serial --initial 1000 --factor 2 --dilutions 12 --transfer 500
        labrat wetlab serial --initial 100 --factor 10 --dilutions 5 --save
        labrat wetlab serial --initial 100 --factor 10 --dilutions 5 --save-csv
        labrat wetlab serial --initial 100 --dilutions 5 --output dilutions.csv
    """
    try:
        from labrat.wetlab import (
            serial_dilution,
            save_text_output,
            save_csv_output,
            format_serial_dilution_for_csv,
        )

        series = serial_dilution(
            initial_concentration=initial,
            factor=factor,
            dilutions=dilutions,
            transfer_volume=transfer,
            final_volume=final_volume,
            concentration_unit=unit,
        )

        # Always display to terminal
        click.echo(f"\n{series}\n")

        # Save if requested
        if save or save_csv or output:
            if output and output.endswith((".csv", ".tsv")):
                save_csv = True

            if save_csv or (output and output.endswith((".csv", ".tsv"))):
                data = format_serial_dilution_for_csv(series)
                delimiter = "\t" if output and output.endswith(".tsv") else ","
                path = save_csv_output(data, output_path=output, base_name="serial_dilution", delimiter=delimiter)
                click.echo(f"✓ CSV saved to: {path}")
            else:
                path = save_text_output(str(series), output_path=output, base_name="serial_dilution")
                click.echo(f"✓ Output saved to: {path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@wetlab.command("buffer")
@click.argument("buffer_name")
@click.option("--volume", "-v", default=1000.0, help="Volume to prepare (mL)")
@click.option("--save", "-s", is_flag=True, help="Save output to dated text file")
@click.option("--save-csv", is_flag=True, help="Save output to dated CSV file")
@click.option("--output", "-o", type=click.Path(), help="Custom output file path")
def buffer(buffer_name, volume, save, save_csv, output):
    """Get buffer recipe and calculate volumes.

    Available buffers: PBS, PBS_10X, TBS, TBS_10X, TBST, TE, TAE_50X, TBE_10X, RIPA, LOADING_6X

    Examples:
        labrat wetlab buffer PBS
        labrat wetlab buffer PBS --volume 500
        labrat wetlab buffer PBS --save
        labrat wetlab buffer PBS --save-csv
        labrat wetlab buffer PBS --output pbs_recipe.csv
    """
    try:
        from labrat.wetlab import (
            get_buffer_recipe,
            calculate_buffer_volume,
            save_text_output,
            save_csv_output,
            format_buffer_for_csv,
        )

        recipe = get_buffer_recipe(buffer_name)

        # Build output text
        output_text = str(recipe)
        if volume != 1000.0:
            output_text += f"\n\n{'='*50}\n"
            output_text += f"Scaled amounts for {volume} mL:\n"
            output_text += f"{'='*50}\n"
            scaled = calculate_buffer_volume(buffer_name, volume)
            for component, data in scaled.items():
                output_text += f"  {component}: {data['amount']:.3f} {data['unit']}\n"

        # Display to terminal
        click.echo(f"\n{output_text}\n")

        # Save if requested
        if save or save_csv or output:
            if output and output.endswith((".csv", ".tsv")):
                save_csv = True

            if save_csv or (output and output.endswith((".csv", ".tsv"))):
                data = format_buffer_for_csv(recipe, volume)
                delimiter = "\t" if output and output.endswith(".tsv") else ","
                path = save_csv_output(data, output_path=output, base_name=f"buffer_{buffer_name.lower()}", delimiter=delimiter)
                click.echo(f"✓ CSV saved to: {path}")
            else:
                path = save_text_output(output_text, output_path=output, base_name=f"buffer_{buffer_name.lower()}")
                click.echo(f"✓ Output saved to: {path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@wetlab.command("buffers")
def list_buffers():
    """List all available buffer recipes.

    Examples:
        labrat wetlab buffers
    """
    try:
        from labrat.wetlab.buffers import list_buffers as get_buffer_list

        buffers = get_buffer_list()
        click.echo("\nAvailable buffer recipes:\n")
        for buf in buffers:
            click.echo(f"  • {buf}")
        click.echo("\nUse 'labrat wetlab buffer <name>' to see the recipe.\n")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@wetlab.command("qpcr-layout")
@click.option("--samples", "-s", required=True, help="Comma-separated list of sample names")
@click.option("--genes", "-g", required=True, help="Comma-separated list of gene names")
@click.option("--replicates", "-r", default=3, help="Number of technical replicates")
@click.option("--plate", "-p", default="96", type=click.Choice(["96", "384"]), help="Plate size")
@click.option("--no-ntc", is_flag=True, help="Exclude no-template controls")
@click.option("--save", is_flag=True, help="Save output to dated text file")
@click.option("--save-csv", is_flag=True, help="Save output to dated CSV file")
@click.option("--output", "-o", type=click.Path(), help="Custom output file path")
def qpcr_layout(samples, genes, replicates, plate, no_ntc, save, save_csv, output):
    """Generate a qPCR plate layout.

    Examples:
        labrat wetlab qpcr-layout --samples "S1,S2,S3" --genes "GAPDH,ACTB,Target1"
        labrat wetlab qpcr-layout --samples "S1,S2" --genes "G1,G2" --replicates 2
        labrat wetlab qpcr-layout --samples "S1,S2" --genes "G1,G2" --save-csv
    """
    try:
        from labrat.wetlab import (
            generate_qpcr_plate_layout,
            save_text_output,
            save_csv_output,
            format_qpcr_layout_for_csv,
        )

        sample_list = [s.strip() for s in samples.split(",")]
        gene_list = [g.strip() for g in genes.split(",")]

        layout = generate_qpcr_plate_layout(
            samples=sample_list,
            genes=gene_list,
            replicates=replicates,
            include_ntc=not no_ntc,
            plate_size=int(plate),
        )

        # Build output text
        summary = layout["summary"]
        output_text = f"""qPCR Plate Layout
{'='*50}
Samples: {', '.join(sample_list)}
Genes: {', '.join(gene_list)}
Replicates: {replicates}
Include NTC: {not no_ntc}
Plate size: {plate}-well
{'='*50}
Wells used: {summary['wells_used']} / {summary['wells_available']} ({summary['utilization']})
{'='*50}
Well Assignments:
"""
        for well_id, assignment in sorted(layout["well_assignments"].items()):
            output_text += f"  {well_id}: {assignment['sample']} - {assignment['gene']} (Rep {assignment['replicate']})\n"

        # Display to terminal
        click.echo(f"\n{output_text}")

        # Save if requested
        if save or save_csv or output:
            if output and output.endswith((".csv", ".tsv")):
                save_csv = True

            if save_csv or (output and output.endswith((".csv", ".tsv"))):
                data = format_qpcr_layout_for_csv(layout)
                delimiter = "\t" if output and output.endswith(".tsv") else ","
                path = save_csv_output(data, output_path=output, base_name="qpcr_layout", delimiter=delimiter)
                click.echo(f"✓ CSV saved to: {path}")
            else:
                path = save_text_output(output_text, output_path=output, base_name="qpcr_layout")
                click.echo(f"✓ Output saved to: {path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@main.group()
def project():
    """Manage projects."""
    pass


@project.command('new')
@click.option('--type', 'project_type', required=True,
              help='Type of project (e.g., computational-biology, data-science)')
@click.option('--name', 'project_name', required=True,
              help='Name of the project')
@click.option('--path', 'project_path', required=True, type=click.Path(),
              help='Path where the project will be created')
@click.option('--description', required=True,
              help='Description of the project')
@click.option('--username', default=None,
              help='Username for project manager (defaults to system default)')
def new_project(project_type, project_name, project_path, description, username):
    """Create a new project."""
    try:
        manager = ProjectManager(username=username)
        manager.new_project(
            project_type=project_type,
            project_name=project_name,
            project_path=project_path,
            description=description
        )
        click.echo(f"✓ Project '{project_name}' created successfully at {project_path}")
    except Exception as e:
        click.echo(f"✗ Error creating project: {e}", err=True)
        raise click.Abort()


@project.command('list')
@click.option('--username', default=None,
              help='Username for project manager (defaults to system default)')
def list_projects(username):
    """List all projects."""
    try:
        manager = ProjectManager(username=username)
        projects = manager.list_projects()
        
        if not projects:
            click.echo("No projects found.")
            return
        
        click.echo(f"\nFound {len(projects)} project(s):\n")
        for idx, proj in enumerate(projects, 1):
            click.echo(f"{idx}. {proj.get('name', 'Unknown')}")
            click.echo(f"   Path: {proj.get('path', 'Unknown')}")
            click.echo(f"   Type: {proj.get('project_type', 'Unknown')}")
            click.echo(f"   Created: {proj.get('created_at', 'Unknown')}")
            click.echo()
    except Exception as e:
        click.echo(f"✗ Error listing projects: {e}", err=True)
        raise click.Abort()


@project.command('delete')
@click.option('--path', 'project_path', required=True, type=click.Path(exists=True),
              help='Path to the project to delete')
@click.option('--archive-dir', required=True, type=click.Path(),
              help='Directory where the archived project will be stored')
@click.option('--username', default=None,
              help='Username for project manager (defaults to system default)')
@click.confirmation_option(prompt='Are you sure you want to delete this project?')
def delete_project(project_path, archive_dir, username):
    """Delete a project (archives it first)."""
    try:
        manager = ProjectManager(username=username)
        archive_path = manager.delete_project(project_path, archive_dir)
        click.echo(f"✓ Project deleted and archived to: {archive_path}")
    except Exception as e:
        click.echo(f"✗ Error deleting project: {e}", err=True)
        raise click.Abort()


@main.command('archive')
@click.option('--source', required=True, type=click.Path(exists=True, dir_okay=True),
              help='Source directory to archive')
@click.option('--destination', required=True, type=click.Path(),
              help='Base directory for storing archives')
@click.option('--name', 'project_name', required=True,
              help='Name for the archive')
def archive(source, destination, project_name):
    """Archive a directory."""
    try:
        archive_dir = Archiver.get_archive_dir(destination, project_name)
        archiver = Archiver(source_dir=source, archive_dir=archive_dir)
        zip_path = archiver.archive()
        click.echo(f"✓ Archive created successfully: {zip_path}")
    except Exception as e:
        click.echo(f"✗ Error creating archive: {e}", err=True)
        raise click.Abort()


@main.command('organize')
@click.option('--science', 'organize_science', is_flag=True,
              help='Organize scientific data files (fastq, fasta, sam, bam, vcf, fits, hdf5, etc.) to Documents/Research_Data')
@click.option('--science-dir', type=click.Path(),
              help='Custom directory for scientific data files (default: Documents/Research_Data)')
@click.option('--keyword', default=None,
              help='Move files containing this keyword to a specific folder')
@click.option('--pictures', 'organize_pictures', is_flag=True,
              help='Organize picture files to Pictures folder')
@click.option('--videos', 'organize_videos', is_flag=True,
              help='Organize video files to Videos folder')
@click.option('--archives', 'organize_archives', is_flag=True,
              help='Organize archive files by compression type')
@click.option('--all', 'organize_all', is_flag=True,
              help='Organize all file types')
def organize(organize_science, science_dir, keyword, organize_pictures,
             organize_videos, organize_archives, organize_all):
    """
    Organize files in Downloads and Documents directories.
    
    By default, scientific data files (fastq, fasta, sam, bam, vcf, fits, hdf5, nc, etc.)
    are moved to Documents/Research_Data. Use --science-dir to specify a custom location.
    
    Examples:
        labrat organize --science
        labrat organize --science --science-dir ~/Research
        labrat organize --keyword "project_alpha"
        labrat organize --all
    """
    if not any([organize_science, keyword, organize_pictures, organize_videos,
                organize_archives, organize_all]):
        click.echo("Error: Specify at least one organization option", err=True)
        click.echo("Use --science to organize science files, or --all for everything", err=True)
        raise click.Abort()
    
    try:
        organizer = FileOrganizer()
        actions_taken = []
        
        if organize_all:
            organizer.organize_all()
            actions_taken.append("all files")
        else:
            # Organize science files (default behavior for scientists)
            if organize_science:
                organizer.organize_science_files(science_dir=science_dir)
                location = science_dir if science_dir else "Documents/Research_Data"
                actions_taken.append(f"science files to {location}")
            
            # Organize media files
            if organize_pictures or organize_videos:
                organizer.organize_files()
                media = []
                if organize_pictures:
                    media.append("pictures")
                if organize_videos:
                    media.append("videos")
                actions_taken.append(f"{' and '.join(media)}")
            
            # Organize archives
            if organize_archives:
                organizer.organize_archives()
                actions_taken.append("archives")
            
            # Handle keyword-based organization
            if keyword:
                organizer.move_specific_files(keyword=keyword)
                actions_taken.append(f"files with keyword '{keyword}'")
        
        click.echo(f"✓ Organized {', '.join(actions_taken)} successfully")
    except Exception as e:
        click.echo(f"✗ Error organizing files: {e}", err=True)
        raise click.Abort()


# =============================================================================
# Report Generation Commands
# =============================================================================


@main.group()
def report():
    """Generate laboratory reports."""
    pass


@report.command("qc")
@click.option("--project", "-p", required=True, help="Project name")
@click.option("--analyst", "-a", required=True, help="Analyst name")
@click.option("--metric", "-m", multiple=True, help="Metric in format 'name:value[:status]'")
@click.option("--sample-count", "-n", type=int, help="Number of samples")
@click.option("--summary", "-s", help="Summary text")
@click.option("--warning", "-w", multiple=True, help="Warning message")
@click.option("--notes", help="Additional notes")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def qc_report(project, analyst, metric, sample_count, summary, warning, notes, output):
    """Generate a QC (Quality Control) report.

    Examples:
        labrat report qc --project "NGS Run 001" --analyst "Dr. Smith" \\
            --metric "Total Reads:50M:PASS" --metric "Q30:92%:PASS"
        labrat report qc --project "Run001" --analyst "Jane" --metric "Yield:100ng" --output qc_report.txt
    """
    try:
        from labrat.reports import ReportGenerator

        # Parse metrics
        metrics = []
        for m in metric:
            parts = m.split(":")
            metric_dict = {"name": parts[0], "value": parts[1] if len(parts) > 1 else "N/A"}
            if len(parts) > 2:
                metric_dict["status"] = parts[2]
            metrics.append(metric_dict)

        generator = ReportGenerator()
        report_text = generator.generate_qc_report(
            project_name=project,
            analyst=analyst,
            metrics=metrics,
            sample_count=sample_count,
            summary=summary,
            warnings=list(warning) if warning else None,
            notes=notes,
        )

        click.echo(report_text)

        if output:
            path = generator.save_report(report_text, output_path=output, base_name="qc_report")
            click.echo(f"\n✓ Report saved to: {path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@report.command("variant")
@click.option("--project", "-p", required=True, help="Project name")
@click.option("--analyst", "-a", required=True, help="Analyst name")
@click.option("--total", "-t", required=True, type=int, help="Total number of variants")
@click.option("--reference", "-r", help="Reference genome (e.g., GRCh38)")
@click.option("--count", "-c", multiple=True, help="Variant count in format 'type:count' (e.g., SNV:12000)")
@click.option("--notes", help="Additional notes")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def variant_report(project, analyst, total, reference, count, notes, output):
    """Generate a variant summary report.

    Examples:
        labrat report variant --project "Exome Analysis" --analyst "Dr. Jones" \\
            --total 15000 --count "SNV:12000" --count "INDEL:3000" --reference GRCh38
    """
    try:
        from labrat.reports import ReportGenerator

        # Parse variant counts
        variant_counts = {}
        for c in count:
            parts = c.split(":")
            if len(parts) == 2:
                variant_counts[parts[0]] = int(parts[1])

        generator = ReportGenerator()
        report_text = generator.generate_variant_summary(
            project_name=project,
            analyst=analyst,
            total_variants=total,
            reference_genome=reference,
            variant_counts=variant_counts if variant_counts else None,
            notes=notes,
        )

        click.echo(report_text)

        if output:
            path = generator.save_report(report_text, output_path=output, base_name="variant_summary")
            click.echo(f"\n✓ Report saved to: {path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@report.command("wetlab")
@click.option("--experiment", "-e", required=True, help="Experiment name")
@click.option("--researcher", "-r", required=True, help="Researcher name")
@click.option("--objective", "-obj", required=True, help="Experiment objective")
@click.option("--material", "-m", multiple=True, help="Material in format 'name[:concentration][:vendor]'")
@click.option("--method", "-M", multiple=True, help="Method step")
@click.option("--lab", "-l", help="Lab name/location")
@click.option("--results", help="Results text")
@click.option("--observation", "-O", multiple=True, help="Observation")
@click.option("--conclusion", "-c", help="Conclusions")
@click.option("--next-step", "-n", multiple=True, help="Next step")
@click.option("--notes", help="Additional notes")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def wetlab_report(experiment, researcher, objective, material, method, lab,
                  results, observation, conclusion, next_step, notes, output):
    """Generate a wet lab experiment report.

    Examples:
        labrat report wetlab --experiment "PCR Optimization" --researcher "Dr. Smith" \\
            --objective "Optimize PCR conditions" --material "Taq Polymerase::NEB" \\
            --method "Mix reagents" --method "Run PCR"
    """
    try:
        from labrat.reports import ReportGenerator

        # Parse materials
        materials = []
        for m in material:
            parts = m.split(":")
            mat_dict = {"name": parts[0]}
            if len(parts) > 1 and parts[1]:
                mat_dict["concentration"] = parts[1]
            if len(parts) > 2 and parts[2]:
                mat_dict["vendor"] = parts[2]
            materials.append(mat_dict)

        generator = ReportGenerator()
        report_text = generator.generate_wetlab_report(
            experiment_name=experiment,
            researcher=researcher,
            objective=objective,
            materials=materials,
            methods=list(method),
            lab=lab,
            results=results,
            observations=list(observation) if observation else None,
            conclusions=conclusion,
            next_steps=list(next_step) if next_step else None,
            notes=notes,
        )

        click.echo(report_text)

        if output:
            path = generator.save_report(report_text, output_path=output, base_name="wetlab_report")
            click.echo(f"\n✓ Report saved to: {path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


# =============================================================================
# Glossary Commands
# =============================================================================


@main.group()
def glossary():
    """Science and lab glossary commands."""
    pass


@glossary.command("lookup")
@click.argument("term")
def glossary_lookup(term):
    """Look up a term in the science glossary.

    Examples:
        labrat glossary lookup PCR
        labrat glossary lookup "melting temperature"
    """
    try:
        from labrat.glossary import lookup_term

        result = lookup_term(term)
        if result:
            click.echo(f"\n{result['term']}")
            click.echo("=" * len(result['term']))
            click.echo(f"\nDefinition: {result['definition']}")
            if result.get('abbreviation'):
                click.echo(f"Abbreviation: {result['abbreviation']}")
            if result.get('category'):
                click.echo(f"Category: {result['category']}")
            if result.get('related'):
                click.echo(f"Related terms: {', '.join(result['related'])}")
            click.echo()
        else:
            click.echo(f"Term '{term}' not found in glossary.")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@glossary.command("search")
@click.argument("query")
@click.option("--category", "-c", help="Filter by category")
def glossary_search(query, category):
    """Search the glossary for matching terms.

    Examples:
        labrat glossary search DNA
        labrat glossary search polymer --category chemistry
    """
    try:
        from labrat.glossary import search_glossary

        results = search_glossary(query, category=category)
        if results:
            click.echo(f"\nFound {len(results)} matching terms:\n")
            for r in results:
                click.echo(f"  • {r['term']}")
                click.echo(f"    {r['definition'][:80]}...")
            click.echo()
        else:
            click.echo(f"No terms matching '{query}' found.")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@glossary.command("categories")
def glossary_categories():
    """List all glossary categories.

    Examples:
        labrat glossary categories
    """
    try:
        from labrat.glossary import list_categories

        categories = list_categories()
        click.echo("\nGlossary Categories:\n")
        for cat in sorted(categories):
            click.echo(f"  • {cat}")
        click.echo()
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Command-line interface for labrat."""

import json
from pathlib import Path

import click

from labrat.filemanager import Archiver, FileOrganizer
from labrat.project import ProjectManager
from labrat.query import QueryError, QueryResult
from labrat.query import query_gene as run_gene_query
from labrat.query import query_literature as run_literature_query
from labrat.query import query_variant as run_variant_query
from labrat.query.render import render_query_result

OUTPUT_FORMAT = click.Choice(["table", "json"], case_sensitive=False)
RELATION_TYPE = click.Choice(
    [
        "ANY",
        "associate",
        "cause",
        "compare",
        "convert",
        "cotreat",
        "drug_interact",
        "inhibit",
        "interact",
        "negative_correlate",
        "positive_correlate",
        "prevent",
        "stimulate",
        "treat",
    ],
    case_sensitive=False,
)


@click.group()
def main():
    """Labrat - A basic science lab framework for reproducibility and lab management."""
    pass


def _echo_query_result(
    result: QueryResult,
    output_format: str,
    show_all_gene_matches: bool = False,
) -> None:
    """Dispatch either stable JSON or a query-specific terminal summary."""
    if output_format.lower() == "json":
        # Bypass Rich so redirected JSON remains valid for downstream parsers.
        click.echo(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        return

    render_query_result(result, show_all_gene_matches=show_all_gene_matches)


@main.group("query")
def query_group() -> None:
    """Query public gene, variant, and biomedical literature resources."""


@query_group.command("gene")
@click.argument("gene")
@click.option("--species", default="human", show_default=True)
@click.option("--limit", default=5, show_default=True, type=click.IntRange(1, 100))
@click.option("--all-matches", is_flag=True, help="Display lower-ranked matches.")
@click.option("--format", "output_format", default="table", type=OUTPUT_FORMAT)
def query_gene_command(
    gene: str,
    species: str,
    limit: int,
    all_matches: bool,
    output_format: str,
) -> None:
    """Find gene annotations through MyGene."""
    try:
        result = run_gene_query(gene, species=species, limit=limit)
    except QueryError as error:
        raise click.ClickException(str(error)) from error
    _echo_query_result(
        result,
        output_format,
        show_all_gene_matches=all_matches,
    )


@query_group.command("variant")
@click.argument("variant")
@click.option("--limit", default=5, show_default=True, type=click.IntRange(1, 100))
@click.option("--format", "output_format", default="table", type=OUTPUT_FORMAT)
def query_variant_command(
    variant: str,
    limit: int,
    output_format: str,
) -> None:
    """Find an rsID or hg19 genomic HGVS identifier through MyVariant."""
    try:
        result = run_variant_query(variant, limit=limit)
    except QueryError as error:
        raise click.ClickException(str(error)) from error
    _echo_query_result(result, output_format)


@query_group.command("literature")
@click.argument("search_text", required=False)
@click.option("--gene", help="Resolve and search for a gene concept.")
@click.option("--disease", help="Resolve and search for a disease concept.")
@click.option("--variant", help="Resolve and search for a variant concept.")
@click.option("--chemical", help="Resolve and search for a chemical concept.")
@click.option("--relation", type=RELATION_TYPE, help="Require an extracted relation.")
@click.option("--page", default=1, show_default=True, type=click.IntRange(min=1))
@click.option("--limit", default=10, show_default=True, type=click.IntRange(1, 100))
@click.option("--format", "output_format", default="table", type=OUTPUT_FORMAT)
def query_literature_command(
    search_text: str | None,
    gene: str | None,
    disease: str | None,
    variant: str | None,
    chemical: str | None,
    relation: str | None,
    page: int,
    limit: int,
    output_format: str,
) -> None:
    """Find biomedical publications through PubTator 3."""
    # Fixed entity-type order keeps generated PubTator queries deterministic.
    entities = {
        entity_type: value
        for entity_type, value in {
            "gene": gene,
            "disease": disease,
            "variant": variant,
            "chemical": chemical,
        }.items()
        if value is not None
    }
    try:
        result = run_literature_query(
            search_text=search_text,
            entities=entities,
            relation=relation,
            page=page,
            limit=limit,
        )
    except QueryError as error:
        raise click.ClickException(str(error)) from error
    _echo_query_result(result, output_format)


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


if __name__ == "__main__":
    main()

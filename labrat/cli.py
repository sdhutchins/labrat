# -*- coding: utf-8 -*-
"""Command-line interface for labrat."""
import click
from pathlib import Path
from labrat.project import ProjectManager
from labrat.filemanager import Archiver, FileOrganizer


@click.group()
def main():
    """Labrat - A basic science lab framework for reproducibility and lab management."""
    pass


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

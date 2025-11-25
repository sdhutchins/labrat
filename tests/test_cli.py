import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from labrat.cli import main


@pytest.fixture
def runner():
    """CLI runner fixture."""
    return CliRunner()

def test_main_help(runner):
    """Test that the main command shows help."""
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "Labrat" in result.output
    assert "project" in result.output
    assert "archive" in result.output
    assert "organize" in result.output

def test_project_group_help(runner):
    """Test that the project group shows help."""
    result = runner.invoke(main, ['project', '--help'])
    assert result.exit_code == 0
    assert "Manage projects" in result.output
    assert "new" in result.output
    assert "list" in result.output
    assert "delete" in result.output

@patch('labrat.cli.ProjectManager')
def test_project_new_success(mock_project_manager_class, runner):
    """Test creating a new project via CLI."""
    mock_manager = MagicMock()
    mock_project_manager_class.return_value = mock_manager

    result = runner.invoke(main, [
        'project', 'new',
        '--type', 'computational-biology',
        '--name', 'Test Project',
        '--path', '/tmp/test_project',
        '--description', 'A test project'
    ])

    assert result.exit_code == 0
    assert "✓ Project 'Test Project' created successfully" in result.output
    mock_manager.new_project.assert_called_once_with(
        project_type='computational-biology',
        project_name='Test Project',
        project_path='/tmp/test_project',
        description='A test project'
    )

def test_project_new_missing_options(runner):
    """Test that missing required options show an error."""
    result = runner.invoke(main, [
        'project', 'new',
        '--name', 'Test Project'
    ])

    assert result.exit_code != 0
    assert "Error" in result.output

@patch('labrat.cli.ProjectManager')
def test_project_new_error_handling(mock_project_manager_class, runner):
    """Test error handling when project creation fails."""
    mock_manager = MagicMock()
    mock_manager.new_project.side_effect = ValueError("Invalid project type")
    mock_project_manager_class.return_value = mock_manager

    result = runner.invoke(main, [
        'project', 'new',
        '--type', 'invalid-type',
        '--name', 'Test Project',
        '--path', '/tmp/test_project',
        '--description', 'A test project'
    ])

    assert result.exit_code != 0
    assert "✗ Error creating project" in result.output

@patch('labrat.cli.ProjectManager')
def test_project_list_empty(mock_project_manager_class, runner):
    """Test listing projects when none exist."""
    mock_manager = MagicMock()
    mock_manager.list_projects.return_value = []
    mock_project_manager_class.return_value = mock_manager

    result = runner.invoke(main, ['project', 'list'])

    assert result.exit_code == 0
    assert "No projects found" in result.output

@patch('labrat.cli.ProjectManager')
def test_project_list_with_projects(mock_project_manager_class, runner):
    """Test listing projects when projects exist."""
    mock_manager = MagicMock()
    mock_manager.list_projects.return_value = [
        {
            'name': 'project1',
            'path': '/path/to/project1',
            'project_type': 'computational-biology',
            'created_at': '2024-01-01T00:00:00'
        },
        {
            'name': 'project2',
            'path': '/path/to/project2',
            'project_type': 'data-science',
            'created_at': '2024-01-02T00:00:00'
        }
    ]
    mock_project_manager_class.return_value = mock_manager

    result = runner.invoke(main, ['project', 'list'])

    assert result.exit_code == 0
    assert "Found 2 project(s)" in result.output
    assert "project1" in result.output
    assert "project2" in result.output

@patch('labrat.cli.ProjectManager')
def test_project_delete_with_confirmation(mock_project_manager_class, runner, tmp_path):
    """Test deleting a project with confirmation."""
    test_project_dir = tmp_path / "test_project"
    test_archive_dir = tmp_path / "archive"
    test_project_dir.mkdir()
    test_archive_dir.mkdir()

    mock_manager = MagicMock()
    mock_manager.delete_project.return_value = str(test_archive_dir)
    mock_project_manager_class.return_value = mock_manager

    result = runner.invoke(main, [
        'project', 'delete',
        '--path', str(test_project_dir),
        '--archive-dir', str(test_archive_dir)
    ], input='y\n')

    assert result.exit_code == 0
    assert "✓ Project deleted and archived" in result.output
    mock_manager.delete_project.assert_called_once_with(
        str(test_project_dir),
        str(test_archive_dir)
    )

@patch('labrat.cli.ProjectManager')
def test_project_delete_without_confirmation(mock_project_manager_class, runner, tmp_path):
    """Test that deleting a project without confirmation is aborted."""
    test_project_dir = tmp_path / "test_project"
    test_archive_dir = tmp_path / "archive"
    test_project_dir.mkdir()
    test_archive_dir.mkdir()

    mock_manager = MagicMock()
    mock_project_manager_class.return_value = mock_manager

    result = runner.invoke(main, [
        'project', 'delete',
        '--path', str(test_project_dir),
        '--archive-dir', str(test_archive_dir)
    ], input='n\n')

    assert result.exit_code != 0
    mock_manager.delete_project.assert_not_called()

@patch('labrat.cli.Archiver')
def test_archive_success(mock_archiver_class, runner, tmp_path):
    """Test archiving a directory via CLI."""
    test_source_dir = tmp_path / "source"
    test_destination_dir = tmp_path / "archive"
    test_source_dir.mkdir()
    test_destination_dir.mkdir()

    mock_archive_dir = tmp_path / "test_archive_20240101_120000"
    # Mock the static method
    mock_archiver_class.get_archive_dir.return_value = mock_archive_dir
    
    # Mock the instance and its archive method
    mock_archiver_instance = MagicMock()
    mock_archiver_instance.archive.return_value = str(mock_archive_dir) + '.zip'
    # When Archiver() is called, return our mock instance
    mock_archiver_class.return_value = mock_archiver_instance

    result = runner.invoke(main, [
        'archive',
        '--source', str(test_source_dir),
        '--destination', str(test_destination_dir),
        '--name', 'test_archive'
    ])

    assert result.exit_code == 0, f"Error: {result.output}"
    assert "✓ Archive created successfully" in result.output
    # Verify get_archive_dir was called correctly
    mock_archiver_class.get_archive_dir.assert_called_once()
    # Verify Archiver was instantiated
    assert mock_archiver_class.called
    # Verify archive method was called
    mock_archiver_instance.archive.assert_called_once()

@patch('labrat.cli.FileOrganizer')
def test_organize_science_files(mock_organizer_class, runner):
    """Test organizing science files."""
    mock_organizer = MagicMock()
    mock_organizer_class.return_value = mock_organizer

    result = runner.invoke(main, ['organize', '--science'])

    assert result.exit_code == 0
    assert "✓ Organized" in result.output
    assert "science files" in result.output
    mock_organizer.organize_science_files.assert_called_once_with(science_dir=None)

@patch('labrat.cli.FileOrganizer')
def test_organize_science_files_custom_dir(mock_organizer_class, runner):
    """Test organizing science files to a custom directory."""
    mock_organizer = MagicMock()
    mock_organizer_class.return_value = mock_organizer

    result = runner.invoke(main, [
        'organize', '--science', '--science-dir', '/custom/path'
    ])

    assert result.exit_code == 0
    assert "✓ Organized" in result.output
    mock_organizer.organize_science_files.assert_called_once_with(science_dir='/custom/path')

@patch('labrat.cli.FileOrganizer')
def test_organize_keyword(mock_organizer_class, runner):
    """Test organizing files by keyword."""
    mock_organizer = MagicMock()
    mock_organizer_class.return_value = mock_organizer

    result = runner.invoke(main, [
        'organize', '--keyword', 'project_alpha'
    ])

    assert result.exit_code == 0
    assert "✓ Organized" in result.output
    assert "keyword 'project_alpha'" in result.output
    mock_organizer.move_specific_files.assert_called_once_with(keyword='project_alpha')

@patch('labrat.cli.FileOrganizer')
def test_organize_pictures_and_videos(mock_organizer_class, runner):
    """Test organizing pictures and videos."""
    mock_organizer = MagicMock()
    mock_organizer_class.return_value = mock_organizer

    result = runner.invoke(main, ['organize', '--pictures', '--videos'])

    assert result.exit_code == 0
    assert "✓ Organized" in result.output
    mock_organizer.organize_files.assert_called_once()

@patch('labrat.cli.FileOrganizer')
def test_organize_archives(mock_organizer_class, runner):
    """Test organizing archive files."""
    mock_organizer = MagicMock()
    mock_organizer_class.return_value = mock_organizer

    result = runner.invoke(main, ['organize', '--archives'])

    assert result.exit_code == 0
    assert "✓ Organized" in result.output
    assert "archives" in result.output
    mock_organizer.organize_archives.assert_called_once()

@patch('labrat.cli.FileOrganizer')
def test_organize_all(mock_organizer_class, runner):
    """Test organizing all file types."""
    mock_organizer = MagicMock()
    mock_organizer_class.return_value = mock_organizer

    result = runner.invoke(main, ['organize', '--all'])

    assert result.exit_code == 0
    assert "✓ Organized" in result.output
    assert "all files" in result.output
    mock_organizer.organize_all.assert_called_once()

def test_organize_no_options(runner):
    """Test that organize command requires at least one option."""
    result = runner.invoke(main, ['organize'])

    assert result.exit_code != 0
    assert "Error: Specify at least one organization option" in result.output

@patch('labrat.cli.FileOrganizer')
def test_organize_multiple_options(mock_organizer_class, runner):
    """Test organizing with multiple options combined."""
    mock_organizer = MagicMock()
    mock_organizer_class.return_value = mock_organizer

    result = runner.invoke(main, [
        'organize', '--science', '--pictures', '--keyword', 'test'
    ])

    assert result.exit_code == 0
    assert "✓ Organized" in result.output
    mock_organizer.organize_science_files.assert_called_once()
    mock_organizer.organize_files.assert_called_once()
    mock_organizer.move_specific_files.assert_called_once_with(keyword='test')

@patch('labrat.cli.FileOrganizer')
def test_organize_error_handling(mock_organizer_class, runner):
    """Test error handling when organization fails."""
    mock_organizer = MagicMock()
    mock_organizer.organize_science_files.side_effect = PermissionError("Permission denied")
    mock_organizer_class.return_value = mock_organizer

    result = runner.invoke(main, ['organize', '--science'])

    assert result.exit_code != 0
    assert "✗ Error organizing files" in result.output

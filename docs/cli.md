# CLI Reference

labrat provides a command-line interface for common tasks.

## Commands

### Project Management

```bash
# Create a new project
labrat project new --type <type> --name <name> --path <path>

# List all projects
labrat project list

# Delete a project
labrat project delete --path <path>
```

### Archiving

```bash
labrat archive --source <source_dir> --destination <dest_dir> --name <name>
```

### File Organization

```bash
# Organize scientific files
labrat organize --science

# Organize by keyword
labrat organize --keyword <keyword>

# Organize all file types
labrat organize --all
```

For detailed help on any command:

```bash
labrat --help
labrat <command> --help
```

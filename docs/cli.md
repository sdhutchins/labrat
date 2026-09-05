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

### Biological Queries

```bash
# Query gene annotations from MyGene
labrat query gene BMPR2

# Display the lower-ranked MyGene candidates too
labrat query gene BMPR2 --all-matches

# Query variant annotations from MyVariant
labrat query variant rs429358

# Search biomedical literature with PubTator 3
labrat query literature "BMPR2 pulmonary arterial hypertension"

# Resolve normalized biological concepts before searching
labrat query literature --gene BMPR2 \
  --disease "pulmonary arterial hypertension"

# Require a text-mined relation between exactly two concepts
labrat query literature --gene BMPR2 \
  --disease "pulmonary arterial hypertension" \
  --relation associate
```

Gene queries default to human records. Use `--species` to select another
MyGene-supported species. All query commands accept `--format json` for the
raw provider response and retrieval provenance.

Gene output displays the highest MyGene `_score` result by default and notes
how many additional matches were returned. The score controls ranking within
the current query. It is not a measure of biological confidence.

The default output uses Rich tables and panels. Rich detects redirected output
and removes terminal color codes automatically.

MyVariant's primary genomic identifiers use the hg19 assembly. Its response
may include mapped coordinates for other assemblies when the source provides
them.

PubTator relations are text-mined associations. They should not be interpreted
as validated biological mechanisms without reviewing the cited publications.

For detailed help on any command:

```bash
labrat --help
labrat <command> --help
```

"""Rich terminal renderers for biological query results."""

from collections.abc import Iterable
from typing import Any

from rich import box
from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from labrat.query.models import QueryResult


def _as_records(value: Any) -> list[dict[str, Any]]:
    """Normalize provider fields that alternate between objects and lists."""
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def _unique_text(values: Iterable[Any]) -> list[str]:
    """Preserve provider order while removing empty and repeated values."""
    return list(dict.fromkeys(str(value) for value in values if value is not None))


def _short_list(values: Iterable[Any], maximum: int = 4) -> str:
    """Keep dense annotation collections readable without hiding their size."""
    items = _unique_text(values)
    if not items:
        return "Not reported"
    if len(items) <= maximum:
        return ", ".join(items)
    return f"{', '.join(items[:maximum])} (+{len(items) - maximum} more)"


def _provenance(result: QueryResult) -> Text:
    """Render provenance as a subdued footer rather than primary evidence."""
    details = [f"Source: {result.provider}"]
    if build_version := result.metadata.get("build_version"):
        details.append(f"build {build_version}")
    if assembly := result.metadata.get("primary_assembly"):
        details.append(f"primary coordinates: {assembly}")
    details.append(f"retrieved {result.retrieved_at}")
    return Text("  •  ".join(details), style="dim")


def _nested_values(value: Any, key: str) -> list[Any]:
    values: list[Any] = []
    for record in _as_records(value):
        nested_value = record.get(key)
        if isinstance(nested_value, list):
            values.extend(nested_value)
        elif nested_value is not None:
            values.append(nested_value)
    return values


def _ranked_gene_hits(result: QueryResult) -> list[dict[str, Any]]:
    hits = result.data.get("hits", [])
    if not isinstance(hits, list):
        return []
    # MyGene _score ranks search matches; an absent score belongs after scored hits.
    return sorted(
        (hit for hit in hits if isinstance(hit, dict)),
        key=lambda hit: float(hit.get("_score", float("-inf"))),
        reverse=True,
    )


def _gene_details(hit: dict[str, Any], species: str) -> Table:
    details = Table.grid(padding=(0, 2))
    details.add_column(style="bold cyan", no_wrap=True)
    details.add_column(ratio=1)
    details.add_row("Name", str(hit.get("name", "Not reported")))
    details.add_row("Symbol", str(hit.get("symbol", "Not reported")))
    details.add_row(
        "Entrez",
        str(hit.get("entrezgene", hit.get("_id", "Not reported"))),
    )
    details.add_row("Ensembl", _short_list(_nested_values(hit.get("ensembl"), "gene")))
    details.add_row(
        "UniProt",
        _short_list(_nested_values(hit.get("uniprot"), "Swiss-Prot")),
    )
    details.add_row("RefSeq RNA", _short_list(_nested_values(hit.get("refseq"), "rna")))
    details.add_row(
        "RefSeq protein",
        _short_list(_nested_values(hit.get("refseq"), "protein")),
    )
    details.add_row("Taxonomy", f"{species} · {hit.get('taxid', 'Not reported')}")
    return details


def _gene_alternatives(hits: list[dict[str, Any]]) -> Table:
    table = Table(
        title="Additional MyGene matches",
        box=box.SIMPLE_HEAVY,
        header_style="bold cyan",
        expand=True,
    )
    table.add_column("Rank", justify="right", style="dim", no_wrap=True)
    table.add_column("Symbol", style="bold", no_wrap=True)
    table.add_column("Name", ratio=3)
    table.add_column("Record", no_wrap=True)
    table.add_column("MyGene score", justify="right", no_wrap=True)

    for rank, hit in enumerate(hits, start=2):
        table.add_row(
            str(rank),
            str(hit.get("symbol", "Unknown")),
            str(hit.get("name", "Not reported")),
            str(hit.get("entrezgene", hit.get("_id", "Not reported"))),
            str(hit.get("_score", "Not reported")),
        )
    return table


def _gene_result(
    result: QueryResult,
    show_all_matches: bool,
) -> RenderableType:
    """Prioritize MyGene's top score while making alternatives discoverable."""
    hits = _ranked_gene_hits(result)
    if not hits:
        return Panel(
            "No matching genes found.", title="Gene query", border_style="yellow"
        )

    # The top panel reflects search relevance, not biological confidence.
    top_hit = hits[0]
    top_score = top_hit.get("_score", "Not reported")
    content = Group(
        _gene_details(top_hit, str(result.metadata.get("species", "unknown"))),
        Text(""),
        Text("Summary", style="bold cyan"),
        Text(str(top_hit.get("summary", "No summary reported."))),
    )
    top_panel = Panel(
        content,
        title=f"Highest-ranked MyGene match · {result.query}",
        subtitle=f"MyGene score {top_score}",
        subtitle_align="right",
        border_style="cyan",
    )

    if len(hits) == 1:
        return top_panel

    additional_count = len(hits) - 1
    match_label = "match" if additional_count == 1 else "matches"
    alternatives_notice = Text(
        f"{additional_count} additional {match_label} returned. "
        "Use --all-matches to display them.",
        style="dim",
    )
    if not show_all_matches:
        return Group(top_panel, alternatives_notice)
    return Group(top_panel, _gene_alternatives(hits[1:]))


def _variant_rsids(hit: dict[str, Any]) -> str:
    return _short_list(record.get("rsid") for record in _as_records(hit.get("dbsnp")))


def _variant_genes(hit: dict[str, Any]) -> str:
    symbols: list[Any] = []
    for clinvar in _as_records(hit.get("clinvar")):
        symbols.extend(gene.get("symbol") for gene in _as_records(clinvar.get("gene")))
    return _short_list(symbols)


def _clinvar_labels(hit: dict[str, Any]) -> str:
    labels: list[Any] = []
    # Keep labels distinct because each RCV record can describe a different condition.
    for clinvar in _as_records(hit.get("clinvar")):
        labels.extend(
            record.get("clinical_significance")
            for record in _as_records(clinvar.get("rcv"))
        )
    return _short_list(labels)


def _cadd_phred(hit: dict[str, Any]) -> str:
    return _short_list(record.get("phred") for record in _as_records(hit.get("cadd")))


def _allele_frequency(hit: dict[str, Any], source: str) -> str:
    values: list[Any] = []
    # Show the overall frequency here; population-specific values remain in JSON.
    for record in _as_records(hit.get(source)):
        for frequency in _as_records(record.get("af")):
            values.append(frequency.get("af"))
    return _short_list(values)


def _variant_panels(result: QueryResult) -> RenderableType:
    """Give each allele its own panel and keep condition labels qualified."""
    hits = result.data.get("hits", [])
    if not hits:
        return Panel(
            "No matching variants found.",
            title="Variant query",
            border_style="yellow",
        )

    panels: list[RenderableType] = []
    for index, hit in enumerate(hits, start=1):
        fields = Table.grid(padding=(0, 2))
        fields.add_column(style="bold cyan", no_wrap=True)
        fields.add_column(ratio=1)
        fields.add_row("dbSNP", _variant_rsids(hit))
        fields.add_row("Gene", _variant_genes(hit))
        fields.add_row("ClinVar record labels", _clinvar_labels(hit))
        fields.add_row("CADD PHRED", _cadd_phred(hit))
        fields.add_row("gnomAD exome AF", _allele_frequency(hit, "gnomad_exome"))
        fields.add_row("gnomAD genome AF", _allele_frequency(hit, "gnomad_genome"))

        title = str(hit.get("_id", f"Allele {index}"))
        panels.append(Panel(fields, title=title, border_style="cyan"))

    panels.append(Text("ClinVar labels are condition-specific.", style="dim italic"))
    return Group(*panels)


def _publication_text(publication: dict[str, Any]) -> Text:
    title = Text(str(publication.get("title", "Untitled publication")), style="bold")
    authors = publication.get("authors", [])
    if isinstance(authors, list) and authors:
        visible_authors = ", ".join(str(author) for author in authors[:3])
        suffix = " et al." if len(authors) > 3 else ""
        title.append(f"\n{visible_authors}{suffix}", style="dim")
    return title


def _citation_text(publication: dict[str, Any]) -> Text:
    journal = publication.get("journal", "Unknown journal")
    date = publication.get("meta_date_publication", publication.get("date", ""))
    citation = Text(f"{journal} · {date}")

    if pmid := publication.get("pmid"):
        citation.append("\nPMID: ", style="dim")
        citation.append(
            str(pmid),
            style=f"cyan link https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        )
    if doi := publication.get("doi"):
        citation.append("\nDOI: ", style="dim")
        citation.append(str(doi), style=f"cyan link https://doi.org/{doi}")
    return citation


def _literature_table(result: QueryResult) -> RenderableType:
    """Render compact citations without interpreting PubTator rankings."""
    publications = result.data.get("results", [])
    if not publications:
        return Panel(
            "No matching publications found.",
            title="Literature query",
            border_style="yellow",
        )

    display_limit = int(result.metadata.get("display_limit", len(publications)))
    table = Table(
        title="Literature results",
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
        expand=True,
    )
    table.add_column("#", justify="right", style="dim", no_wrap=True)
    table.add_column("Publication", ratio=3)
    table.add_column("Citation", ratio=2)

    for index, publication in enumerate(publications[:display_limit], start=1):
        table.add_row(
            str(index),
            _publication_text(publication),
            _citation_text(publication),
        )
    return table


def render_query_result(
    result: QueryResult,
    console: Console | None = None,
    show_all_gene_matches: bool = False,
) -> None:
    """Render one query result with terminal-aware Rich formatting."""
    # Build at render time so Click capture and TTY detection use current stdout.
    output_console = console or Console(highlight=False)
    if result.kind == "gene":
        rendered_result = _gene_result(result, show_all_gene_matches)
    else:
        renderers = {
            "variant": _variant_panels,
            "literature": _literature_table,
        }
        rendered_result = renderers[result.kind](result)
    output_console.print(rendered_result)
    output_console.print(_provenance(result))

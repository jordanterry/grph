"""Output formatters for table and JSON display."""

import json
from typing import Any, Iterable

from rich.console import Console
from rich.table import Table

from .models import (
    Edge,
    GraphMetadata,
    Node,
    PathResult,
    GraphStats,
    CentralityResult,
    ComponentInfo,
)


def format_json(data: Any) -> str:
    """Format data as JSON string.

    Args:
        data: Data to serialize. Can be a dict, list, or model object.

    Returns:
        Pretty-printed JSON string.
    """
    if hasattr(data, "to_dict"):
        data = data.to_dict()
    elif isinstance(data, list):
        data = [item.to_dict() if hasattr(item, "to_dict") else item for item in data]

    return json.dumps(data, indent=2, default=str)


def print_json(data: Any, console: Console | None = None) -> None:
    """Print data as JSON to console.

    Args:
        data: Data to serialize and print.
        console: Rich console to use. Creates a new one if not provided.
    """
    console = console or Console()
    console.print(format_json(data))


def print_metadata_table(metadata: GraphMetadata, console: Console | None = None) -> None:
    """Print metadata as a formatted table.

    Args:
        metadata: Graph metadata to display.
        console: Rich console to use.
    """
    console = console or Console()

    table = Table(title="Graph Metadata", show_header=True, header_style="bold cyan")
    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Version", metadata.version or "N/A")
    table.add_row("Creator", metadata.creator or "N/A")
    table.add_row("Description", metadata.description or "N/A")
    table.add_row("Last Modified", metadata.last_modified or "N/A")
    table.add_row("Mode", metadata.mode)
    table.add_row("Default Edge Type", metadata.default_edge_type)
    table.add_row("Node Count", str(metadata.node_count))
    table.add_row("Edge Count", str(metadata.edge_count))

    console.print(table)


def print_nodes_table(
    nodes: Iterable[Node],
    show_attributes: bool = True,
    console: Console | None = None,
) -> None:
    """Print nodes as a formatted table.

    Args:
        nodes: Iterable of nodes to display.
        show_attributes: Whether to show the attributes column.
        console: Rich console to use.
    """
    console = console or Console()
    nodes_list = list(nodes)

    if not nodes_list:
        console.print("[yellow]No nodes found matching the filters.[/yellow]")
        return

    table = Table(title=f"Nodes ({len(nodes_list)})", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="bold")
    table.add_column("Label")
    if show_attributes:
        table.add_column("Attributes")

    for node in nodes_list:
        attrs_str = ""
        if show_attributes and node.attributes:
            attrs_str = ", ".join(f"{k}={v}" for k, v in node.attributes.items())

        table.add_row(
            node.id,
            node.label or "",
            attrs_str if show_attributes else None,
        )

    console.print(table)


def print_edges_table(
    edges: Iterable[Edge],
    show_attributes: bool = True,
    console: Console | None = None,
) -> None:
    """Print edges as a formatted table.

    Args:
        edges: Iterable of edges to display.
        show_attributes: Whether to show the attributes column.
        console: Rich console to use.
    """
    console = console or Console()
    edges_list = list(edges)

    if not edges_list:
        console.print("[yellow]No edges found matching the filters.[/yellow]")
        return

    table = Table(title=f"Edges ({len(edges_list)})", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="bold")
    table.add_column("Source")
    table.add_column("Target")
    table.add_column("Weight")
    table.add_column("Type")
    if show_attributes:
        table.add_column("Attributes")

    for edge in edges_list:
        attrs_str = ""
        if show_attributes and edge.attributes:
            attrs_str = ", ".join(f"{k}={v}" for k, v in edge.attributes.items())

        table.add_row(
            edge.id or "",
            edge.source,
            edge.target,
            str(edge.weight) if edge.weight is not None else "",
            edge.edge_type or "",
            attrs_str if show_attributes else None,
        )

    console.print(table)


def print_info_table(info: dict[str, Any], console: Console | None = None) -> None:
    """Print graph info summary as a formatted table.

    Args:
        info: Graph info dictionary.
        console: Rich console to use.
    """
    console = console or Console()

    # Main info table
    table = Table(title="Graph Summary", show_header=True, header_style="bold cyan")
    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("File", info.get("file", "N/A"))
    table.add_row("Version", info.get("version") or "N/A")
    table.add_row("Mode", info.get("mode", "N/A"))
    table.add_row("Default Edge Type", info.get("default_edge_type", "N/A"))
    table.add_row("Node Count", str(info.get("node_count", 0)))
    table.add_row("Edge Count", str(info.get("edge_count", 0)))

    console.print(table)
    console.print()

    # Node attributes
    node_attrs = info.get("node_attributes", [])
    if node_attrs:
        console.print("[bold]Node Attributes:[/bold]", ", ".join(node_attrs))
    else:
        console.print("[bold]Node Attributes:[/bold] [dim]None[/dim]")

    # Edge attributes
    edge_attrs = info.get("edge_attributes", [])
    if edge_attrs:
        console.print("[bold]Edge Attributes:[/bold]", ", ".join(edge_attrs))
    else:
        console.print("[bold]Edge Attributes:[/bold] [dim]None[/dim]")


def print_path_result(
    path_result: PathResult | None,
    console: Console | None = None,
) -> None:
    """Print a path result as a formatted display.

    Args:
        path_result: Path result to display, or None if no path.
        console: Rich console to use.
    """
    console = console or Console()

    if path_result is None:
        console.print("[yellow]No path found between the nodes.[/yellow]")
        return

    console.print(f"[bold]Path from[/bold] {path_result.source} [bold]to[/bold] {path_result.target}")
    console.print(f"[bold]Length:[/bold] {path_result.length} edges")
    if path_result.total_weight is not None:
        console.print(f"[bold]Total Weight:[/bold] {path_result.total_weight}")
    console.print()
    console.print("[bold]Path:[/bold]", " → ".join(path_result.path))


def print_paths_list(
    paths: list[PathResult],
    console: Console | None = None,
) -> None:
    """Print multiple paths as a formatted display.

    Args:
        paths: List of path results.
        console: Rich console to use.
    """
    console = console or Console()

    if not paths:
        console.print("[yellow]No paths found between the nodes.[/yellow]")
        return

    console.print(f"[bold]Found {len(paths)} path(s)[/bold]")
    console.print()

    for i, path in enumerate(paths, 1):
        console.print(f"[cyan]Path {i}[/cyan] (length {path.length}):")
        console.print("  " + " → ".join(path.path))


def print_stats_table(stats: GraphStats, console: Console | None = None) -> None:
    """Print graph statistics as a formatted table.

    Args:
        stats: Graph statistics to display.
        console: Rich console to use.
    """
    console = console or Console()

    table = Table(title="Graph Statistics", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="bold")
    table.add_column("Value")

    table.add_row("Node Count", str(stats.node_count))
    table.add_row("Edge Count", str(stats.edge_count))
    table.add_row("Directed", "Yes" if stats.is_directed else "No")
    table.add_row("Density", f"{stats.density:.4f}")
    table.add_row("Average Degree", f"{stats.avg_degree:.2f}")
    table.add_row("Avg Clustering Coefficient", f"{stats.avg_clustering:.4f}")
    table.add_row("Connected", "Yes" if stats.is_connected else "No")
    table.add_row("Number of Components", str(stats.num_components))
    table.add_row("Has Cycles", "Yes" if stats.has_cycles else "No")

    if stats.diameter is not None:
        table.add_row("Diameter", str(stats.diameter))
    if stats.radius is not None:
        table.add_row("Radius", str(stats.radius))
    if stats.avg_path_length is not None:
        table.add_row("Avg Path Length", f"{stats.avg_path_length:.4f}")

    console.print(table)


def print_centrality_table(
    result: CentralityResult,
    top_n: int = 10,
    console: Console | None = None,
) -> None:
    """Print centrality scores as a formatted table.

    Args:
        result: Centrality result to display.
        top_n: Number of top nodes to show.
        console: Rich console to use.
    """
    console = console or Console()

    table = Table(
        title=f"{result.centrality_type.title()} Centrality (Top {top_n})",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Rank", style="dim")
    table.add_column("Node", style="bold")
    table.add_column("Score")

    for i, (node, score) in enumerate(result.top_n(top_n), 1):
        table.add_row(str(i), node, f"{score:.6f}")

    console.print(table)


def print_components_table(
    info: ComponentInfo,
    show_members: bool = False,
    console: Console | None = None,
) -> None:
    """Print component information as a formatted table.

    Args:
        info: Component info to display.
        show_members: Whether to show component members.
        console: Rich console to use.
    """
    console = console or Console()

    console.print(f"[bold]Number of Components:[/bold] {info.num_components}")
    console.print(f"[bold]Largest Component Size:[/bold] {info.largest_component_size}")
    console.print()

    if info.num_components > 0:
        table = Table(title="Components", show_header=True, header_style="bold cyan")
        table.add_column("Component", style="dim")
        table.add_column("Size")
        if show_members:
            table.add_column("Members")

        for i, (size, members) in enumerate(zip(info.component_sizes, info.components), 1):
            if show_members:
                # Truncate long member lists
                member_str = ", ".join(members[:10])
                if len(members) > 10:
                    member_str += f", ... (+{len(members) - 10} more)"
                table.add_row(str(i), str(size), member_str)
            else:
                table.add_row(str(i), str(size))

        console.print(table)


def print_degree_table(
    degree_info: dict[str, Any],
    top_n: int = 10,
    console: Console | None = None,
) -> None:
    """Print degree information as a formatted table.

    Args:
        degree_info: Degree information dictionary.
        top_n: Number of top nodes to show.
        console: Rich console to use.
    """
    console = console or Console()

    if "node" in degree_info:
        # Single node degree
        table = Table(title="Node Degree", show_header=True, header_style="bold cyan")
        table.add_column("Property", style="bold")
        table.add_column("Value")

        table.add_row("Node", degree_info["node"])
        if "in_degree" in degree_info:
            table.add_row("In-Degree", str(degree_info["in_degree"]))
            table.add_row("Out-Degree", str(degree_info["out_degree"]))
            table.add_row("Total Degree", str(degree_info["total_degree"]))
        else:
            table.add_row("Degree", str(degree_info["degree"]))

        console.print(table)
    else:
        # All nodes degree list
        degrees = degree_info.get("degrees", [])[:top_n]
        is_directed = "in_degree" in degrees[0] if degrees else False

        table = Table(
            title=f"Node Degrees (Top {top_n})",
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Rank", style="dim")
        table.add_column("Node", style="bold")

        if is_directed:
            table.add_column("In")
            table.add_column("Out")
            table.add_column("Total")

            for i, d in enumerate(degrees, 1):
                table.add_row(
                    str(i),
                    d["node"],
                    str(d["in_degree"]),
                    str(d["out_degree"]),
                    str(d["total_degree"]),
                )
        else:
            table.add_column("Degree")

            for i, d in enumerate(degrees, 1):
                table.add_row(str(i), d["node"], str(d["degree"]))

        console.print(table)

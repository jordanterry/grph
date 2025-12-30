"""CLI entry point for the gfx tool."""

import sys
from pathlib import Path

import click
from rich.console import Console

from . import __version__
from .formatters import (
    print_edges_table,
    print_info_table,
    print_json,
    print_metadata_table,
    print_nodes_table,
    print_path_result,
    print_paths_list,
    print_stats_table,
    print_centrality_table,
    print_components_table,
    print_degree_table,
)
from .models import CentralityType, ExportFormat
from .parser import GEXFGraph, GEXFParseError


console = Console()


def parse_attr_filter(
    ctx: click.Context, param: click.Parameter, value: tuple[str, ...]
) -> list[tuple[str, str]]:
    """Parse attribute filters in key=value format.

    Args:
        ctx: Click context.
        param: Click parameter.
        value: Tuple of key=value strings.

    Returns:
        List of (key, value) tuples.
    """
    filters = []
    for item in value:
        if "=" not in item:
            raise click.BadParameter(
                f"Invalid format '{item}'. Expected key=value format."
            )
        key, val = item.split("=", 1)
        filters.append((key.strip(), val.strip()))
    return filters


def load_graph(file_path: str) -> GEXFGraph:
    """Load a GEXF graph, handling errors gracefully.

    Args:
        file_path: Path to the GEXF file.

    Returns:
        Parsed GEXFGraph object.

    Raises:
        SystemExit: If the file cannot be parsed.
    """
    try:
        return GEXFGraph(file_path)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@click.group()
@click.version_option(version=__version__, prog_name="gfx")
def main() -> None:
    """GFX - A CLI tool for interrogating and browsing GEXF graph files.

    GEXF (Graph Exchange XML Format) is a standard format for representing
    graph data, commonly used with tools like Gephi.

    Examples:

        gfx info graph.gexf

        gfx nodes graph.gexf --attr type=server

        gfx edges graph.gexf --source node1 --json
    """
    pass


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def meta(file: str, as_json: bool) -> None:
    """Display metadata from a GEXF file.

    Shows information like creator, description, last modified date,
    graph mode, and default edge type.
    """
    graph = load_graph(file)

    if as_json:
        print_json(graph.metadata, console)
    else:
        print_metadata_table(graph.metadata, console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def info(file: str, as_json: bool) -> None:
    """Display a summary of the graph.

    Shows node/edge counts and available attributes.
    """
    graph = load_graph(file)
    info_data = graph.get_info()

    if as_json:
        print_json(info_data, console)
    else:
        print_info_table(info_data, console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--attr",
    "attr_filters",
    multiple=True,
    callback=parse_attr_filter,
    help="Filter by attribute (key=value). Can be specified multiple times.",
)
@click.option(
    "--label",
    "label_pattern",
    help="Filter by label pattern (supports * and ? wildcards).",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option(
    "--no-attrs",
    is_flag=True,
    help="Hide the attributes column in table output.",
)
def nodes(
    file: str,
    attr_filters: list[tuple[str, str]],
    label_pattern: str | None,
    as_json: bool,
    no_attrs: bool,
) -> None:
    """List and filter nodes in the graph.

    Examples:

        gfx nodes graph.gexf

        gfx nodes graph.gexf --attr type=server

        gfx nodes graph.gexf --label "Server*" --json
    """
    graph = load_graph(file)
    matching_nodes = list(graph.nodes(attr_filters=attr_filters, label_pattern=label_pattern))

    if as_json:
        print_json(matching_nodes, console)
    else:
        print_nodes_table(matching_nodes, show_attributes=not no_attrs, console=console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--attr",
    "attr_filters",
    multiple=True,
    callback=parse_attr_filter,
    help="Filter by attribute (key=value). Can be specified multiple times.",
)
@click.option("--source", "source_filter", help="Filter by source node ID.")
@click.option("--target", "target_filter", help="Filter by target node ID.")
@click.option(
    "--type",
    "type_filter",
    help="Filter by edge type (e.g., directed, undirected).",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option(
    "--no-attrs",
    is_flag=True,
    help="Hide the attributes column in table output.",
)
def edges(
    file: str,
    attr_filters: list[tuple[str, str]],
    source_filter: str | None,
    target_filter: str | None,
    type_filter: str | None,
    as_json: bool,
    no_attrs: bool,
) -> None:
    """List and filter edges in the graph.

    Examples:

        gfx edges graph.gexf

        gfx edges graph.gexf --source node1

        gfx edges graph.gexf --attr weight=1.0 --json
    """
    graph = load_graph(file)
    matching_edges = list(
        graph.edges(
            attr_filters=attr_filters,
            source_filter=source_filter,
            target_filter=target_filter,
            type_filter=type_filter,
        )
    )

    if as_json:
        print_json(matching_edges, console)
    else:
        print_edges_table(matching_edges, show_attributes=not no_attrs, console=console)


# =============================================================================
# Graph Traversal Commands
# =============================================================================


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("node_id")
@click.option(
    "--direction",
    type=click.Choice(["in", "out", "all"]),
    default="all",
    help="Direction for directed graphs (in=predecessors, out=successors, all=both).",
)
@click.option(
    "--depth",
    type=int,
    default=1,
    help="Number of hops to traverse (default: 1).",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def neighbors(
    file: str,
    node_id: str,
    direction: str,
    depth: int,
    as_json: bool,
) -> None:
    """Find neighbors of a node.

    Shows nodes directly connected to NODE_ID. Use --depth for multi-hop
    neighbors and --direction for directed graphs.

    Examples:

        gfx neighbors graph.gexf server1

        gfx neighbors graph.gexf lb1 --direction out --depth 2
    """
    graph = load_graph(file)

    try:
        neighbor_nodes = graph.neighbors(node_id, direction=direction, depth=depth)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if as_json:
        print_json(neighbor_nodes, console)
    else:
        if neighbor_nodes:
            console.print(f"[bold]Neighbors of {node_id}[/bold] (depth={depth}, direction={direction})")
            console.print()
            print_nodes_table(neighbor_nodes, console=console)
        else:
            console.print(f"[yellow]No neighbors found for node {node_id}.[/yellow]")


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("source")
@click.argument("target")
@click.option("--weighted", is_flag=True, help="Use edge weights for path calculation.")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def path(
    file: str,
    source: str,
    target: str,
    weighted: bool,
    as_json: bool,
) -> None:
    """Find the shortest path between two nodes.

    Examples:

        gfx path graph.gexf server1 db1

        gfx path graph.gexf lb1 cache1 --weighted
    """
    graph = load_graph(file)

    try:
        result = graph.shortest_path(source, target, weighted=weighted)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if as_json:
        print_json(result, console)
    else:
        print_path_result(result, console)


@main.command(name="all-paths")
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("source")
@click.argument("target")
@click.option(
    "--max-depth",
    type=int,
    default=None,
    help="Maximum path length.",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def all_paths(
    file: str,
    source: str,
    target: str,
    max_depth: int | None,
    as_json: bool,
) -> None:
    """Find all simple paths between two nodes.

    Examples:

        gfx all-paths graph.gexf lb1 db1

        gfx all-paths graph.gexf lb1 cache1 --max-depth 3
    """
    graph = load_graph(file)

    try:
        paths = graph.all_paths(source, target, max_depth=max_depth)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if as_json:
        print_json(paths, console)
    else:
        print_paths_list(paths, console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("source")
@click.argument("target")
def has_path(file: str, source: str, target: str) -> None:
    """Check if a path exists between two nodes.

    Examples:

        gfx has-path graph.gexf lb1 db1
    """
    graph = load_graph(file)
    exists = graph.has_path(source, target)

    if exists:
        console.print(f"[green]Yes[/green] - a path exists from {source} to {target}")
    else:
        console.print(f"[red]No[/red] - no path exists from {source} to {target}")


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("node_id")
@click.option(
    "--direction",
    type=click.Choice(["forward", "backward", "both"]),
    default="forward",
    help="Direction to traverse (forward=descendants, backward=ancestors).",
)
@click.option(
    "--max-depth",
    type=int,
    default=None,
    help="Maximum traversal depth.",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def reachable(
    file: str,
    node_id: str,
    direction: str,
    max_depth: int | None,
    as_json: bool,
) -> None:
    """Find all nodes reachable from a given node.

    Examples:

        gfx reachable graph.gexf lb1

        gfx reachable graph.gexf db1 --direction backward
    """
    graph = load_graph(file)

    try:
        reachable_nodes = graph.reachable(node_id, direction=direction, max_depth=max_depth)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if as_json:
        print_json(reachable_nodes, console)
    else:
        if reachable_nodes:
            console.print(
                f"[bold]Nodes reachable from {node_id}[/bold] (direction={direction})"
            )
            console.print()
            print_nodes_table(reachable_nodes, console=console)
        else:
            console.print(f"[yellow]No nodes reachable from {node_id}.[/yellow]")


@main.command(name="common-neighbors")
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("node1")
@click.argument("node2")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def common_neighbors_cmd(
    file: str,
    node1: str,
    node2: str,
    as_json: bool,
) -> None:
    """Find nodes that are neighbors of both given nodes.

    Examples:

        gfx common-neighbors graph.gexf server1 server2
    """
    graph = load_graph(file)

    try:
        common = graph.common_neighbors(node1, node2)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if as_json:
        print_json(common, console)
    else:
        if common:
            console.print(f"[bold]Common neighbors of {node1} and {node2}[/bold]")
            console.print()
            print_nodes_table(common, console=console)
        else:
            console.print(
                f"[yellow]No common neighbors found between {node1} and {node2}.[/yellow]"
            )


# =============================================================================
# Graph Analysis Commands
# =============================================================================


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def stats(file: str, as_json: bool) -> None:
    """Display comprehensive graph statistics.

    Shows density, connectivity, cycles, clustering, and more.

    Examples:

        gfx stats graph.gexf
    """
    graph = load_graph(file)
    graph_stats = graph.get_stats()

    if as_json:
        print_json(graph_stats, console)
    else:
        print_stats_table(graph_stats, console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--type",
    "centrality_type",
    type=click.Choice(["degree", "betweenness", "closeness", "pagerank", "eigenvector"]),
    default="degree",
    help="Type of centrality to calculate.",
)
@click.option(
    "--top",
    "top_n",
    type=int,
    default=10,
    help="Number of top nodes to display.",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def centrality(
    file: str,
    centrality_type: str,
    top_n: int,
    as_json: bool,
) -> None:
    """Calculate centrality metrics for nodes.

    Identifies the most important or influential nodes in the graph.

    Examples:

        gfx centrality graph.gexf

        gfx centrality graph.gexf --type pagerank --top 20
    """
    graph = load_graph(file)

    ctype = CentralityType(centrality_type)
    result = graph.get_centrality(ctype)

    if as_json:
        print_json(result, console)
    else:
        print_centrality_table(result, top_n=top_n, console=console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--type",
    "component_type",
    type=click.Choice(["connected", "strongly", "weakly"]),
    default="connected",
    help="Type of components (strongly/weakly for directed graphs).",
)
@click.option("--list", "show_members", is_flag=True, help="Show component members.")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def components(
    file: str,
    component_type: str,
    show_members: bool,
    as_json: bool,
) -> None:
    """Analyze connected components in the graph.

    Shows how many disconnected clusters exist and their sizes.

    Examples:

        gfx components graph.gexf

        gfx components graph.gexf --type strongly --list
    """
    graph = load_graph(file)
    result = graph.get_components(component_type)

    if as_json:
        print_json(result, console)
    else:
        print_components_table(result, show_members=show_members, console=console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--node", "node_id", help="Show degree for a specific node.")
@click.option(
    "--top",
    "top_n",
    type=int,
    default=10,
    help="Number of top nodes to display.",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def degree(
    file: str,
    node_id: str | None,
    top_n: int,
    as_json: bool,
) -> None:
    """Show node degree information.

    For directed graphs, shows in-degree, out-degree, and total degree.

    Examples:

        gfx degree graph.gexf

        gfx degree graph.gexf --node server1

        gfx degree graph.gexf --top 20
    """
    graph = load_graph(file)

    try:
        result = graph.get_degree(node_id)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if as_json:
        print_json(result, console)
    else:
        print_degree_table(result, top_n=top_n, console=console)


# =============================================================================
# Subgraph Commands
# =============================================================================


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("node_id")
@click.option(
    "--radius",
    type=int,
    default=1,
    help="Number of hops to include (default: 1).",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Save subgraph to a file (GEXF format).",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def ego(
    file: str,
    node_id: str,
    radius: int,
    output: str | None,
    as_json: bool,
) -> None:
    """Extract the ego graph (neighborhood) around a node.

    The ego graph includes the center node and all nodes within
    the specified radius, along with edges between them.

    Examples:

        gfx ego graph.gexf server1

        gfx ego graph.gexf lb1 --radius 2

        gfx ego graph.gexf server1 --output server1-ego.gexf
    """
    graph = load_graph(file)

    try:
        ego_graph = graph.ego_graph(node_id, radius=radius)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if output:
        # Export as GEXF
        import networkx as nx

        nx.write_gexf(ego_graph._graph, output)
        console.print(f"[green]Saved ego graph to {output}[/green]")
    elif as_json:
        # Output info as JSON
        print_json(ego_graph.get_info(), console)
    else:
        # Display summary
        console.print(f"[bold]Ego graph for {node_id}[/bold] (radius={radius})")
        console.print()
        print_info_table(ego_graph.get_info(), console)


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--nodes",
    "node_ids",
    required=True,
    help="Comma-separated list of node IDs to include.",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Save subgraph to a file (GEXF format).",
)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def subgraph(
    file: str,
    node_ids: str,
    output: str | None,
    as_json: bool,
) -> None:
    """Extract a subgraph containing only specified nodes.

    Creates a subgraph with the specified nodes and all edges
    between them.

    Examples:

        gfx subgraph graph.gexf --nodes server1,server2,db1

        gfx subgraph graph.gexf --nodes lb1,server1 --output subset.gexf
    """
    graph = load_graph(file)

    nodes_list = [n.strip() for n in node_ids.split(",")]

    try:
        sub = graph.subgraph(nodes_list)
    except GEXFParseError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if output:
        # Export as GEXF
        import networkx as nx

        nx.write_gexf(sub._graph, output)
        console.print(f"[green]Saved subgraph to {output}[/green]")
    elif as_json:
        print_json(sub.get_info(), console)
    else:
        console.print(f"[bold]Subgraph[/bold] with nodes: {', '.join(nodes_list)}")
        console.print()
        print_info_table(sub.get_info(), console)


# =============================================================================
# Export Commands
# =============================================================================


@main.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--format",
    "export_format",
    type=click.Choice(["json", "graphml", "adjlist", "edgelist"]),
    default="json",
    help="Output format.",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Output file (default: stdout).",
)
def export(file: str, export_format: str, output: str | None) -> None:
    """Export the graph to different formats.

    Supported formats:
    - json: Node-link JSON format
    - graphml: GraphML XML format
    - adjlist: Adjacency list (node followed by neighbors)
    - edgelist: Edge list (source target [weight])

    Examples:

        gfx export graph.gexf --format json

        gfx export graph.gexf --format graphml --output graph.graphml
    """
    graph = load_graph(file)

    fmt = ExportFormat(export_format)
    result = graph.export(fmt)

    if output:
        Path(output).write_text(result)
        console.print(f"[green]Exported to {output}[/green]")
    else:
        console.print(result)


if __name__ == "__main__":
    main()

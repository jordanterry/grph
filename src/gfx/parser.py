"""GEXF file parser using NetworkX and ElementTree."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterator

import networkx as nx

from .models import (
    Edge,
    GraphMetadata,
    Node,
    PathResult,
    GraphStats,
    CentralityResult,
    ComponentInfo,
    CentralityType,
    ExportFormat,
)


class GEXFParseError(Exception):
    """Raised when a GEXF file cannot be parsed."""

    pass


class GEXFGraph:
    """A parsed GEXF graph with metadata and query capabilities."""

    # Known GEXF namespaces
    NAMESPACES = {
        "1.0": "http://www.gephi.org/gexf",
        "1.1": "http://www.gephi.org/gexf/1.1draft",
        "1.2": "http://gexf.net/1.2draft",
        "1.3": "http://gexf.net/1.3",
    }

    def __init__(self, file_path: str | Path):
        """Parse a GEXF file.

        Args:
            file_path: Path to the GEXF file.

        Raises:
            GEXFParseError: If the file cannot be parsed.
        """
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise GEXFParseError(f"File not found: {file_path}")

        if not self.file_path.is_file():
            raise GEXFParseError(f"Not a file: {file_path}")

        try:
            # Parse with NetworkX for graph structure
            self._graph = nx.read_gexf(str(self.file_path))
        except Exception as e:
            raise GEXFParseError(f"Failed to parse GEXF file: {e}") from e

        # Parse metadata directly from XML
        self._metadata = self._parse_metadata()
        self._node_attr_keys: set[str] = set()
        self._edge_attr_keys: set[str] = set()
        self._collect_attribute_keys()

    def _detect_namespace(self, root: ET.Element) -> str | None:
        """Detect the GEXF namespace from the root element."""
        # Try to extract namespace from the tag
        if root.tag.startswith("{"):
            ns_end = root.tag.index("}")
            return root.tag[1:ns_end]
        return None

    def _parse_metadata(self) -> GraphMetadata:
        """Parse metadata from the GEXF file XML."""
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise GEXFParseError(f"Invalid XML: {e}") from e

        ns = self._detect_namespace(root)
        ns_prefix = f"{{{ns}}}" if ns else ""

        # Extract version from root
        version = root.get("version")

        # Find meta element
        meta = root.find(f"{ns_prefix}meta")

        creator = None
        description = None
        last_modified = None

        if meta is not None:
            last_modified = meta.get("lastmodifieddate")
            creator_elem = meta.find(f"{ns_prefix}creator")
            desc_elem = meta.find(f"{ns_prefix}description")

            if creator_elem is not None:
                creator = creator_elem.text
            if desc_elem is not None:
                description = desc_elem.text

        # Find graph element for mode and default edge type
        graph = root.find(f"{ns_prefix}graph")
        mode = "static"
        default_edge_type = "undirected"

        if graph is not None:
            mode = graph.get("mode", "static")
            default_edge_type = graph.get("defaultedgetype", "undirected")

        return GraphMetadata(
            creator=creator,
            description=description,
            last_modified=last_modified,
            mode=mode,
            default_edge_type=default_edge_type,
            version=version,
            node_count=self._graph.number_of_nodes(),
            edge_count=self._graph.number_of_edges(),
        )

    def _collect_attribute_keys(self) -> None:
        """Collect all unique attribute keys from nodes and edges."""
        # Collect node attribute keys
        for _, attrs in self._graph.nodes(data=True):
            self._node_attr_keys.update(attrs.keys())

        # Collect edge attribute keys
        for _, _, attrs in self._graph.edges(data=True):
            self._edge_attr_keys.update(attrs.keys())

        # Remove 'label' as it's a standard field, not a custom attribute
        self._node_attr_keys.discard("label")

    @property
    def metadata(self) -> GraphMetadata:
        """Get the graph metadata."""
        return self._metadata

    def node_attribute_keys(self) -> list[str]:
        """Get all unique attribute keys used by nodes."""
        return sorted(self._node_attr_keys)

    def edge_attribute_keys(self) -> list[str]:
        """Get all unique attribute keys used by edges."""
        return sorted(self._edge_attr_keys)

    def nodes(
        self,
        attr_filters: list[tuple[str, str]] | None = None,
        label_pattern: str | None = None,
    ) -> Iterator[Node]:
        """Iterate over nodes, optionally filtering.

        Args:
            attr_filters: List of (key, value) tuples for attribute filtering.
            label_pattern: Glob pattern to match against node labels.

        Yields:
            Node objects matching the filters.
        """
        attr_filters = attr_filters or []

        for node_id, attrs in self._graph.nodes(data=True):
            # Extract standard fields
            label = attrs.get("label")

            # Remaining attributes (excluding label)
            custom_attrs = {k: v for k, v in attrs.items() if k != "label"}

            node = Node(
                id=str(node_id),
                label=label,
                attributes=custom_attrs,
            )

            if node.matches_filters(attr_filters, label_pattern):
                yield node

    def edges(
        self,
        attr_filters: list[tuple[str, str]] | None = None,
        source_filter: str | None = None,
        target_filter: str | None = None,
        type_filter: str | None = None,
    ) -> Iterator[Edge]:
        """Iterate over edges, optionally filtering.

        Args:
            attr_filters: List of (key, value) tuples for attribute filtering.
            source_filter: Filter by source node ID.
            target_filter: Filter by target node ID.
            type_filter: Filter by edge type.

        Yields:
            Edge objects matching the filters.
        """
        attr_filters = attr_filters or []

        for source, target, attrs in self._graph.edges(data=True):
            # Extract standard fields
            edge_id = attrs.get("id")
            weight = attrs.get("weight")
            edge_type = attrs.get("type")
            label = attrs.get("label")

            # Remaining attributes
            standard_keys = {"id", "weight", "type", "label"}
            custom_attrs = {k: v for k, v in attrs.items() if k not in standard_keys}

            edge = Edge(
                id=str(edge_id) if edge_id else None,
                source=str(source),
                target=str(target),
                weight=float(weight) if weight is not None else None,
                edge_type=edge_type,
                label=label,
                attributes=custom_attrs,
            )

            if edge.matches_filters(attr_filters, source_filter, target_filter, type_filter):
                yield edge

    def get_node(self, node_id: str) -> Node | None:
        """Get a specific node by ID."""
        if node_id not in self._graph:
            return None

        attrs = self._graph.nodes[node_id]
        label = attrs.get("label")
        custom_attrs = {k: v for k, v in attrs.items() if k != "label"}

        return Node(id=node_id, label=label, attributes=custom_attrs)

    def get_info(self) -> dict[str, Any]:
        """Get a summary of the graph."""
        return {
            "file": str(self.file_path),
            "version": self._metadata.version,
            "mode": self._metadata.mode,
            "default_edge_type": self._metadata.default_edge_type,
            "node_count": self._metadata.node_count,
            "edge_count": self._metadata.edge_count,
            "node_attributes": self.node_attribute_keys(),
            "edge_attributes": self.edge_attribute_keys(),
        }

    # =========================================================================
    # Graph Traversal Methods
    # =========================================================================

    def neighbors(
        self,
        node_id: str,
        direction: str = "all",
        depth: int = 1,
    ) -> list[Node]:
        """Get neighbors of a node.

        Args:
            node_id: The node to find neighbors for.
            direction: "in" (predecessors), "out" (successors), or "all" (both).
            depth: Number of hops to traverse (default: 1).

        Returns:
            List of neighbor nodes.

        Raises:
            GEXFParseError: If node not found.
        """
        if node_id not in self._graph:
            raise GEXFParseError(f"Node not found: {node_id}")

        visited: set[str] = set()
        current_level = {node_id}

        for _ in range(depth):
            next_level: set[str] = set()
            for nid in current_level:
                if self._graph.is_directed():
                    if direction in ("out", "all"):
                        next_level.update(self._graph.successors(nid))
                    if direction in ("in", "all"):
                        next_level.update(self._graph.predecessors(nid))
                else:
                    next_level.update(self._graph.neighbors(nid))
            visited.update(next_level)
            current_level = next_level - {node_id}

        # Convert to Node objects (excluding the original node)
        visited.discard(node_id)
        return [self.get_node(nid) for nid in sorted(visited) if self.get_node(nid)]

    def shortest_path(
        self,
        source: str,
        target: str,
        weighted: bool = False,
    ) -> PathResult | None:
        """Find the shortest path between two nodes.

        Args:
            source: Source node ID.
            target: Target node ID.
            weighted: Whether to use edge weights.

        Returns:
            PathResult or None if no path exists.
        """
        if source not in self._graph:
            raise GEXFParseError(f"Source node not found: {source}")
        if target not in self._graph:
            raise GEXFParseError(f"Target node not found: {target}")

        try:
            if weighted:
                path = nx.shortest_path(self._graph, source, target, weight="weight")
                length = nx.shortest_path_length(self._graph, source, target, weight="weight")
                return PathResult(
                    source=source,
                    target=target,
                    path=list(path),
                    length=len(path) - 1,
                    total_weight=float(length),
                )
            else:
                path = nx.shortest_path(self._graph, source, target)
                return PathResult(
                    source=source,
                    target=target,
                    path=list(path),
                    length=len(path) - 1,
                )
        except nx.NetworkXNoPath:
            return None

    def all_paths(
        self,
        source: str,
        target: str,
        max_depth: int | None = None,
    ) -> list[PathResult]:
        """Find all simple paths between two nodes.

        Args:
            source: Source node ID.
            target: Target node ID.
            max_depth: Maximum path length (None for unlimited).

        Returns:
            List of PathResult objects.
        """
        if source not in self._graph:
            raise GEXFParseError(f"Source node not found: {source}")
        if target not in self._graph:
            raise GEXFParseError(f"Target node not found: {target}")

        cutoff = max_depth if max_depth else None
        paths = []

        for path in nx.all_simple_paths(self._graph, source, target, cutoff=cutoff):
            paths.append(
                PathResult(
                    source=source,
                    target=target,
                    path=list(path),
                    length=len(path) - 1,
                )
            )

        return paths

    def has_path(self, source: str, target: str) -> bool:
        """Check if a path exists between two nodes.

        Args:
            source: Source node ID.
            target: Target node ID.

        Returns:
            True if a path exists.
        """
        if source not in self._graph or target not in self._graph:
            return False
        return nx.has_path(self._graph, source, target)

    def reachable(
        self,
        node_id: str,
        direction: str = "forward",
        max_depth: int | None = None,
    ) -> list[Node]:
        """Find all nodes reachable from a given node.

        Args:
            node_id: Starting node ID.
            direction: "forward" (descendants), "backward" (ancestors), or "both".
            max_depth: Maximum traversal depth.

        Returns:
            List of reachable nodes.
        """
        if node_id not in self._graph:
            raise GEXFParseError(f"Node not found: {node_id}")

        reachable_ids: set[str] = set()

        if self._graph.is_directed():
            if direction in ("forward", "both"):
                if max_depth:
                    # Use BFS with depth limit
                    reachable_ids.update(
                        nx.single_source_shortest_path_length(
                            self._graph, node_id, cutoff=max_depth
                        ).keys()
                    )
                else:
                    reachable_ids.update(nx.descendants(self._graph, node_id))

            if direction in ("backward", "both"):
                if max_depth:
                    reversed_graph = self._graph.reverse()
                    reachable_ids.update(
                        nx.single_source_shortest_path_length(
                            reversed_graph, node_id, cutoff=max_depth
                        ).keys()
                    )
                else:
                    reachable_ids.update(nx.ancestors(self._graph, node_id))
        else:
            # For undirected graphs, use connected component
            if max_depth:
                reachable_ids.update(
                    nx.single_source_shortest_path_length(
                        self._graph, node_id, cutoff=max_depth
                    ).keys()
                )
            else:
                reachable_ids.update(nx.node_connected_component(self._graph, node_id))

        reachable_ids.discard(node_id)
        return [self.get_node(nid) for nid in sorted(reachable_ids) if self.get_node(nid)]

    def common_neighbors(self, node1: str, node2: str) -> list[Node]:
        """Find nodes that are neighbors of both given nodes.

        For directed graphs, considers both predecessors and successors.

        Args:
            node1: First node ID.
            node2: Second node ID.

        Returns:
            List of common neighbor nodes.
        """
        if node1 not in self._graph:
            raise GEXFParseError(f"Node not found: {node1}")
        if node2 not in self._graph:
            raise GEXFParseError(f"Node not found: {node2}")

        if self._graph.is_directed():
            # For directed graphs, get both predecessors and successors
            neighbors1 = set(self._graph.predecessors(node1)) | set(self._graph.successors(node1))
            neighbors2 = set(self._graph.predecessors(node2)) | set(self._graph.successors(node2))
            common = neighbors1 & neighbors2
        else:
            common = set(nx.common_neighbors(self._graph, node1, node2))

        return [self.get_node(nid) for nid in sorted(common) if self.get_node(nid)]

    # =========================================================================
    # Graph Analysis Methods
    # =========================================================================

    def get_stats(self) -> GraphStats:
        """Get comprehensive statistics about the graph.

        Returns:
            GraphStats object with various metrics.
        """
        n = self._graph.number_of_nodes()
        m = self._graph.number_of_edges()

        is_directed = self._graph.is_directed()
        density = nx.density(self._graph)

        # Calculate average degree
        degrees = [d for _, d in self._graph.degree()]
        avg_degree = sum(degrees) / n if n > 0 else 0

        # Clustering coefficient
        try:
            avg_clustering = nx.average_clustering(self._graph)
        except Exception:
            avg_clustering = 0.0

        # Connected components
        if is_directed:
            is_connected = nx.is_weakly_connected(self._graph)
            num_components = nx.number_weakly_connected_components(self._graph)
        else:
            is_connected = nx.is_connected(self._graph) if n > 0 else True
            num_components = nx.number_connected_components(self._graph)

        # Cycle detection
        try:
            if is_directed:
                has_cycles = not nx.is_directed_acyclic_graph(self._graph)
            else:
                has_cycles = len(list(nx.cycle_basis(self._graph))) > 0
        except Exception:
            has_cycles = False

        # Diameter and path length (only if connected)
        diameter = None
        radius = None
        avg_path_length = None

        if is_connected and n > 1:
            try:
                if is_directed:
                    # For directed graphs, check strong connectivity
                    if nx.is_strongly_connected(self._graph):
                        diameter = nx.diameter(self._graph)
                        radius = nx.radius(self._graph)
                        avg_path_length = nx.average_shortest_path_length(self._graph)
                else:
                    diameter = nx.diameter(self._graph)
                    radius = nx.radius(self._graph)
                    avg_path_length = nx.average_shortest_path_length(self._graph)
            except Exception:
                pass

        return GraphStats(
            node_count=n,
            edge_count=m,
            density=density,
            is_directed=is_directed,
            is_connected=is_connected,
            num_components=num_components,
            avg_degree=avg_degree,
            avg_clustering=avg_clustering,
            has_cycles=has_cycles,
            diameter=diameter,
            radius=radius,
            avg_path_length=avg_path_length,
        )

    def get_centrality(self, centrality_type: CentralityType) -> CentralityResult:
        """Calculate centrality scores for all nodes.

        Args:
            centrality_type: Type of centrality to calculate.

        Returns:
            CentralityResult with scores for each node.
        """
        if centrality_type == CentralityType.DEGREE:
            scores = dict(nx.degree_centrality(self._graph))
        elif centrality_type == CentralityType.BETWEENNESS:
            scores = dict(nx.betweenness_centrality(self._graph))
        elif centrality_type == CentralityType.CLOSENESS:
            scores = dict(nx.closeness_centrality(self._graph))
        elif centrality_type == CentralityType.PAGERANK:
            scores = dict(nx.pagerank(self._graph))
        elif centrality_type == CentralityType.EIGENVECTOR:
            try:
                scores = dict(nx.eigenvector_centrality(self._graph, max_iter=1000))
            except nx.PowerIterationFailedConvergence:
                # Fall back to numpy-based calculation
                scores = dict(nx.eigenvector_centrality_numpy(self._graph))
        else:
            raise ValueError(f"Unknown centrality type: {centrality_type}")

        return CentralityResult(
            centrality_type=centrality_type.value,
            scores=scores,
        )

    def get_components(self, component_type: str = "connected") -> ComponentInfo:
        """Get information about connected components.

        Args:
            component_type: "connected", "strongly", or "weakly".

        Returns:
            ComponentInfo object.
        """
        if self._graph.is_directed():
            if component_type == "strongly":
                components_gen = nx.strongly_connected_components(self._graph)
            else:  # weakly or connected
                components_gen = nx.weakly_connected_components(self._graph)
        else:
            components_gen = nx.connected_components(self._graph)

        components = [sorted(c) for c in components_gen]
        components.sort(key=len, reverse=True)

        sizes = [len(c) for c in components]

        return ComponentInfo(
            num_components=len(components),
            component_sizes=sizes,
            largest_component_size=sizes[0] if sizes else 0,
            components=components,
        )

    def get_degree(self, node_id: str | None = None) -> dict[str, Any]:
        """Get degree information for nodes.

        Args:
            node_id: Specific node ID or None for all nodes.

        Returns:
            Dictionary with degree information.
        """
        if node_id:
            if node_id not in self._graph:
                raise GEXFParseError(f"Node not found: {node_id}")

            if self._graph.is_directed():
                return {
                    "node": node_id,
                    "in_degree": self._graph.in_degree(node_id),
                    "out_degree": self._graph.out_degree(node_id),
                    "total_degree": self._graph.degree(node_id),
                }
            else:
                return {
                    "node": node_id,
                    "degree": self._graph.degree(node_id),
                }
        else:
            # Return top nodes by degree
            if self._graph.is_directed():
                degrees = [
                    {
                        "node": n,
                        "in_degree": self._graph.in_degree(n),
                        "out_degree": self._graph.out_degree(n),
                        "total_degree": d,
                    }
                    for n, d in self._graph.degree()
                ]
                degrees.sort(key=lambda x: x["total_degree"], reverse=True)
            else:
                degrees = [
                    {"node": n, "degree": d}
                    for n, d in self._graph.degree()
                ]
                degrees.sort(key=lambda x: x["degree"], reverse=True)
            return {"degrees": degrees}

    # =========================================================================
    # Subgraph Methods
    # =========================================================================

    def ego_graph(self, node_id: str, radius: int = 1) -> "GEXFGraph":
        """Get the ego graph (neighborhood) around a node.

        Args:
            node_id: Center node ID.
            radius: Number of hops to include.

        Returns:
            New GEXFGraph containing the ego subgraph.

        Note:
            Returns a new GEXFGraph-like object with the subgraph.
        """
        if node_id not in self._graph:
            raise GEXFParseError(f"Node not found: {node_id}")

        ego = nx.ego_graph(self._graph, node_id, radius=radius)
        return self._create_subgraph(ego)

    def subgraph(self, node_ids: list[str]) -> "GEXFGraph":
        """Extract a subgraph containing only specified nodes.

        Args:
            node_ids: List of node IDs to include.

        Returns:
            New GEXFGraph containing the subgraph.
        """
        # Validate nodes
        missing = [n for n in node_ids if n not in self._graph]
        if missing:
            raise GEXFParseError(f"Nodes not found: {', '.join(missing)}")

        sub = self._graph.subgraph(node_ids).copy()
        return self._create_subgraph(sub)

    def _create_subgraph(self, subgraph: nx.Graph) -> "GEXFGraph":
        """Create a new GEXFGraph wrapper around a NetworkX subgraph.

        This is an internal helper that creates a minimal GEXFGraph-like object.
        """
        # Create a new instance without parsing a file
        wrapper = object.__new__(GEXFGraph)
        wrapper.file_path = self.file_path
        wrapper._graph = subgraph
        wrapper._metadata = GraphMetadata(
            creator=self._metadata.creator,
            description=f"Subgraph of {self._metadata.description or self.file_path.name}",
            mode=self._metadata.mode,
            default_edge_type=self._metadata.default_edge_type,
            version=self._metadata.version,
            node_count=subgraph.number_of_nodes(),
            edge_count=subgraph.number_of_edges(),
        )
        wrapper._node_attr_keys = set()
        wrapper._edge_attr_keys = set()
        wrapper._collect_attribute_keys()
        return wrapper

    # =========================================================================
    # Export Methods
    # =========================================================================

    def export(self, format: ExportFormat) -> str:
        """Export the graph to a different format.

        Args:
            format: Target export format.

        Returns:
            String representation of the graph in the target format.
        """
        import io
        import json

        if format == ExportFormat.JSON:
            # Export as node-link JSON
            data = nx.node_link_data(self._graph)
            return json.dumps(data, indent=2, default=str)

        elif format == ExportFormat.GRAPHML:
            # Export as GraphML
            buffer = io.BytesIO()
            nx.write_graphml(self._graph, buffer)
            return buffer.getvalue().decode("utf-8")

        elif format == ExportFormat.ADJLIST:
            # Export as adjacency list
            lines = []
            for node in self._graph.nodes():
                neighbors = list(self._graph.neighbors(node))
                if neighbors:
                    lines.append(f"{node} {' '.join(str(n) for n in neighbors)}")
                else:
                    lines.append(str(node))
            return "\n".join(lines)

        elif format == ExportFormat.EDGELIST:
            # Export as edge list
            lines = []
            for source, target, data in self._graph.edges(data=True):
                weight = data.get("weight", "")
                if weight:
                    lines.append(f"{source} {target} {weight}")
                else:
                    lines.append(f"{source} {target}")
            return "\n".join(lines)

        else:
            raise ValueError(f"Unsupported export format: {format}")

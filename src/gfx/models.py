"""Data models for GEXF graph structures."""

from dataclasses import dataclass, field
from typing import Any
from enum import Enum


class CentralityType(Enum):
    """Types of centrality metrics."""
    DEGREE = "degree"
    BETWEENNESS = "betweenness"
    CLOSENESS = "closeness"
    PAGERANK = "pagerank"
    EIGENVECTOR = "eigenvector"


class ExportFormat(Enum):
    """Supported export formats."""
    JSON = "json"
    GRAPHML = "graphml"
    ADJLIST = "adjlist"
    EDGELIST = "edgelist"


@dataclass(frozen=True)
class GraphMetadata:
    """Metadata extracted from a GEXF file."""

    creator: str | None = None
    description: str | None = None
    last_modified: str | None = None
    mode: str = "static"
    default_edge_type: str = "undirected"
    version: str | None = None
    node_count: int = 0
    edge_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata to a dictionary for JSON serialization."""
        return {
            "creator": self.creator,
            "description": self.description,
            "last_modified": self.last_modified,
            "mode": self.mode,
            "default_edge_type": self.default_edge_type,
            "version": self.version,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
        }


@dataclass(frozen=True)
class Node:
    """A node in the graph."""

    id: str
    label: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert node to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "label": self.label,
            "attributes": dict(self.attributes),
        }

    def matches_filters(
        self, attr_filters: list[tuple[str, str]], label_pattern: str | None = None
    ) -> bool:
        """Check if this node matches the given filters (AND logic)."""
        import fnmatch

        # Check label pattern
        if label_pattern and self.label:
            if not fnmatch.fnmatch(self.label, label_pattern):
                return False
        elif label_pattern and not self.label:
            return False

        # Check attribute filters
        for key, value in attr_filters:
            node_value = self.attributes.get(key)
            if node_value is None:
                return False
            # String comparison (handles type coercion)
            if str(node_value) != value:
                return False

        return True


@dataclass(frozen=True)
class Edge:
    """An edge in the graph."""

    id: str | None
    source: str
    target: str
    weight: float | None = None
    edge_type: str | None = None
    label: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert edge to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
            "type": self.edge_type,
            "label": self.label,
            "attributes": dict(self.attributes),
        }

    def matches_filters(
        self,
        attr_filters: list[tuple[str, str]],
        source_filter: str | None = None,
        target_filter: str | None = None,
        type_filter: str | None = None,
    ) -> bool:
        """Check if this edge matches the given filters (AND logic)."""
        # Check source filter
        if source_filter and self.source != source_filter:
            return False

        # Check target filter
        if target_filter and self.target != target_filter:
            return False

        # Check type filter
        if type_filter and self.edge_type != type_filter:
            return False

        # Check attribute filters
        for key, value in attr_filters:
            edge_value = self.attributes.get(key)
            if edge_value is None:
                # Also check weight as a special attribute
                if key == "weight" and self.weight is not None:
                    if str(self.weight) != value:
                        return False
                else:
                    return False
            elif str(edge_value) != value:
                return False

        return True


@dataclass
class PathResult:
    """A path between two nodes in the graph."""

    source: str
    target: str
    path: list[str]
    length: int
    total_weight: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert path result to a dictionary for JSON serialization."""
        return {
            "source": self.source,
            "target": self.target,
            "path": self.path,
            "length": self.length,
            "total_weight": self.total_weight,
        }


@dataclass
class GraphStats:
    """Statistical summary of a graph."""

    node_count: int
    edge_count: int
    density: float
    is_directed: bool
    is_connected: bool
    num_components: int
    avg_degree: float
    avg_clustering: float
    has_cycles: bool
    diameter: int | None = None
    radius: int | None = None
    avg_path_length: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert stats to a dictionary for JSON serialization."""
        return {
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "density": round(self.density, 4),
            "is_directed": self.is_directed,
            "is_connected": self.is_connected,
            "num_components": self.num_components,
            "avg_degree": round(self.avg_degree, 2),
            "avg_clustering": round(self.avg_clustering, 4),
            "has_cycles": self.has_cycles,
            "diameter": self.diameter,
            "radius": self.radius,
            "avg_path_length": round(self.avg_path_length, 4) if self.avg_path_length else None,
        }


@dataclass
class CentralityResult:
    """Centrality scores for nodes."""

    centrality_type: str
    scores: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        """Convert centrality result to a dictionary for JSON serialization."""
        return {
            "type": self.centrality_type,
            "scores": {k: round(v, 6) for k, v in self.scores.items()},
        }

    def top_n(self, n: int = 10) -> list[tuple[str, float]]:
        """Get the top N nodes by centrality score."""
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:n]


@dataclass
class ComponentInfo:
    """Information about connected components in the graph."""

    num_components: int
    component_sizes: list[int]
    largest_component_size: int
    components: list[list[str]]

    def to_dict(self) -> dict[str, Any]:
        """Convert component info to a dictionary for JSON serialization."""
        return {
            "num_components": self.num_components,
            "component_sizes": self.component_sizes,
            "largest_component_size": self.largest_component_size,
            "components": self.components,
        }

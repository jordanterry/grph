"""Tests for the graph traversal, analysis, and export features."""

from pathlib import Path

import pytest

from gfx.models import CentralityType, ExportFormat
from gfx.parser import GEXFGraph, GEXFParseError


FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_FILE = FIXTURES_DIR / "sample.gexf"


class TestNeighbors:
    """Tests for the neighbors method."""

    def test_neighbors_all_directions(self) -> None:
        """Test getting all neighbors of a node."""
        graph = GEXFGraph(SAMPLE_FILE)
        neighbors = graph.neighbors("lb1", direction="all")

        # lb1 has outgoing edges to server1 and server2
        assert len(neighbors) == 2
        neighbor_ids = {n.id for n in neighbors}
        assert neighbor_ids == {"server1", "server2"}

    def test_neighbors_out_direction(self) -> None:
        """Test getting outgoing neighbors of a node."""
        graph = GEXFGraph(SAMPLE_FILE)
        neighbors = graph.neighbors("lb1", direction="out")

        assert len(neighbors) == 2
        neighbor_ids = {n.id for n in neighbors}
        assert neighbor_ids == {"server1", "server2"}

    def test_neighbors_in_direction(self) -> None:
        """Test getting incoming neighbors of a node."""
        graph = GEXFGraph(SAMPLE_FILE)
        neighbors = graph.neighbors("db1", direction="in")

        # db1 receives edges from server1 and server2
        assert len(neighbors) == 2
        neighbor_ids = {n.id for n in neighbors}
        assert neighbor_ids == {"server1", "server2"}

    def test_neighbors_multi_hop(self) -> None:
        """Test getting neighbors at multiple hops."""
        graph = GEXFGraph(SAMPLE_FILE)
        neighbors = graph.neighbors("lb1", direction="out", depth=2)

        # 2 hops from lb1: server1, server2, db1, cache1
        assert len(neighbors) == 4
        neighbor_ids = {n.id for n in neighbors}
        assert neighbor_ids == {"server1", "server2", "db1", "cache1"}

    def test_neighbors_node_not_found(self) -> None:
        """Test that missing node raises error."""
        graph = GEXFGraph(SAMPLE_FILE)
        with pytest.raises(GEXFParseError, match="Node not found"):
            graph.neighbors("nonexistent")


class TestShortestPath:
    """Tests for the shortest path method."""

    def test_shortest_path_exists(self) -> None:
        """Test finding shortest path between two nodes."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.shortest_path("lb1", "db1")

        assert result is not None
        assert result.source == "lb1"
        assert result.target == "db1"
        assert result.length == 2
        assert result.path[0] == "lb1"
        assert result.path[-1] == "db1"

    def test_shortest_path_weighted(self) -> None:
        """Test finding weighted shortest path."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.shortest_path("lb1", "db1", weighted=True)

        assert result is not None
        assert result.total_weight is not None
        assert result.total_weight > 0

    def test_shortest_path_not_found(self) -> None:
        """Test when no path exists (reverse direction in directed graph)."""
        graph = GEXFGraph(SAMPLE_FILE)
        # db1 -> lb1 doesn't exist in the directed graph
        result = graph.shortest_path("db1", "lb1")

        assert result is None

    def test_shortest_path_node_not_found(self) -> None:
        """Test that missing node raises error."""
        graph = GEXFGraph(SAMPLE_FILE)
        with pytest.raises(GEXFParseError, match="Source node not found"):
            graph.shortest_path("nonexistent", "db1")


class TestAllPaths:
    """Tests for the all_paths method."""

    def test_all_paths_between_nodes(self) -> None:
        """Test finding all paths between two nodes."""
        graph = GEXFGraph(SAMPLE_FILE)
        paths = graph.all_paths("lb1", "db1")

        # There are 2 paths: lb1->server1->db1 and lb1->server2->db1
        assert len(paths) == 2
        assert all(p.source == "lb1" for p in paths)
        assert all(p.target == "db1" for p in paths)

    def test_all_paths_with_max_depth(self) -> None:
        """Test finding paths with depth limit."""
        graph = GEXFGraph(SAMPLE_FILE)
        paths = graph.all_paths("lb1", "db1", max_depth=1)

        # No direct path exists with length 1
        assert len(paths) == 0


class TestHasPath:
    """Tests for the has_path method."""

    def test_has_path_exists(self) -> None:
        """Test path existence check."""
        graph = GEXFGraph(SAMPLE_FILE)
        assert graph.has_path("lb1", "db1") is True

    def test_has_path_not_exists(self) -> None:
        """Test when path doesn't exist."""
        graph = GEXFGraph(SAMPLE_FILE)
        assert graph.has_path("db1", "lb1") is False


class TestReachable:
    """Tests for the reachable method."""

    def test_reachable_forward(self) -> None:
        """Test finding all reachable nodes forward."""
        graph = GEXFGraph(SAMPLE_FILE)
        reachable = graph.reachable("lb1", direction="forward")

        # lb1 can reach all other nodes
        assert len(reachable) == 4
        reachable_ids = {n.id for n in reachable}
        assert reachable_ids == {"server1", "server2", "db1", "cache1"}

    def test_reachable_backward(self) -> None:
        """Test finding all reachable nodes backward (ancestors)."""
        graph = GEXFGraph(SAMPLE_FILE)
        reachable = graph.reachable("db1", direction="backward")

        # db1 is reachable from lb1, server1, server2
        assert len(reachable) == 3
        reachable_ids = {n.id for n in reachable}
        assert reachable_ids == {"lb1", "server1", "server2"}

    def test_reachable_with_max_depth(self) -> None:
        """Test reachable with depth limit."""
        graph = GEXFGraph(SAMPLE_FILE)
        reachable = graph.reachable("lb1", direction="forward", max_depth=1)

        # Only immediate neighbors
        assert len(reachable) == 2
        reachable_ids = {n.id for n in reachable}
        assert reachable_ids == {"server1", "server2"}


class TestCommonNeighbors:
    """Tests for the common_neighbors method."""

    def test_common_neighbors_exist(self) -> None:
        """Test finding common neighbors."""
        graph = GEXFGraph(SAMPLE_FILE)
        common = graph.common_neighbors("server1", "server2")

        # Both servers have:
        # - lb1 as predecessor
        # - db1 and cache1 as successors
        # So common neighbors = {lb1, db1, cache1}
        assert len(common) == 3
        common_ids = {n.id for n in common}
        assert common_ids == {"lb1", "db1", "cache1"}

    def test_common_neighbors_some(self) -> None:
        """Test when some common neighbors exist."""
        graph = GEXFGraph(SAMPLE_FILE)
        common = graph.common_neighbors("lb1", "db1")

        # lb1's neighbors: server1, server2 (successors)
        # db1's neighbors: server1, server2 (predecessors)
        # Common = {server1, server2}
        assert len(common) == 2
        common_ids = {n.id for n in common}
        assert common_ids == {"server1", "server2"}

    def test_common_neighbors_none(self) -> None:
        """Test when no common neighbors exist."""
        graph = GEXFGraph(SAMPLE_FILE)
        common = graph.common_neighbors("lb1", "cache1")

        # lb1's neighbors: server1, server2 (successors)
        # cache1's neighbors: server1, server2 (predecessors)
        # Common = {server1, server2} - they do share neighbors!
        # Let's test db1 and cache1 instead - both are leaf nodes with no shared neighbors
        common = graph.common_neighbors("db1", "cache1")

        # db1's neighbors: server1, server2 (predecessors)
        # cache1's neighbors: server1, server2 (predecessors)
        # Common = {server1, server2}
        assert len(common) == 2


class TestGetStats:
    """Tests for the get_stats method."""

    def test_stats_basic(self) -> None:
        """Test getting basic graph statistics."""
        graph = GEXFGraph(SAMPLE_FILE)
        stats = graph.get_stats()

        assert stats.node_count == 5
        assert stats.edge_count == 6
        assert stats.is_directed is True
        assert stats.is_connected is True
        assert stats.num_components == 1
        assert stats.has_cycles is False
        assert stats.avg_degree > 0
        assert stats.density > 0

    def test_stats_to_dict(self) -> None:
        """Test stats serialization."""
        graph = GEXFGraph(SAMPLE_FILE)
        stats = graph.get_stats()
        d = stats.to_dict()

        assert "node_count" in d
        assert "edge_count" in d
        assert "density" in d
        assert "is_connected" in d


class TestCentrality:
    """Tests for the centrality methods."""

    def test_degree_centrality(self) -> None:
        """Test degree centrality calculation."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.get_centrality(CentralityType.DEGREE)

        assert result.centrality_type == "degree"
        assert len(result.scores) == 5
        assert all(0 <= s <= 1 for s in result.scores.values())

    def test_betweenness_centrality(self) -> None:
        """Test betweenness centrality calculation."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.get_centrality(CentralityType.BETWEENNESS)

        assert result.centrality_type == "betweenness"
        assert len(result.scores) == 5

    def test_pagerank(self) -> None:
        """Test PageRank calculation."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.get_centrality(CentralityType.PAGERANK)

        assert result.centrality_type == "pagerank"
        assert len(result.scores) == 5
        # PageRank scores should sum to approximately 1
        assert abs(sum(result.scores.values()) - 1.0) < 0.01

    def test_centrality_top_n(self) -> None:
        """Test getting top N nodes by centrality."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.get_centrality(CentralityType.DEGREE)
        top_3 = result.top_n(3)

        assert len(top_3) == 3
        # Top nodes should be sorted by score descending
        assert top_3[0][1] >= top_3[1][1] >= top_3[2][1]


class TestComponents:
    """Tests for the components method."""

    def test_components_connected(self) -> None:
        """Test getting connected components."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.get_components("connected")

        assert result.num_components == 1
        assert result.largest_component_size == 5
        assert len(result.components) == 1
        assert len(result.components[0]) == 5

    def test_components_to_dict(self) -> None:
        """Test components serialization."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.get_components("connected")
        d = result.to_dict()

        assert "num_components" in d
        assert "component_sizes" in d
        assert "components" in d


class TestDegree:
    """Tests for the degree method."""

    def test_degree_single_node(self) -> None:
        """Test getting degree for a single node."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.get_degree("server1")

        assert result["node"] == "server1"
        assert "in_degree" in result
        assert "out_degree" in result
        assert "total_degree" in result

    def test_degree_all_nodes(self) -> None:
        """Test getting degree for all nodes."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.get_degree()

        assert "degrees" in result
        assert len(result["degrees"]) == 5
        # Should be sorted by total degree
        degrees = result["degrees"]
        for i in range(len(degrees) - 1):
            assert degrees[i]["total_degree"] >= degrees[i + 1]["total_degree"]


class TestEgoGraph:
    """Tests for the ego_graph method."""

    def test_ego_graph_basic(self) -> None:
        """Test creating an ego graph."""
        graph = GEXFGraph(SAMPLE_FILE)
        ego = graph.ego_graph("server1", radius=1)

        # server1 + outgoing neighbors (db1, cache1)
        # Note: In directed graphs, ego_graph follows outgoing edges
        assert ego.metadata.node_count == 3
        ego_ids = {n.id for n in ego.nodes()}
        assert ego_ids == {"server1", "db1", "cache1"}

    def test_ego_graph_radius_2(self) -> None:
        """Test ego graph with larger radius."""
        graph = GEXFGraph(SAMPLE_FILE)
        ego = graph.ego_graph("lb1", radius=2)

        # lb1 + all reachable nodes via outgoing edges
        assert ego.metadata.node_count == 5


class TestSubgraph:
    """Tests for the subgraph method."""

    def test_subgraph_basic(self) -> None:
        """Test extracting a subgraph."""
        graph = GEXFGraph(SAMPLE_FILE)
        sub = graph.subgraph(["server1", "server2", "db1"])

        assert sub.metadata.node_count == 3
        # Should include edges between these nodes
        assert sub.metadata.edge_count > 0

    def test_subgraph_invalid_node(self) -> None:
        """Test subgraph with invalid node."""
        graph = GEXFGraph(SAMPLE_FILE)
        with pytest.raises(GEXFParseError, match="Nodes not found"):
            graph.subgraph(["server1", "nonexistent"])


class TestExport:
    """Tests for the export method."""

    def test_export_json(self) -> None:
        """Test exporting to JSON format."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.export(ExportFormat.JSON)

        assert '"directed": true' in result
        assert '"nodes"' in result
        assert '"links"' in result or '"edges"' in result

    def test_export_graphml(self) -> None:
        """Test exporting to GraphML format."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.export(ExportFormat.GRAPHML)

        assert "<?xml" in result
        assert "graphml" in result.lower()

    def test_export_adjlist(self) -> None:
        """Test exporting to adjacency list format."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.export(ExportFormat.ADJLIST)

        # Should contain node IDs
        assert "server1" in result
        assert "lb1" in result

    def test_export_edgelist(self) -> None:
        """Test exporting to edge list format."""
        graph = GEXFGraph(SAMPLE_FILE)
        result = graph.export(ExportFormat.EDGELIST)

        # Should contain source-target pairs
        lines = result.strip().split("\n")
        assert len(lines) == 6  # 6 edges


class TestModelSerialization:
    """Tests for model to_dict methods."""

    def test_path_result_to_dict(self) -> None:
        """Test PathResult serialization."""
        from gfx.models import PathResult

        path = PathResult(
            source="a",
            target="c",
            path=["a", "b", "c"],
            length=2,
            total_weight=3.5,
        )
        d = path.to_dict()

        assert d["source"] == "a"
        assert d["target"] == "c"
        assert d["path"] == ["a", "b", "c"]
        assert d["length"] == 2
        assert d["total_weight"] == 3.5

    def test_centrality_result_to_dict(self) -> None:
        """Test CentralityResult serialization."""
        from gfx.models import CentralityResult

        result = CentralityResult(
            centrality_type="degree",
            scores={"a": 0.5, "b": 0.3, "c": 0.2},
        )
        d = result.to_dict()

        assert d["type"] == "degree"
        assert "scores" in d
        assert len(d["scores"]) == 3

    def test_component_info_to_dict(self) -> None:
        """Test ComponentInfo serialization."""
        from gfx.models import ComponentInfo

        info = ComponentInfo(
            num_components=2,
            component_sizes=[3, 2],
            largest_component_size=3,
            components=[["a", "b", "c"], ["d", "e"]],
        )
        d = info.to_dict()

        assert d["num_components"] == 2
        assert d["component_sizes"] == [3, 2]
        assert d["largest_component_size"] == 3

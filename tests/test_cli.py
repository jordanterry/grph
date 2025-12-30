"""Integration tests for the CLI commands."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from gfx.cli import main


FIXTURES_DIR = Path(__file__).parent / "fixtures"
SAMPLE_FILE = str(FIXTURES_DIR / "sample.gexf")


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


class TestBasicCommands:
    """Tests for basic CLI commands."""

    def test_help(self, runner: CliRunner) -> None:
        """Test help command."""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "GFX" in result.output

    def test_version(self, runner: CliRunner) -> None:
        """Test version command."""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0

    def test_meta(self, runner: CliRunner) -> None:
        """Test meta command."""
        result = runner.invoke(main, ["meta", SAMPLE_FILE])
        assert result.exit_code == 0
        assert "GFX Test Suite" in result.output

    def test_meta_json(self, runner: CliRunner) -> None:
        """Test meta command with JSON output."""
        result = runner.invoke(main, ["meta", SAMPLE_FILE, "--json"])
        assert result.exit_code == 0
        assert '"creator"' in result.output

    def test_info(self, runner: CliRunner) -> None:
        """Test info command."""
        result = runner.invoke(main, ["info", SAMPLE_FILE])
        assert result.exit_code == 0
        assert "5" in result.output  # node count

    def test_nodes(self, runner: CliRunner) -> None:
        """Test nodes command."""
        result = runner.invoke(main, ["nodes", SAMPLE_FILE])
        assert result.exit_code == 0
        assert "server1" in result.output

    def test_nodes_filter(self, runner: CliRunner) -> None:
        """Test nodes command with filter."""
        result = runner.invoke(main, ["nodes", SAMPLE_FILE, "--attr", "type=server"])
        assert result.exit_code == 0
        assert "server1" in result.output
        assert "server2" in result.output
        assert "db1" not in result.output

    def test_edges(self, runner: CliRunner) -> None:
        """Test edges command."""
        result = runner.invoke(main, ["edges", SAMPLE_FILE])
        assert result.exit_code == 0
        assert "lb1" in result.output


class TestNeighborsCommand:
    """Tests for the neighbors command."""

    def test_neighbors_basic(self, runner: CliRunner) -> None:
        """Test basic neighbors command."""
        result = runner.invoke(main, ["neighbors", SAMPLE_FILE, "lb1"])
        assert result.exit_code == 0
        assert "server1" in result.output
        assert "server2" in result.output

    def test_neighbors_direction(self, runner: CliRunner) -> None:
        """Test neighbors with direction."""
        result = runner.invoke(main, ["neighbors", SAMPLE_FILE, "db1", "--direction", "in"])
        assert result.exit_code == 0
        assert "server1" in result.output

    def test_neighbors_depth(self, runner: CliRunner) -> None:
        """Test neighbors with depth."""
        result = runner.invoke(main, ["neighbors", SAMPLE_FILE, "lb1", "--depth", "2"])
        assert result.exit_code == 0
        assert "db1" in result.output

    def test_neighbors_json(self, runner: CliRunner) -> None:
        """Test neighbors with JSON output."""
        result = runner.invoke(main, ["neighbors", SAMPLE_FILE, "lb1", "--json"])
        assert result.exit_code == 0
        assert '"id"' in result.output

    def test_neighbors_not_found(self, runner: CliRunner) -> None:
        """Test neighbors with invalid node."""
        result = runner.invoke(main, ["neighbors", SAMPLE_FILE, "nonexistent"])
        assert result.exit_code == 1
        assert "Error" in result.output


class TestPathCommand:
    """Tests for the path command."""

    def test_path_basic(self, runner: CliRunner) -> None:
        """Test basic path command."""
        result = runner.invoke(main, ["path", SAMPLE_FILE, "lb1", "db1"])
        assert result.exit_code == 0
        assert "lb1" in result.output
        assert "db1" in result.output

    def test_path_weighted(self, runner: CliRunner) -> None:
        """Test weighted path."""
        result = runner.invoke(main, ["path", SAMPLE_FILE, "lb1", "db1", "--weighted"])
        assert result.exit_code == 0
        assert "Weight" in result.output

    def test_path_not_found(self, runner: CliRunner) -> None:
        """Test when no path exists."""
        result = runner.invoke(main, ["path", SAMPLE_FILE, "db1", "lb1"])
        assert result.exit_code == 0
        assert "No path found" in result.output

    def test_path_json(self, runner: CliRunner) -> None:
        """Test path with JSON output."""
        result = runner.invoke(main, ["path", SAMPLE_FILE, "lb1", "db1", "--json"])
        assert result.exit_code == 0
        assert '"path"' in result.output


class TestAllPathsCommand:
    """Tests for the all-paths command."""

    def test_all_paths_basic(self, runner: CliRunner) -> None:
        """Test basic all-paths command."""
        result = runner.invoke(main, ["all-paths", SAMPLE_FILE, "lb1", "db1"])
        assert result.exit_code == 0
        assert "2 path" in result.output.lower()

    def test_all_paths_max_depth(self, runner: CliRunner) -> None:
        """Test all-paths with max depth."""
        result = runner.invoke(main, ["all-paths", SAMPLE_FILE, "lb1", "db1", "--max-depth", "1"])
        assert result.exit_code == 0
        assert "No paths found" in result.output


class TestHasPathCommand:
    """Tests for the has-path command."""

    def test_has_path_exists(self, runner: CliRunner) -> None:
        """Test when path exists."""
        result = runner.invoke(main, ["has-path", SAMPLE_FILE, "lb1", "db1"])
        assert result.exit_code == 0
        assert "Yes" in result.output

    def test_has_path_not_exists(self, runner: CliRunner) -> None:
        """Test when path doesn't exist."""
        result = runner.invoke(main, ["has-path", SAMPLE_FILE, "db1", "lb1"])
        assert result.exit_code == 0
        assert "No" in result.output


class TestReachableCommand:
    """Tests for the reachable command."""

    def test_reachable_basic(self, runner: CliRunner) -> None:
        """Test basic reachable command."""
        result = runner.invoke(main, ["reachable", SAMPLE_FILE, "lb1"])
        assert result.exit_code == 0
        assert "server1" in result.output

    def test_reachable_backward(self, runner: CliRunner) -> None:
        """Test reachable with backward direction."""
        result = runner.invoke(main, ["reachable", SAMPLE_FILE, "db1", "--direction", "backward"])
        assert result.exit_code == 0
        assert "lb1" in result.output


class TestCommonNeighborsCommand:
    """Tests for the common-neighbors command."""

    def test_common_neighbors_basic(self, runner: CliRunner) -> None:
        """Test basic common-neighbors command."""
        result = runner.invoke(main, ["common-neighbors", SAMPLE_FILE, "server1", "server2"])
        assert result.exit_code == 0
        assert "db1" in result.output
        assert "cache1" in result.output


class TestStatsCommand:
    """Tests for the stats command."""

    def test_stats_basic(self, runner: CliRunner) -> None:
        """Test basic stats command."""
        result = runner.invoke(main, ["stats", SAMPLE_FILE])
        assert result.exit_code == 0
        assert "Node Count" in result.output
        assert "5" in result.output
        assert "Density" in result.output

    def test_stats_json(self, runner: CliRunner) -> None:
        """Test stats with JSON output."""
        result = runner.invoke(main, ["stats", SAMPLE_FILE, "--json"])
        assert result.exit_code == 0
        assert '"node_count"' in result.output


class TestCentralityCommand:
    """Tests for the centrality command."""

    def test_centrality_default(self, runner: CliRunner) -> None:
        """Test default centrality (degree)."""
        result = runner.invoke(main, ["centrality", SAMPLE_FILE])
        assert result.exit_code == 0
        assert "Degree" in result.output

    def test_centrality_pagerank(self, runner: CliRunner) -> None:
        """Test PageRank centrality."""
        result = runner.invoke(main, ["centrality", SAMPLE_FILE, "--type", "pagerank"])
        assert result.exit_code == 0
        assert "Pagerank" in result.output

    def test_centrality_top_n(self, runner: CliRunner) -> None:
        """Test centrality with custom top N."""
        result = runner.invoke(main, ["centrality", SAMPLE_FILE, "--top", "3"])
        assert result.exit_code == 0
        assert "Top 3" in result.output


class TestComponentsCommand:
    """Tests for the components command."""

    def test_components_basic(self, runner: CliRunner) -> None:
        """Test basic components command."""
        result = runner.invoke(main, ["components", SAMPLE_FILE])
        assert result.exit_code == 0
        assert "Components" in result.output

    def test_components_list(self, runner: CliRunner) -> None:
        """Test components with list."""
        result = runner.invoke(main, ["components", SAMPLE_FILE, "--list"])
        assert result.exit_code == 0
        assert "Members" in result.output


class TestDegreeCommand:
    """Tests for the degree command."""

    def test_degree_all(self, runner: CliRunner) -> None:
        """Test degree for all nodes."""
        result = runner.invoke(main, ["degree", SAMPLE_FILE])
        assert result.exit_code == 0
        assert "Degrees" in result.output

    def test_degree_single_node(self, runner: CliRunner) -> None:
        """Test degree for single node."""
        result = runner.invoke(main, ["degree", SAMPLE_FILE, "--node", "server1"])
        assert result.exit_code == 0
        assert "server1" in result.output


class TestEgoCommand:
    """Tests for the ego command."""

    def test_ego_basic(self, runner: CliRunner) -> None:
        """Test basic ego command."""
        result = runner.invoke(main, ["ego", SAMPLE_FILE, "server1"])
        assert result.exit_code == 0
        assert "Ego graph" in result.output

    def test_ego_radius(self, runner: CliRunner) -> None:
        """Test ego with radius."""
        result = runner.invoke(main, ["ego", SAMPLE_FILE, "lb1", "--radius", "2"])
        assert result.exit_code == 0

    def test_ego_output(self, runner: CliRunner) -> None:
        """Test ego with file output."""
        with runner.isolated_filesystem():
            result = runner.invoke(main, ["ego", SAMPLE_FILE, "server1", "--output", "ego.gexf"])
            assert result.exit_code == 0
            assert Path("ego.gexf").exists()


class TestSubgraphCommand:
    """Tests for the subgraph command."""

    def test_subgraph_basic(self, runner: CliRunner) -> None:
        """Test basic subgraph command."""
        result = runner.invoke(main, ["subgraph", SAMPLE_FILE, "--nodes", "server1,server2,db1"])
        assert result.exit_code == 0
        assert "Subgraph" in result.output

    def test_subgraph_output(self, runner: CliRunner) -> None:
        """Test subgraph with file output."""
        with runner.isolated_filesystem():
            result = runner.invoke(
                main,
                ["subgraph", SAMPLE_FILE, "--nodes", "server1,db1", "--output", "sub.gexf"],
            )
            assert result.exit_code == 0
            assert Path("sub.gexf").exists()


class TestExportCommand:
    """Tests for the export command."""

    def test_export_json(self, runner: CliRunner) -> None:
        """Test export to JSON."""
        result = runner.invoke(main, ["export", SAMPLE_FILE, "--format", "json"])
        assert result.exit_code == 0
        assert '"directed"' in result.output

    def test_export_graphml(self, runner: CliRunner) -> None:
        """Test export to GraphML."""
        result = runner.invoke(main, ["export", SAMPLE_FILE, "--format", "graphml"])
        assert result.exit_code == 0
        assert "graphml" in result.output.lower()

    def test_export_edgelist(self, runner: CliRunner) -> None:
        """Test export to edge list."""
        result = runner.invoke(main, ["export", SAMPLE_FILE, "--format", "edgelist"])
        assert result.exit_code == 0
        assert "lb1" in result.output

    def test_export_to_file(self, runner: CliRunner) -> None:
        """Test export to file."""
        with runner.isolated_filesystem():
            result = runner.invoke(
                main,
                ["export", SAMPLE_FILE, "--format", "json", "--output", "graph.json"],
            )
            assert result.exit_code == 0
            assert Path("graph.json").exists()

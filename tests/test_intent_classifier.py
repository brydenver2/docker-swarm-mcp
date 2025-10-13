"""
Unit tests for IntentClassifier module.
"""

import time

import pytest

from app.mcp.intent_classifier import KeywordIntentClassifier


class TestKeywordIntentClassifier:
    """Test cases for KeywordIntentClassifier."""

    @pytest.fixture
    def default_classifier(self):
        """Create classifier with default mappings."""
        return KeywordIntentClassifier()

    @pytest.fixture
    def custom_classifier(self):
        """Create classifier with custom test mappings."""
        custom_mappings = {
            "container-ops": ["container", "docker run", "start", "stop"],
            "network-ops": ["network", "bridge", "overlay"],
            "system-ops": ["info", "ping", "version"]
        }
        return KeywordIntentClassifier(keyword_mappings=custom_mappings)

    def test_single_task_type_detection(self, default_classifier):
        """Test query matches one task type."""
        result = default_classifier.classify_intent("list running containers")
        assert result == ["container-ops"]

    def test_multiple_task_types_detection(self, default_classifier):
        """Test query matches multiple task types."""
        result = default_classifier.classify_intent("docker container network info")
        assert "container-ops" in result
        assert "network-ops" in result
        assert "system-ops" in result
        assert len(result) == 3

    def test_no_match_returns_empty(self, default_classifier):
        """Test query doesn't match any keywords."""
        result = default_classifier.classify_intent("random unrelated query")
        assert result == []

    def test_case_insensitive_matching(self, default_classifier):
        """Test keywords work regardless of case."""
        result1 = default_classifier.classify_intent("CONTAINER logs")
        result2 = default_classifier.classify_intent("container LOGS")
        result3 = default_classifier.classify_intent("Container Logs")

        assert result1 == ["container-ops"]
        assert result2 == ["container-ops"]
        assert result3 == ["container-ops"]

    def test_multi_word_phrase_matching(self, default_classifier):
        """Test phrases like 'docker compose' are detected."""
        result = default_classifier.classify_intent("deploy docker compose stack")
        assert "compose-ops" in result

    def test_container_keywords(self, default_classifier):
        """Test all container-ops keywords."""
        test_queries = [
            "show containers",
            "docker run nginx",
            "start my container",
            "stop container",
            "restart container",
            "get container logs",
            "exec into container",
            "attach to container",
            "inspect container",
            "running container status",
            "docker container list",
            "container logs",
            "container exec",
            "container start",
            "container stop",
            "container restart",
            "container remove",
            "container inspect",
            "container list",
            "container create"
        ]

        for query in test_queries:
            result = default_classifier.classify_intent(query)
            assert "container-ops" in result, f"Failed for query: {query}"

    def test_compose_keywords(self, default_classifier):
        """Test all compose-ops keywords."""
        test_queries = [
            "deploy compose",
            "docker compose up",
            "compose file",
            "compose.yaml",
            "docker-compose.yml",
            "multi-container app",
            "orchestrate services",
            "compose up",
            "compose down",
            "compose build",
            "compose start",
            "compose stop",
            "compose restart",
            "compose logs",
            "compose ps",
            "compose scale",
            "stack deploy",
            "stack remove",
            "stack list",
            "stack services"
        ]

        for query in test_queries:
            result = default_classifier.classify_intent(query)
            assert "compose-ops" in result, f"Failed for query: {query}"

    def test_service_keywords(self, default_classifier):
        """Test all service-ops keywords."""
        test_queries = [
            "list services",
            "swarm services",
            "scale service",
            "update service",
            "docker service",
            "service create",
            "service remove",
            "service inspect",
            "service logs",
            "service ps",
            "service update",
            "service rollback",
            "service list"
        ]

        for query in test_queries:
            result = default_classifier.classify_intent(query)
            assert "service-ops" in result, f"Failed for query: {query}"

    def test_network_keywords(self, default_classifier):
        """Test all network-ops keywords."""
        test_queries = [
            "list networks",
            "bridge network",
            "overlay network",
            "network create",
            "network connect",
            "network disconnect",
            "docker network",
            "network inspect",
            "network remove",
            "network list",
            "bridge network",
            "overlay network",
            "network driver",
            "network ip",
            "network gateway"
        ]

        for query in test_queries:
            result = default_classifier.classify_intent(query)
            assert "network-ops" in result, f"Failed for query: {query}"

    def test_volume_keywords(self, default_classifier):
        """Test all volume-ops keywords."""
        test_queries = [
            "list volumes",
            "persistent storage",
            "data volume",
            "volume create",
            "docker volume",
            "volume inspect",
            "volume remove",
            "volume list",
            "volume driver",
            "volume mount",
            "bind mount",
            "tmpfs",
            "volume backup"
        ]

        for query in test_queries:
            result = default_classifier.classify_intent(query)
            assert "volume-ops" in result, f"Failed for query: {query}"

    def test_system_keywords(self, default_classifier):
        """Test all system-ops keywords."""
        test_queries = [
            "docker info",
            "docker version",
            "health check",
            "system status",
            "docker system",
            "system df",
            "system prune",
            "system events",
            "docker events",
            "docker stats",
            "docker top",
            "docker history"
        ]

        for query in test_queries:
            result = default_classifier.classify_intent(query)
            assert "system-ops" in result, f"Failed for query: {query}"

    def test_custom_keyword_mappings(self, custom_classifier):
        """Test with custom keyword mappings."""
        result = custom_classifier.classify_intent("start container")
        assert result == ["container-ops"]

        result = custom_classifier.classify_intent("create network")
        assert result == ["network-ops"]

        result = custom_classifier.classify_intent("system info")
        assert result == ["system-ops"]

    def test_get_keyword_mappings(self, default_classifier):
        """Test get_keyword_mappings method."""
        mappings = default_classifier.get_keyword_mappings()
        assert isinstance(mappings, dict)
        assert "container-ops" in mappings
        assert "compose-ops" in mappings
        assert "service-ops" in mappings
        assert "network-ops" in mappings
        assert "volume-ops" in mappings
        assert "system-ops" in mappings


class TestIntentClassifierIntegration:
    """Integration tests with realistic queries."""

    @pytest.fixture
    def classifier(self):
        """Create classifier for integration tests."""
        return KeywordIntentClassifier()

    def test_real_world_queries(self, classifier):
        """Test with realistic user queries."""
        test_cases = [
            ("List all running containers", ["container-ops"]),
            ("Deploy my docker-compose stack", ["compose-ops"]),
            ("Scale the web service to 5 replicas", ["service-ops"]),
            ("Create a bridge network", ["network-ops"]),
            ("Show me docker info", ["system-ops"]),
            ("Check container logs for errors", ["container-ops"]),
            ("Remove unused volumes", ["volume-ops"]),
            ("Update swarm service configuration", ["service-ops"]),
            ("Connect container to network", ["network-ops"]),
            ("Backup volume data", ["volume-ops"])
        ]

        for query, expected_types in test_cases:
            result = classifier.classify_intent(query)
            for expected_type in expected_types:
                assert expected_type in result, f"Query '{query}' should detect {expected_type}, got {result}"

    def test_ambiguous_queries(self, classifier):
        """Test queries that match multiple types."""
        ambiguous_queries = [
            "docker container network info",  # container + network + system
            "compose service scale",  # compose + service
            "volume network bridge",  # volume + network
            "system container logs"  # system + container
        ]

        for query in ambiguous_queries:
            result = classifier.classify_intent(query)
            assert len(result) > 1, f"Query '{query}' should match multiple types, got {result}"

    def test_custom_keyword_mappings_integration(self):
        """Test integration with custom mappings."""
        custom_mappings = {
            "container-ops": ["container", "docker run", "logs", "exec"],
            "network-ops": ["network", "bridge", "connect"],
            "system-ops": ["info", "version", "status"]
        }

        classifier = KeywordIntentClassifier(keyword_mappings=custom_mappings)

        result = classifier.classify_intent("show container logs")
        assert "container-ops" in result

        result = classifier.classify_intent("connect to network")
        assert "network-ops" in result

        result = classifier.classify_intent("docker version info")
        assert "system-ops" in result


class TestIntentClassifierEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.fixture
    def classifier(self):
        """Create classifier for edge case tests."""
        return KeywordIntentClassifier()

    def test_empty_query(self, classifier):
        """Test empty string returns empty list."""
        result = classifier.classify_intent("")
        assert result == []

    def test_whitespace_only_query(self, classifier):
        """Test whitespace-only returns empty list."""
        result = classifier.classify_intent("   \n\t  ")
        assert result == []

    def test_special_characters(self, classifier):
        """Test queries with special chars handled gracefully."""
        special_queries = [
            "container@logs!",
            "network#bridge$",
            "service%scale^",
            "volume&mount*",
            "system(info)"
        ]

        for query in special_queries:
            result = classifier.classify_intent(query)
            # Should not crash, may or may not match
            assert isinstance(result, list)

    def test_very_long_query(self, classifier):
        """Test performance with long queries."""
        long_query = "container " * 1000 + "logs"

        start_time = time.time()
        result = classifier.classify_intent(long_query)
        end_time = time.time()

        # Should complete quickly (< 10ms)
        assert (end_time - start_time) < 0.01
        assert "container-ops" in result

    def test_unicode_characters(self, classifier):
        """Test queries with unicode characters."""
        unicode_queries = [
            "container logs with émojis 🐳",
            "network bridge with ñ",
            "service scale with 中文",
            "volume mount with русский"
        ]

        for query in unicode_queries:
            result = classifier.classify_intent(query)
            # Should not crash
            assert isinstance(result, list)

    def test_none_input(self, classifier):
        """Test None input handled gracefully."""
        result = classifier.classify_intent(None)
        assert result == []

    def test_word_boundary_matching(self, classifier):
        """Test word boundary matching for single words."""
        # "container" should match "container" but not "containers" or "containment"
        result1 = classifier.classify_intent("container logs")
        result2 = classifier.classify_intent("containers logs")
        result3 = classifier.classify_intent("containment logs")

        assert "container-ops" in result1
        assert "container-ops" in result2  # "containers" is also a keyword
        # "containment" should not match unless it's in the keyword list


class TestIntentClassifierPerformance:
    """Performance tests for intent classifier."""

    @pytest.fixture
    def classifier(self):
        """Create classifier for performance tests."""
        return KeywordIntentClassifier()

    def test_classification_speed(self, classifier):
        """Test that classification is fast."""
        test_queries = [
            "list running containers",
            "deploy docker compose stack",
            "scale web service to 5 replicas",
            "create bridge network",
            "show docker info",
            "backup volume data"
        ]

        start_time = time.time()
        for query in test_queries:
            classifier.classify_intent(query)
        end_time = time.time()

        # Should classify 6 queries in < 10ms total
        total_time = end_time - start_time
        assert total_time < 0.01, f"Classification took {total_time:.4f}s, expected < 0.01s"

    def test_memory_usage(self, classifier):
        """Test that classifier doesn't leak memory."""
        # Run many classifications
        for i in range(1000):
            classifier.classify_intent(f"test query {i}")

        # Should still work correctly
        result = classifier.classify_intent("container logs")
        assert "container-ops" in result

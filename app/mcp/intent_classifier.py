"""
Intent Classification Module

Analyzes natural language queries to determine relevant Docker task types.
Supports keyword-based pattern matching with extensible design for future LLM integration.
"""

import logging
import re
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)


class IntentClassifierBase(ABC):
    """Abstract base class for intent classifiers."""

    @abstractmethod
    def classify_intent(self, query: str) -> list[str]:
        """
        Classify a natural language query into relevant task types.

        Args:
            query: Natural language query from the LLM

        Returns:
            List of detected task types (e.g., ["container-ops", "compose-ops"])
        """
        pass


class KeywordIntentClassifier(IntentClassifierBase):
    """
    Keyword-based intent classifier using pattern matching.

    Maps natural language queries to Docker task types using configurable
    keyword mappings. Supports case-insensitive matching and multi-word phrases.
    """

    def __init__(self, keyword_mappings: Optional[dict[str, list[str]]] = None):
        """
        Initialize the classifier with keyword mappings.

        Args:
            keyword_mappings: Dict mapping task types to keyword lists.
                            If None, uses default mappings.
        """
        self.keyword_mappings = keyword_mappings or self._get_default_mappings()
        logger.info(f"Intent classifier initialized with {len(self.keyword_mappings)} task types")

    def classify_intent(self, query: str) -> list[str]:
        """
        Classify query into task types using keyword matching.

        Args:
            query: Natural language query

        Returns:
            List of detected task types
        """
        if not query or not query.strip():
            return []

        query_lower = query.lower().strip()
        detected_types = []

        for task_type, keywords in self.keyword_mappings.items():
            if self._matches_keywords(query_lower, keywords):
                detected_types.append(task_type)
                logger.debug(f"Query matched task type '{task_type}': {query[:50]}...")

        if detected_types:
            logger.info(f"Intent classifier detected task types: {detected_types} for query: {query[:100]}...")
        else:
            logger.debug(f"No task types detected for query: {query[:50]}...")

        return detected_types

    def _matches_keywords(self, query: str, keywords: list[str]) -> bool:
        """
        Check if query matches any keywords for a task type.

        Args:
            query: Lowercase query string
            keywords: List of keywords/phrases to match

        Returns:
            True if any keyword matches
        """
        for keyword in keywords:
            # Support both exact word matches and phrase matches
            if keyword.lower() in query:
                return True

            # Also check for word boundaries for single words
            if len(keyword.split()) == 1:
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, query):
                    return True

        return False

    def get_keyword_mappings(self) -> dict[str, list[str]]:
        """Get current keyword mappings for observability."""
        return self.keyword_mappings.copy()

    def _get_default_mappings(self) -> dict[str, list[str]]:
        """Get default keyword mappings for Docker task types."""
        return {
            "container-ops": [
                "container", "containers", "docker run", "start", "stop",
                "restart", "logs", "exec", "attach", "inspect container",
                "running container", "container status", "docker container",
                "container logs", "container exec", "container start",
                "container stop", "container restart", "container remove",
                "container inspect", "container list", "container create"
            ],
            "compose-ops": [
                "compose", "stack", "deploy", "docker-compose", "docker compose",
                "compose file", "compose.yaml", "docker-compose.yml",
                "multi-container", "orchestrate", "compose up", "compose down",
                "compose build", "compose start", "compose stop", "compose restart",
                "compose logs", "compose ps", "compose scale", "stack deploy",
                "stack remove", "stack list", "stack services"
            ],
            "service-ops": [
                "service", "services", "swarm", "scale", "replicas",
                "swarm service", "service scale", "update service",
                "docker service", "service create", "service remove",
                "service inspect", "service logs", "service ps",
                "service update", "service rollback", "service list"
            ],
            "network-ops": [
                "network", "networks", "bridge", "overlay", "subnet",
                "network create", "network connect", "network disconnect",
                "docker network", "network inspect", "network remove",
                "network list", "bridge network", "overlay network",
                "network driver", "network ip", "network gateway"
            ],
            "volume-ops": [
                "volume", "volumes", "storage", "mount", "bind",
                "volume create", "persistent storage", "data volume",
                "docker volume", "volume inspect", "volume remove",
                "volume list", "volume driver", "volume mount",
                "bind mount", "tmpfs", "volume backup"
            ],
            "system-ops": [
                "info", "ping", "version", "status", "system",
                "docker info", "docker version", "health check",
                "connectivity", "daemon", "docker system", "system df",
                "system prune", "system events", "docker events",
                "docker stats", "docker top", "docker history"
            ]
        }


# Future: LLM-based classifier
class LLMIntentClassifier(IntentClassifierBase):
    """
    LLM-based intent classifier (future implementation).

    Uses OpenAI/Anthropic APIs to classify queries into task types.
    Provides higher accuracy but requires API calls and costs.
    """

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize LLM classifier.

        Args:
            api_key: API key for LLM service
            model: Model to use for classification
        """
        self.api_key = api_key
        self.model = model
        # TODO: Implement LLM-based classification
        raise NotImplementedError("LLM-based classification not yet implemented")

    def classify_intent(self, query: str) -> list[str]:
        """Classify query using LLM."""
        # TODO: Implement LLM-based classification
        raise NotImplementedError("LLM-based classification not yet implemented")

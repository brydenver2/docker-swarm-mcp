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
        Determine one or more Docker-related task types expressed in a natural language query.
        
        Parameters:
            query (str): The natural language text to classify.
        
        Returns:
            list[str]: Detected task type identifiers (for example, "container-ops", "compose-ops").
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
        Create a KeywordIntentClassifier using the supplied keyword mappings or defaults.
        
        Parameters:
            keyword_mappings (Optional[dict[str, list[str]]]): Mapping from task type identifiers (e.g., "container-ops") to lists of keywords or phrases that indicate that task type. If None, a default mapping set is used.
        """
        self.keyword_mappings = keyword_mappings or self._get_default_mappings()
        logger.info(f"Intent classifier initialized with {len(self.keyword_mappings)} task types")

    def classify_intent(self, query: str) -> list[str]:
        """
        Determine Docker task types present in a natural-language query using the classifier's configured keyword mappings.
        
        Returns:
            list[str]: Detected task type identifiers (for example, "container-ops", "compose-ops"); empty list if no keywords match.
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
        Determine whether the query matches any of the provided keywords or phrases.
        
        Parameters:
            query (str): The text to search; expected to be normalized (e.g., lowercased and trimmed).
            keywords (list[str]): Keywords or phrases to match against the query.
        
        Returns:
            True if the query contains any keyword as a substring or contains a single-word keyword as a whole word, False otherwise.
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
        """
        Return a shallow copy of the current keyword-to-keywords mappings for inspection.
        
        Returns:
            dict[str, list[str]]: A shallow copy of the mapping where keys are task types and values are lists of keywords.
        """
        return self.keyword_mappings.copy()

    def _get_default_mappings(self) -> dict[str, list[str]]:
        """
        Return default keyword mappings used to map natural-language queries to Docker task types.
        
        Returns:
            dict[str, list[str]]: Mapping from task-type keys (e.g., "container-ops") to lists of associated keyword phrases used for pattern matching.
        """
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
        Create a placeholder LLM-based intent classifier and store the provided API credentials.
        
        Parameters:
            api_key (str): API key for the LLM service.
            model (str): Identifier of the LLM model to use (default: "gpt-3.5-turbo").
        
        Raises:
            NotImplementedError: Always raised because the LLM-based classifier is not yet implemented.
        """
        self.api_key = api_key
        self.model = model
        # TODO: Implement LLM-based classification
        raise NotImplementedError("LLM-based classification not yet implemented")

    def classify_intent(self, query: str) -> list[str]:
        """Classify query using LLM."""
        # TODO: Implement LLM-based classification
        raise NotImplementedError("LLM-based classification not yet implemented")
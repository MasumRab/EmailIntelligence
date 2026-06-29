"""
SonarQube REST API Client Integration

This module provides a client to interact with the SonarQube/SonarCloud REST API.
It allows fetching, searching, and managing code quality issues.
"""

import os
import logging
from typing import Dict, Any, List, Union
import requests

logger = logging.getLogger(__name__)

class SonarQubeClient:
    """
    Client for interacting with the SonarQube / SonarCloud REST API.
    """

    def __init__(
        self,
        host_url: str = None,
        project_key: str = None,
        token: str = None,
    ):
        """
        Initialize the SonarQube client.

        Args:
            host_url: The URL of the SonarQube server (defaults to SONAR_HOST_URL env var or https://sonarcloud.io)
            project_key: The project key to query (defaults to SONAR_PROJECT_KEY env var)
            token: The authentication token (defaults to SONAR_TOKEN env var)
        """
        self.host_url = host_url or os.environ.get("SONAR_HOST_URL", "https://sonarcloud.io")
        self.host_url = self.host_url.rstrip("/")

        self.project_key = project_key or os.environ.get("SONAR_PROJECT_KEY")
        self.token = token or os.environ.get("SONAR_TOKEN")

        self.session = requests.Session()
        if self.token:
            # SonarQube uses basic auth with the token as the username and an empty password
            self.session.auth = (self.token, "")

        # Ensure we always get JSON responses
        self.session.headers.update({"Accept": "application/json"})

    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Helper method to make API requests.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., "/api/issues/search")
            params: Query parameters

        Returns:
            JSON response dictionary
        """
        url = f"{self.host_url}{endpoint}"

        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"SonarQube API request failed: {method} {url} - {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    logger.error(f"Error details: {error_data}")
                except ValueError:
                    logger.error(f"Raw error response: {e.response.text}")
            raise

    def search_issues(
        self,
        severities: str = None,
        types: str = None,
        statuses: str = None,
        paged: bool = False,
        page_size: int = 100,
        page_index: int = 1,
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Search for issues in the configured project.

        When ``paged`` is ``False`` (default), this method returns only the list of
        issues from the first page that matches the given filters.

        When ``paged`` is ``True``, this method returns the full paginated response
        from SonarQube (including paging metadata and any additional fields).

        :param severities: Comma-separated list of severities (e.g. "BLOCKER,CRITICAL").
        :param types: Comma-separated list of types (e.g. "BUG,VULNERABILITY,CODE_SMELL").
        :param statuses: Comma-separated list of statuses (e.g. "OPEN,CONFIRMED").
        :param paged: If True, return the full paginated response; otherwise return
                      only the list of issues.
        :param page_size: Page size (SonarQube parameter ``ps``).
        :param page_index: Page index, 1-based (SonarQube parameter ``p``).
        :return: If ``paged`` is False, returns ``List[Dict[str, Any]]`` of issues.
                 If ``paged`` is True, returns the full SonarQube response as
                 ``Dict[str, Any]``.
        """
        params: Dict[str, Any] = {
            # SonarQube paging parameters
            "ps": min(page_size, 500),
            "p": page_index,
        }

        # Respect existing project configuration if present on the client
        project_key = getattr(self, "project_key", None)
        if project_key:
            params["componentKeys"] = project_key

        if severities:
            params["severities"] = severities
        if types:
            params["types"] = types
        if statuses:
            params["statuses"] = statuses
        else:
            # Default to unresolved issues if not specified
            params["resolved"] = "false"

        # Delegate to the existing request helper on this client
        response: Dict[str, Any] = self._make_request(
            method="GET",
            endpoint="/api/issues/search",
            params=params,
        )

        if paged:
            # Caller handles pagination metadata and any further paging logic
            return response

        # Default behavior: return just the issues list
        return response.get("issues", [])

    def get_issues(
        self,
        severities: str = None,
        types: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get a flat list of issues up to the specified limit.
        Handles pagination automatically.

        Args:
            severities: Comma-separated list of severities
            types: Comma-separated list of types
            limit: Maximum number of issues to return

        Returns:
            List of issue dictionaries
        """
        all_issues = []
        page_size = min(limit, 100)
        page_index = 1

        while len(all_issues) < limit:
            response = self.search_issues(
                severities=severities,
                types=types,
                paged=True,
                page_size=page_size,
                page_index=page_index
            )

            issues = response.get("issues", [])
            if not issues:
                break

            all_issues.extend(issues)

            # Check if we've retrieved all available issues
            paging = response.get("paging", {})
            total = paging.get("total", 0)

            if len(all_issues) >= total or len(issues) < page_size:
                break

            page_index += 1

        return all_issues[:limit]

    def get_issue_details(self, issue_key: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific issue.

        Args:
            issue_key: The key of the issue (e.g., "AWf1-234...")

        Returns:
            Dictionary containing the issue details
        """
        params = {"issues": issue_key}
        response = self._make_request("GET", "/api/issues/search", params)

        issues = response.get("issues", [])
        if not issues:
            raise ValueError(f"Issue not found: {issue_key}")

        return issues[0]

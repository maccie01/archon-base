"""
Auto-Tagging Service

Provides automatic tag suggestions based on URL patterns and content analysis.
"""

import re
from typing import Any

from ...config.logfire_config import get_logger

logger = get_logger(__name__)


class AutoTaggingService:
    """
    Service for automatically suggesting tags based on content analysis.

    Uses URL pattern matching and content keyword detection to suggest
    relevant tags for knowledge sources during creation.
    """

    # URL pattern matching - maps regex patterns to tag lists
    URL_TAG_PATTERNS = {
        r"react\.dev|reactjs\.org": ["react", "javascript"],
        r"nextjs\.org": ["nextjs", "react"],
        r"fastapi\.tiangolo\.com": ["fastapi", "python"],
        r"docs\.docker\.com|docker\.com": ["docker", "deployment"],
        r"postgresql\.org": ["postgresql", "database"],
        r"mongodb\.com": ["mongodb", "database"],
        r"redis\.io": ["redis", "database"],
        r"kubernetes\.io": ["kubernetes", "deployment"],
        r"docs\.djangoproject\.com": ["django", "python"],
        r"expressjs\.com": ["express", "javascript"],
        r"rust-lang\.org": ["rust"],
        r"golang\.org|go\.dev": ["go"],
        r"typescriptlang\.org": ["typescript", "javascript"],
        r"tailwindcss\.com": ["tailwindcss", "css"],
        r"supabase\.com": ["supabase", "database"],
        r"radix-ui\.com": ["radix-ui", "ui"],
        r"github\.com": ["github", "documentation"],
        r"npmjs\.com": ["npm", "javascript"],
        r"code\.visualstudio\.com": ["vscode", "tools"],
        r"developer\.mozilla\.org": ["mdn", "documentation"],
        r"stackoverflow\.com": ["stackoverflow", "qa"],
        r"auth0\.com": ["authentication", "security"],
        r"openapi|swagger": ["openapi", "api"],
        r"graphql\.org": ["graphql", "api"],
        r"stripe\.com": ["payment", "api"],
    }

    # Content keyword matching - maps keywords to tag lists
    CONTENT_TAG_KEYWORDS = {
        "authentication": ["authentication", "security"],
        "authorization": ["authorization", "security"],
        "testing": ["testing"],
        "unit test": ["unit-testing", "testing"],
        "integration test": ["integration-testing", "testing"],
        "e2e test": ["e2e-testing", "testing"],
        "api reference": ["api-reference", "documentation"],
        "tutorial": ["tutorial", "documentation"],
        "guide": ["tutorial", "documentation"],
        "architecture": ["architecture-docs", "documentation"],
        "troubleshooting": ["troubleshooting", "documentation"],
        "microservices": ["microservices", "architecture"],
        "rest api": ["rest-api", "architecture", "api"],
        "graphql": ["graphql", "architecture", "api"],
        "encryption": ["encryption", "security"],
        "ci/cd": ["ci-cd", "deployment"],
        "deployment": ["deployment"],
        "deploy": ["deployment"],
        "production": ["deployment"],
        "docker": ["docker", "deployment"],
        "kubernetes": ["kubernetes", "deployment"],
        "database": ["database"],
        "sql": ["database"],
        "vector search": ["vector-search", "database"],
        "websocket": ["websockets", "api"],
        "design system": ["design-system", "ui"],
    }

    def __init__(self, supabase_client=None):
        """
        Initialize the auto-tagging service.

        Args:
            supabase_client: Optional Supabase client (for future use)
        """
        self.supabase = supabase_client

    async def suggest_tags(
        self, url: str, title: str | None = None, summary: str | None = None
    ) -> list[str]:
        """
        Suggest tags based on URL patterns and content analysis.

        Args:
            url: The URL of the knowledge source
            title: Optional title of the source
            summary: Optional summary/description of the source

        Returns:
            List of suggested tag names (lowercase, deduplicated, ordered)
        """
        try:
            logger.info(f"Suggesting tags | url={url}")

            suggested_tags = []

            # Check URL patterns
            url_tags = self._match_url_patterns(url)
            suggested_tags.extend(url_tags)

            # Check content keywords
            content_tags = self._match_content_keywords(title, summary)
            suggested_tags.extend(content_tags)

            # Remove duplicates while preserving order
            unique_tags = list(dict.fromkeys(suggested_tags))

            # Normalize to lowercase
            normalized_tags = [tag.lower().strip() for tag in unique_tags]

            logger.info(
                f"Tags suggested | url={url} | tag_count={len(normalized_tags)} | tags={normalized_tags}"
            )

            return normalized_tags

        except Exception as e:
            logger.error(f"Failed to suggest tags | error={str(e)} | url={url}")
            # Return empty list on error rather than failing
            return []

    def _match_url_patterns(self, url: str) -> list[str]:
        """
        Match URL against known patterns to suggest tags.

        Args:
            url: URL to match against patterns

        Returns:
            List of suggested tags based on URL patterns
        """
        matched_tags = []

        if not url:
            return matched_tags

        try:
            # Check each pattern
            for pattern, tags in self.URL_TAG_PATTERNS.items():
                if re.search(pattern, url, re.IGNORECASE):
                    matched_tags.extend(tags)
                    logger.debug(f"URL pattern matched | pattern={pattern} | tags={tags}")

        except Exception as e:
            logger.warning(f"Error matching URL patterns | error={str(e)} | url={url}")

        return matched_tags

    def _match_content_keywords(
        self, title: str | None, summary: str | None
    ) -> list[str]:
        """
        Match content keywords in title and summary to suggest tags.

        Args:
            title: Title of the knowledge source
            summary: Summary/description of the knowledge source

        Returns:
            List of suggested tags based on content keywords
        """
        matched_tags = []

        # Combine title and summary for keyword matching
        content_parts = []
        if title:
            content_parts.append(title)
        if summary:
            content_parts.append(summary)

        if not content_parts:
            return matched_tags

        content = " ".join(content_parts).lower()

        try:
            # Check each keyword
            for keyword, tags in self.CONTENT_TAG_KEYWORDS.items():
                if keyword.lower() in content:
                    matched_tags.extend(tags)
                    logger.debug(f"Content keyword matched | keyword={keyword} | tags={tags}")

        except Exception as e:
            logger.warning(f"Error matching content keywords | error={str(e)}")

        return matched_tags

    def add_url_pattern(self, pattern: str, tags: list[str]) -> None:
        """
        Add a custom URL pattern for tag suggestion.

        This allows dynamic extension of URL patterns at runtime.

        Args:
            pattern: Regular expression pattern to match URLs
            tags: List of tags to suggest when pattern matches
        """
        try:
            # Validate pattern is a valid regex
            re.compile(pattern)

            self.URL_TAG_PATTERNS[pattern] = tags
            logger.info(f"Added URL pattern | pattern={pattern} | tags={tags}")

        except re.error as e:
            logger.error(f"Invalid regex pattern | pattern={pattern} | error={str(e)}")
            raise ValueError(f"Invalid regex pattern: {str(e)}")

    def add_content_keyword(self, keyword: str, tags: list[str]) -> None:
        """
        Add a custom content keyword for tag suggestion.

        This allows dynamic extension of content keywords at runtime.

        Args:
            keyword: Keyword to search for in content
            tags: List of tags to suggest when keyword is found
        """
        try:
            self.CONTENT_TAG_KEYWORDS[keyword.lower()] = tags
            logger.info(f"Added content keyword | keyword={keyword} | tags={tags}")

        except Exception as e:
            logger.error(f"Failed to add content keyword | error={str(e)}")
            raise

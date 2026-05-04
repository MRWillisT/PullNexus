"""Shared schema constants for PullNexus JSON outputs."""

SCHEMA_VERSION = "1.0"

# Fields required in every skill.json
REQUIRED_FIELDS = ("name", "version", "description", "tags", "license")

# Provenance fields — recommended for all resource types
PROVENANCE_FIELDS = ("source", "author")

# Quality metadata fields — recommended for all resource types
QUALITY_FIELDS = ("maturity", "maintained", "last_verified")

# Supersession: a skill entry can declare `"supersedes": "old-skill-name"`.
# The superseded entry is hidden from search results by default but remains
# accessible via `pullnexus info <old-name>`.
SUPERSEDES_FIELD = "supersedes"

# Resource types that do not require downloadable file packages
NON_INSTALLABLE_TYPES = frozenset({"repository", "eval", "policy"})

# Resource types that do not require training examples (examples.jsonl)
NO_EXAMPLES_REQUIRED_TYPES = frozenset({
    "tool", "playbook", "dataset", "eval", "policy",
    "template", "environment", "repository",
})

"""
Rich styles and display labels for Lupaxa GitHub Repository Sync.

All application colours, presentation styles, and display labels are
centralised here so the console appearance can be changed without modifying
operational code.
"""

from __future__ import annotations

from typing import Final

#
# General labels
#

LABEL_INFORMATION: Final[str] = "Info"
LABEL_SUCCESS: Final[str] = "Success"
LABEL_WARNING: Final[str] = "Warning"
LABEL_ERROR: Final[str] = "Error"


#
# General styles
#

STYLE_BOLD: Final[str] = "bold"
STYLE_LABEL: Final[str] = "cyan"

STYLE_HEADING: Final[str] = "bold"
STYLE_DETAIL_LABEL: Final[str] = "cyan"
STYLE_MUTED: Final[str] = "dim"
STYLE_PATH: Final[str] = "cyan"
STYLE_REPOSITORY: Final[str] = "bold"

STYLE_SUCCESS: Final[str] = "bold green"
STYLE_INFORMATION: Final[str] = "bold cyan"
STYLE_WARNING: Final[str] = "bold yellow"
STYLE_ERROR: Final[str] = "bold red"

STYLE_TABLE_HEADER: Final[str] = "bold"


#
# Rule styles
#

STYLE_RULE_PRIMARY: Final[str] = "bold"
STYLE_RULE_SECONDARY: Final[str] = "bold"


#
# Repository action labels and styles
#

REPOSITORY_ACTION_LABELS: Final[dict[str, str]] = {
    "clone": "Clone",
    "cloned": "Cloned",
    "update": "Update",
    "updated": "Updated",
    "skipped": "Skipped",
}

STYLE_ACTION_CLONING: Final[str] = "cyan"
STYLE_ACTION_UPDATING: Final[str] = "cyan"

STYLE_ACTION_CLONED: Final[str] = "bold green"
STYLE_ACTION_UPDATED: Final[str] = "bold green"
STYLE_ACTION_SKIPPED: Final[str] = "bold yellow"

REPOSITORY_ACTION_STYLES: Final[dict[str, str]] = {
    "clone": STYLE_ACTION_CLONING,
    "cloned": STYLE_ACTION_CLONED,
    "update": STYLE_ACTION_UPDATING,
    "updated": STYLE_ACTION_UPDATED,
    "skipped": STYLE_ACTION_SKIPPED,
}


#
# Summary styles
#

STYLE_SUMMARY_CLONED: Final[str] = "bold cyan"
STYLE_SUMMARY_UPDATED: Final[str] = "bold green"
STYLE_SUMMARY_SKIPPED: Final[str] = "bold yellow"
STYLE_SUMMARY_FAILED: Final[str] = "bold red"

STYLE_SUMMARY_TO_CLONE: Final[str] = "cyan"
STYLE_SUMMARY_TO_UPDATE: Final[str] = "green"
STYLE_SUMMARY_ATTENTION: Final[str] = "yellow"
STYLE_SUMMARY_PROBLEM: Final[str] = "red"


#
# Repository inspection labels and styles
#

REPOSITORY_INSPECTION_LABELS: Final[dict[str, str]] = {
    "clone": "Clone",
    "update": "Update",
    "invalid": "Invalid",
    "bare": "Bare",
    "detached": "Detached",
    "no-origin": "No Origin",
    "origin-mismatch": "Wrong Origin",
    "dirty": "Dirty",
    "no-upstream": "No Upstream",
    "upstream-mismatch": "Wrong Upstream",
    "inaccessible": "Inaccessible",
}

REPOSITORY_INSPECTION_STYLES: Final[dict[str, str]] = {
    "clone": STYLE_INFORMATION,
    "update": STYLE_SUCCESS,
    "invalid": STYLE_ERROR,
    "bare": STYLE_ERROR,
    "detached": STYLE_WARNING,
    "no-origin": STYLE_WARNING,
    "origin-mismatch": STYLE_ERROR,
    "dirty": STYLE_WARNING,
    "no-upstream": STYLE_WARNING,
    "upstream-mismatch": STYLE_WARNING,
    "inaccessible": STYLE_ERROR,
}


#
# Repository status check labels and styles
#

REPOSITORY_STATUS_CHECK_LABELS: Final[dict[str, str]] = {
    "clean": "Clean",
    "missing": "Missing",
    "ahead": "Ahead",
    "behind": "Behind",
    "diverged": "Diverged",
    "history-rewritten": "History Rewritten",
    "fetch-failed": "Fetch Failed",
    "dirty": "Dirty",
    "invalid": "Invalid",
    "bare": "Bare",
    "detached": "Detached",
    "no-origin": "No Origin",
    "origin-mismatch": "Wrong Origin",
    "no-upstream": "No Upstream",
    "upstream-mismatch": "Wrong Upstream",
    "inaccessible": "Inaccessible",
}

REPOSITORY_STATUS_CHECK_STYLES: Final[dict[str, str]] = {
    "clean": STYLE_SUCCESS,
    "missing": STYLE_INFORMATION,
    "ahead": STYLE_WARNING,
    "behind": STYLE_WARNING,
    "diverged": STYLE_WARNING,
    "history-rewritten": STYLE_WARNING,
    "fetch-failed": STYLE_ERROR,
    "dirty": STYLE_WARNING,
    "invalid": STYLE_ERROR,
    "bare": STYLE_ERROR,
    "detached": STYLE_ERROR,
    "no-origin": STYLE_ERROR,
    "origin-mismatch": STYLE_ERROR,
    "no-upstream": STYLE_ERROR,
    "upstream-mismatch": STYLE_ERROR,
    "inaccessible": STYLE_ERROR,
}


#
# Repository result labels and styles
#

REPOSITORY_RESULT_LABELS: Final[dict[str, str]] = {
    "success": "Success",
    "invalid": "Invalid",
    "bare": "Bare",
    "detached": "Detached",
    "no-origin": "No Origin",
    "origin-mismatch": "Wrong Origin",
    "dirty": "Dirty",
    "history-rewritten": "History Rewritten",
    "no-upstream": "No Upstream",
    "upstream-mismatch": "Wrong Upstream",
    "inaccessible": "Inaccessible",
    "failed": "Failed",
}

REPOSITORY_RESULT_STYLES: Final[dict[str, str]] = {
    "success": STYLE_SUCCESS,
    "invalid": STYLE_ERROR,
    "bare": STYLE_ERROR,
    "detached": STYLE_WARNING,
    "no-origin": STYLE_WARNING,
    "origin-mismatch": STYLE_ERROR,
    "dirty": STYLE_WARNING,
    "history-rewritten": STYLE_WARNING,
    "no-upstream": STYLE_WARNING,
    "upstream-mismatch": STYLE_WARNING,
    "inaccessible": STYLE_ERROR,
    "failed": STYLE_ERROR,
}


#
# Special successful result labels and styles
#

RESULT_LABEL_CLONED: Final[str] = "Cloned"
RESULT_STYLE_CLONED: Final[str] = STYLE_SUMMARY_CLONED

RESULT_LABEL_UPDATED: Final[str] = "Updated"
RESULT_STYLE_UPDATED: Final[str] = STYLE_SUMMARY_UPDATED


#
# Configuration summary labels and styles
#

CONFIGURATION_STATUS_LABELS: Final[dict[str, str]] = {
    "clone": "To Clone",
    "update": "To Update",
    "dirty": "Dirty",
    "origin-mismatch": "Wrong Origin",
    "detached": "Detached",
    "no-origin": "No Origin",
    "no-upstream": "No Upstream",
    "upstream-mismatch": "Wrong Upstream",
    "invalid": "Invalid",
    "bare": "Bare",
    "inaccessible": "Inaccessible",
}

CONFIGURATION_STATUS_STYLES: Final[dict[str, str]] = {
    "clone": STYLE_SUMMARY_TO_CLONE,
    "update": STYLE_SUMMARY_TO_UPDATE,
    "dirty": STYLE_SUMMARY_ATTENTION,
    "origin-mismatch": STYLE_SUMMARY_PROBLEM,
    "detached": STYLE_SUMMARY_ATTENTION,
    "no-origin": STYLE_SUMMARY_ATTENTION,
    "no-upstream": STYLE_SUMMARY_ATTENTION,
    "upstream-mismatch": STYLE_SUMMARY_ATTENTION,
    "invalid": STYLE_SUMMARY_PROBLEM,
    "bare": STYLE_SUMMARY_PROBLEM,
    "inaccessible": STYLE_SUMMARY_PROBLEM,
}

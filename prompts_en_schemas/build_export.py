"""Build a thesis export of prompt texts and compact schema contracts.

Inputs:
- Read-only source files from the matcher and AI-agent codebases.

Outputs:
- prompts_schemas_export.md: readable thesis appendix.
- prompts_schemas_export.json: machine-readable index.
- structured/: GitHub-readable folder appendix with separate Markdown files
  per prompt/schema item where needed.

Pipeline role:
- Documents the LLM prompt and output-schema contracts used in the thesis
  pipeline without importing runtime modules, calling APIs, or touching the DB.

Changelog:
- 2026-06-05: Created reproducible prompt/schema export for thesis appendix.
- 2026-06-05: Added structured export folders for readable thesis navigation.
- 2026-06-06: Made structured export GitHub-friendly with separate files for
  colliding prompt/schema items and a root README.
"""

from __future__ import annotations

import ast
import hashlib
import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPORT_VERSION = "prompts_schema_export_20260605_v1"
EXPORT_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXPORT_DIR.parents[1]
OUTPUT_MD = EXPORT_DIR / "prompts_schemas_export.md"
OUTPUT_JSON = EXPORT_DIR / "prompts_schemas_export.json"
STRUCTURED_DIR = EXPORT_DIR / "structured"
STRUCTURED_README_MD = STRUCTURED_DIR / "README.md"
STRUCTURED_INDEX_MD = STRUCTURED_DIR / "INDEX.md"
STRUCTURED_MANIFEST_JSON = STRUCTURED_DIR / "manifest.json"

BLOCKED_PATH_PARTS = {
    ".agent_call_cache",
    ".env",
    ".git",
    ".pytest_cache",
    "__pycache__",
    "cache",
    "checkpoints",
    "debug",
    "o",
    "out",
    "output",
    "temp",
}


@dataclass(frozen=True)
class PythonSource:
    codebase: str
    relative_path: str
    status: str
    reason: str
    symbols: tuple[str, ...] = ()
    functions: tuple[str, ...] = ()
    include_classes: bool = False
    include_prompt_constants: bool = False
    include_schema_constants: bool = False


@dataclass(frozen=True)
class TextSource:
    codebase: str
    relative_path: str
    status: str
    category: str
    reason: str
    symbol_name: str | None = None


@dataclass(frozen=True)
class PythonGlob:
    codebase: str
    pattern: str
    status: str
    reason: str
    include_classes: bool = False
    include_prompt_constants: bool = False
    include_schema_constants: bool = False


@dataclass(frozen=True)
class TextGlob:
    codebase: str
    pattern: str
    status: str
    category: str
    reason: str


@dataclass
class AssignmentInfo:
    name: str
    line: int
    end_line: int | None
    value_kind: str
    value: Any
    value_source: str
    assignment_source: str


@dataclass
class ClassSummary:
    name: str
    line: int
    bases: list[str]
    fields: list[dict[str, Any]] = field(default_factory=list)
    enum_values: list[dict[str, Any]] = field(default_factory=list)
    validators: list[dict[str, Any]] = field(default_factory=list)
    docstring: str | None = None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative_display(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def assert_safe_source_path(relative_path: str) -> None:
    path = Path(relative_path)
    parts = {part.lower() for part in path.parts}
    if ".env" in parts or path.name.lower() == ".env":
        raise ValueError(f"Refusing to export environment file: {relative_path}")
    if parts & BLOCKED_PATH_PARTS:
        raise ValueError(f"Refusing blocked runtime/cache path: {relative_path}")


def safe_unparse(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:
        return None


def literal_or_source(node: ast.AST, file_text: str) -> tuple[str, Any, str]:
    source = ast.get_source_segment(file_text, node) or safe_unparse(node) or ""
    try:
        value = ast.literal_eval(node)
        return type(value).__name__, value, source
    except Exception:
        if isinstance(node, ast.JoinedStr):
            return "f_string_template", joined_str_template(node, file_text), source
        return type(node).__name__, None, source


def joined_str_template(node: ast.JoinedStr, file_text: str) -> str:
    parts: list[str] = []
    for value in node.values:
        if isinstance(value, ast.Constant):
            parts.append(str(value.value))
        elif isinstance(value, ast.FormattedValue):
            expression = ast.get_source_segment(file_text, value.value) or safe_unparse(value.value) or "..."
            parts.append("{" + expression + "}")
    return "".join(parts)


def assignment_targets(node: ast.Assign | ast.AnnAssign) -> list[str]:
    if isinstance(node, ast.AnnAssign):
        return [node.target.id] if isinstance(node.target, ast.Name) else []
    names: list[str] = []
    for target in node.targets:
        if isinstance(target, ast.Name):
            names.append(target.id)
    return names


def collect_assignments(tree: ast.Module, file_text: str) -> dict[str, AssignmentInfo]:
    assignments: dict[str, AssignmentInfo] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        value_node = node.value
        if value_node is None:
            continue
        value_kind, value, value_source = literal_or_source(value_node, file_text)
        assignment_source = ast.get_source_segment(file_text, node) or value_source
        for name in assignment_targets(node):
            assignments[name] = AssignmentInfo(
                name=name,
                line=getattr(node, "lineno", 0),
                end_line=getattr(node, "end_lineno", None),
                value_kind=value_kind,
                value=value,
                value_source=value_source,
                assignment_source=assignment_source,
            )
    return assignments


def decorator_name(decorator: ast.AST) -> str:
    text = safe_unparse(decorator)
    return text or type(decorator).__name__


def summarize_class(node: ast.ClassDef, file_text: str) -> ClassSummary:
    summary = ClassSummary(
        name=node.name,
        line=node.lineno,
        bases=[safe_unparse(base) or type(base).__name__ for base in node.bases],
        docstring=ast.get_docstring(node),
    )
    for child in node.body:
        if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            value_kind = None
            default_source = None
            if child.value is not None:
                value_kind, _, default_source = literal_or_source(child.value, file_text)
            summary.fields.append(
                {
                    "name": child.target.id,
                    "annotation": safe_unparse(child.annotation),
                    "default_kind": value_kind,
                    "default_source": default_source,
                    "line": child.lineno,
                }
            )
        elif isinstance(child, ast.Assign):
            for name in assignment_targets(child):
                value_kind, value, value_source = literal_or_source(child.value, file_text)
                if name.isupper() or isinstance(value, (str, int, float, bool)):
                    summary.enum_values.append(
                        {
                            "name": name,
                            "value_kind": value_kind,
                            "value": value,
                            "source": value_source,
                            "line": child.lineno,
                        }
                    )
        elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decorators = [decorator_name(decorator) for decorator in child.decorator_list]
            if (
                any("validator" in decorator.lower() for decorator in decorators)
                or child.name.startswith("_validate")
                or child.name.startswith("_normalize")
                or child.name.startswith("_coerce")
            ):
                summary.validators.append(
                    {
                        "name": child.name,
                        "decorators": decorators,
                        "line": child.lineno,
                    }
                )
    return summary


def summarize_classes(tree: ast.Module, file_text: str) -> list[dict[str, Any]]:
    return [
        summarize_class(node, file_text).__dict__
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]


def is_prompt_symbol(name: str) -> bool:
    upper = name.upper()
    return any(token in upper for token in ("PROMPT", "INSTRUCTION", "FRAMING"))


def is_schema_symbol(name: str) -> bool:
    upper = name.upper()
    return any(
        token in upper
        for token in (
            "SCHEMA",
            "CONTRACT",
            "ALLOWED",
            "CHOICES",
            "LABELS",
            "RELATION_ROLES",
            "STAGE_DEFINITIONS",
        )
    )


def symbol_category(name: str, default: str = "contract") -> str:
    upper = name.upper()
    if "VERSION" in upper:
        return "version"
    if is_prompt_symbol(name):
        return "prompt"
    if is_schema_symbol(name):
        return "schema_contract"
    return default


def version_info(assignments: dict[str, AssignmentInfo]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name, info in assignments.items():
        if "VERSION" in name.upper() and isinstance(info.value, str):
            versions[name] = info.value
    return versions


def build_base_item(
    *,
    codebase: str,
    relative_path: str,
    status: str,
    category: str,
    reason: str,
    symbol_name: str,
    symbol_type: str,
    source_text: str,
    source_file_sha256: str,
    versions: dict[str, str] | None = None,
) -> dict[str, Any]:
    content_hash = sha256_text(source_text)
    return {
        "id": f"{relative_path}::{symbol_name}",
        "codebase": codebase,
        "source_path": relative_path,
        "symbol_name": symbol_name,
        "symbol_type": symbol_type,
        "category": category,
        "status": status,
        "reason_for_thesis": reason,
        "sha256": content_hash,
        "source_file_sha256": source_file_sha256,
        "prompt_or_schema_versions": versions or {},
    }


def extract_python_source(spec: PythonSource) -> list[dict[str, Any]]:
    assert_safe_source_path(spec.relative_path)
    path = REPO_ROOT / spec.relative_path
    if not path.exists():
        return [
            build_missing_source_item(
                codebase=spec.codebase,
                relative_path=spec.relative_path,
                status=spec.status,
                reason=spec.reason,
                symbol_name="__source_file__",
            )
        ]
    file_text = read_text(path)
    source_file_sha256 = sha256_text(file_text)
    tree = ast.parse(file_text, filename=spec.relative_path)
    assignments = collect_assignments(tree, file_text)
    versions = version_info(assignments)
    items: list[dict[str, Any]] = []

    selected_symbols = set(spec.symbols)
    if spec.include_prompt_constants:
        selected_symbols.update(name for name in assignments if is_prompt_symbol(name))
    if spec.include_schema_constants:
        selected_symbols.update(name for name in assignments if is_schema_symbol(name))

    for symbol_name in sorted(selected_symbols):
        info = assignments.get(symbol_name)
        if info is None:
            items.append(
                build_missing_item(
                    codebase=spec.codebase,
                    relative_path=spec.relative_path,
                    status=spec.status,
                    category=symbol_category(symbol_name),
                    reason=spec.reason,
                    symbol_name=symbol_name,
                    source_file_sha256=source_file_sha256,
                    versions=versions,
                )
            )
            continue
        source_text = (
            info.value
            if isinstance(info.value, str) and symbol_category(symbol_name) == "prompt"
            else info.value_source
        )
        item = build_base_item(
            codebase=spec.codebase,
            relative_path=spec.relative_path,
            status=spec.status,
            category=symbol_category(symbol_name),
            reason=spec.reason,
            symbol_name=symbol_name,
            symbol_type="module_constant",
            source_text=str(source_text),
            source_file_sha256=source_file_sha256,
            versions=versions,
        )
        item.update(
            {
                "line": info.line,
                "end_line": info.end_line,
                "value_kind": info.value_kind,
                "content": source_text if symbol_category(symbol_name) == "prompt" else None,
                "source_excerpt": info.assignment_source,
            }
        )
        items.append(item)

    if spec.include_classes:
        class_summary = summarize_classes(tree, file_text)
        source_text = json.dumps(class_summary, ensure_ascii=False, sort_keys=True)
        item = build_base_item(
            codebase=spec.codebase,
            relative_path=spec.relative_path,
            status=spec.status,
            category="schema",
            reason=spec.reason,
            symbol_name="__classes__",
            symbol_type="class_summary",
            source_text=source_text,
            source_file_sha256=source_file_sha256,
            versions=versions,
        )
        item["schema_summary"] = class_summary
        items.append(item)

    for function_name in spec.functions:
        function_node = find_function(tree, function_name)
        if function_node is None:
            items.append(
                build_missing_item(
                    codebase=spec.codebase,
                    relative_path=spec.relative_path,
                    status=spec.status,
                    category="schema_contract",
                    reason=spec.reason,
                    symbol_name=function_name,
                    source_file_sha256=source_file_sha256,
                    versions=versions,
                )
            )
            continue
        source_excerpt = ast.get_source_segment(file_text, function_node) or ""
        item = build_base_item(
            codebase=spec.codebase,
            relative_path=spec.relative_path,
            status=spec.status,
            category="schema_contract",
            reason=spec.reason,
            symbol_name=function_name,
            symbol_type="function",
            source_text=source_excerpt,
            source_file_sha256=source_file_sha256,
            versions=versions,
        )
        item.update(
            {
                "line": function_node.lineno,
                "end_line": getattr(function_node, "end_lineno", None),
                "source_excerpt": source_excerpt,
            }
        )
        items.append(item)

    return items


def build_missing_item(
    *,
    codebase: str,
    relative_path: str,
    status: str,
    category: str,
    reason: str,
    symbol_name: str,
    source_file_sha256: str | None,
    versions: dict[str, str],
) -> dict[str, Any]:
    return {
        "id": f"{relative_path}::{symbol_name}",
        "codebase": codebase,
        "source_path": relative_path,
        "symbol_name": symbol_name,
        "symbol_type": "missing_symbol",
        "category": category,
        "status": "missing",
        "reason_for_thesis": reason,
        "sha256": None,
        "source_file_sha256": source_file_sha256,
        "prompt_or_schema_versions": versions,
        "warning": "Symbol was requested for export but was not found in the current source file.",
    }


def build_missing_source_item(
    *,
    codebase: str,
    relative_path: str,
    status: str,
    reason: str,
    symbol_name: str,
) -> dict[str, Any]:
    return {
        "id": f"{relative_path}::{symbol_name}",
        "codebase": codebase,
        "source_path": relative_path,
        "symbol_name": symbol_name,
        "symbol_type": "missing_source_file",
        "category": "missing_source",
        "status": "missing",
        "reason_for_thesis": reason,
        "sha256": None,
        "source_file_sha256": None,
        "prompt_or_schema_versions": {},
        "warning": "Source file was planned for export but is absent in the current workspace.",
    }


def find_function(tree: ast.Module, function_name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            return node
    return None


def extract_text_source(spec: TextSource) -> dict[str, Any]:
    assert_safe_source_path(spec.relative_path)
    path = REPO_ROOT / spec.relative_path
    if not path.exists():
        return build_missing_source_item(
            codebase=spec.codebase,
            relative_path=spec.relative_path,
            status=spec.status,
            reason=spec.reason,
            symbol_name=spec.symbol_name or path.name,
        )
    file_text = read_text(path)
    source_file_sha256 = sha256_text(file_text)
    symbol_name = spec.symbol_name or path.name
    item = build_base_item(
        codebase=spec.codebase,
        relative_path=spec.relative_path,
        status=spec.status,
        category=spec.category,
        reason=spec.reason,
        symbol_name=symbol_name,
        symbol_type="text_file",
        source_text=file_text,
        source_file_sha256=source_file_sha256,
        versions={},
    )
    item["content"] = file_text
    return item


def expand_python_globs(globs: list[PythonGlob]) -> list[PythonSource]:
    sources: list[PythonSource] = []
    for spec in globs:
        for path in sorted(REPO_ROOT.glob(spec.pattern)):
            if not path.is_file():
                continue
            relative_path = relative_display(path)
            assert_safe_source_path(relative_path)
            sources.append(
                PythonSource(
                    codebase=spec.codebase,
                    relative_path=relative_path,
                    status=spec.status,
                    reason=spec.reason,
                    include_classes=spec.include_classes,
                    include_prompt_constants=spec.include_prompt_constants,
                    include_schema_constants=spec.include_schema_constants,
                )
            )
    return sources


def expand_text_globs(globs: list[TextGlob]) -> list[TextSource]:
    sources: list[TextSource] = []
    for spec in globs:
        for path in sorted(REPO_ROOT.glob(spec.pattern)):
            if not path.is_file():
                continue
            relative_path = relative_display(path)
            assert_safe_source_path(relative_path)
            sources.append(
                TextSource(
                    codebase=spec.codebase,
                    relative_path=relative_path,
                    status=spec.status,
                    category=spec.category,
                    reason=spec.reason,
                    symbol_name=path.name,
                )
            )
    return sources


PYTHON_SOURCES: list[PythonSource] = [
    PythonSource(
        codebase="matcher/parlementair_v2",
        relative_path="matcher/parlementair_v2/ai_review/prompt_builder.py",
        status="active",
        reason="LLM review prompt and expected output contract for parliamentary uptake candidates.",
        symbols=("PROMPT_VERSION", "SYSTEM_PROMPT", "EXPECTED_OUTPUT_SCHEMA"),
    ),
    PythonSource(
        codebase="matcher/parlementair_v2",
        relative_path="matcher/parlementair_v2/ai_review/schemas.py",
        status="active",
        reason="Pydantic review result schema, enums, and validators for parlementair_v2.",
        include_classes=True,
        include_schema_constants=True,
    ),
    PythonSource(
        codebase="matcher/kabinetsreactie",
        relative_path="matcher/kabinetsreactie/run_vlam_response_judge.py",
        status="active",
        reason="VLAM judgement prompt for deciding whether a document is a real cabinet response.",
        symbols=("PROMPT_VERSION", "SYSTEM_PROMPT"),
        functions=("build_vlam_user_payload", "coerce_vlam_response_output"),
        include_schema_constants=True,
        include_classes=True,
    ),
    PythonSource(
        codebase="matcher/kabinetsreactie",
        relative_path="matcher/kabinetsreactie/run_vlam_response_to_other_advice_chooser.py",
        status="active",
        reason="VLAM target chooser prompt for response-to-other-advice cases.",
        symbols=("PROMPT_VERSION", "SYSTEM_PROMPT"),
        functions=("build_choice_payload", "coerce_chooser_output"),
        include_schema_constants=True,
        include_classes=True,
    ),
    PythonSource(
        codebase="matcher/kabinetsreactie",
        relative_path="matcher/kabinetsreactie/build_chatgpt_kabinetsreactie_search_batches.py",
        status="manual",
        reason="Manual ChatGPT/web-search batch prompt, only relevant when manual validation was used.",
        symbols=("PROMPT_HEADER",),
    ),
    PythonSource(
        codebase="matcher/instellingsbesluit",
        relative_path="matcher/instellingsbesluit/llm_judge.py",
        status="active",
        reason="Main legal-review prompts and JSON contracts for instellingsbesluit discovery and audits.",
        symbols=(
            "CLASSIFIER_PROMPT_VERSION",
            "DISCOVERY_CLASSIFIER_PROMPT_VERSION",
            "KNOWN_COLLEGE_URL_VALIDATION_PROMPT_VERSION",
            "VISIBLE_COLLEGE_METADATA_AUDIT_PROMPT_VERSION",
            "SYSTEM_PROMPT",
            "DOCUMENT_CLASSIFICATION_SYSTEM_PROMPT",
            "DISCOVERY_DOCUMENT_CLASSIFICATION_SYSTEM_PROMPT",
            "KNOWN_COLLEGE_URL_VALIDATION_SYSTEM_PROMPT",
            "VISIBLE_COLLEGE_METADATA_AUDIT_SYSTEM_PROMPT",
            "EXPECTED_OUTPUT_SCHEMA",
            "DOCUMENT_CLASSIFICATION_OUTPUT_SCHEMA",
            "DISCOVERY_DOCUMENT_CLASSIFICATION_OUTPUT_SCHEMA",
            "KNOWN_COLLEGE_URL_VALIDATION_OUTPUT_SCHEMA",
            "VISIBLE_COLLEGE_METADATA_AUDIT_OUTPUT_SCHEMA",
        ),
        include_classes=True,
    ),
    PythonSource(
        codebase="matcher/instellingsbesluit",
        relative_path="matcher/instellingsbesluit/diagnostic_judge.py",
        status="technical",
        reason="Technical diagnostic prompt/schema for explaining pipeline failures.",
        symbols=("PROMPT_PATH", "EXPECTED_DIAGNOSTIC_SCHEMA"),
        include_classes=True,
    ),
    PythonSource(
        codebase="matcher/advies",
        relative_path="matcher/advies/llm_judge.py",
        status="active",
        reason="LLM labelling prompt for deciding whether a candidate is a final advice document.",
        symbols=("LLM_PROMPT_VERSION", "SYSTEM_PROMPT", "JUDGEMENT_CONTRACT", "ALLOWED_LLM_LABELS"),
        include_classes=True,
    ),
    PythonSource(
        codebase="matcher/advies",
        relative_path="matcher/advies/vlam_promotion.py",
        status="active",
        reason="VLAM promotion prompt for selecting main advice documents from candidates.",
        symbols=("VLAM_PROMOTION_PROMPT_VERSION", "SYSTEM_PROMPT"),
        include_classes=True,
    ),
    PythonSource(
        codebase="matcher/advies",
        relative_path="matcher/advies/promotion_policy.py",
        status="active",
        reason="VLAM promotion payload and expected output contract for advice discovery.",
        symbols=("PROMOTION_POLICY_VERSION",),
        functions=("coerce_vlam_promotion_result",),
        include_classes=True,
        include_schema_constants=True,
    ),
    PythonSource(
        codebase="matcher/advies",
        relative_path="matcher/advies/comparative_review.py",
        status="active",
        reason="Comparative review contract for main advice and related-document roles.",
        symbols=("COMPARATIVE_REVIEW_PROMPT_VERSION", "KNOWN_RELATION_ROLES"),
        functions=("_expected_output_contract", "_role_guidance"),
        include_classes=True,
    ),
    PythonSource(
        codebase="matcher/advies",
        relative_path="matcher/advies/export_chatgpt_review.py",
        status="manual",
        reason="Manual ChatGPT review prompt builder, only relevant for manually checked batches.",
        functions=("_write_prompt_file",),
    ),
    PythonSource(
        codebase="matcher/advies",
        relative_path="matcher/advies/export_kandidaten_chatgpt.py",
        status="manual",
        reason="Manual ChatGPT batch prompt for online candidate checks.",
        symbols=("PROMPT_HEADER",),
    ),
    PythonSource(
        codebase="AI adviescollege documenten - classificatie and metadata",
        relative_path="AI agents/AI adviescollege documenten - classificatie and metadata/agents/classificatie_agents/classification_agent/prompt.py",
        status="active",
        reason="Main document classification prompt for advisory-council documents.",
        include_prompt_constants=True,
    ),
    PythonSource(
        codebase="AI adviescollege documenten - classificatie and metadata",
        relative_path="AI agents/AI adviescollege documenten - classificatie and metadata/agents/classificatie_agents/verification_agent/prompt.py",
        status="active",
        reason="Verification and arbiter prompts for classification checks.",
        include_prompt_constants=True,
        functions=("build_arbiter_header",),
    ),
    PythonSource(
        codebase="AI adviescollege documenten - classificatie and metadata",
        relative_path="AI agents/AI adviescollege documenten - classificatie and metadata/agents/classificatie_agents/schemas/classification_schemas.py",
        status="active",
        reason="Pydantic classification and verification schemas.",
        include_classes=True,
        include_schema_constants=True,
    ),
    PythonSource(
        codebase="AI adviescollege documenten - classificatie and metadata",
        relative_path="AI agents/AI adviescollege documenten - classificatie and metadata/agents/document_summary_agent/prompt.py",
        status="active",
        reason="Document-summary prompt used for compact content summaries.",
        include_prompt_constants=True,
    ),
    PythonSource(
        codebase="AI adviescollege documenten - classificatie and metadata",
        relative_path="AI agents/AI adviescollege documenten - classificatie and metadata/agents/document_summary_agent/schema.py",
        status="active",
        reason="Pydantic schema for document summaries.",
        include_classes=True,
    ),
    PythonSource(
        codebase="AI adviescollege documenten - classificatie and metadata",
        relative_path="AI agents/AI adviescollege documenten - classificatie and metadata/agents/metadata_agent/schemas/uniform_schema.py",
        status="active",
        reason="Uniform metadata schema used by metadata agents.",
        include_classes=True,
        include_schema_constants=True,
    ),
    PythonSource(
        codebase="AI adviescollege documenten - classificatie and metadata",
        relative_path="AI agents/AI adviescollege documenten - classificatie and metadata/agents/metadata_agent/schemas/common_schemas.py",
        status="active",
        reason="Shared metadata evidence and theme-code schema definitions.",
        include_classes=True,
        include_schema_constants=True,
        include_prompt_constants=True,
    ),
    PythonSource(
        codebase="AI kabinetsreactie agent",
        relative_path="AI agents/AI kabinetsreactie agent/pipeline/document_pipeline.py",
        status="active",
        reason="V2 stage registry that links each kabinetsreactie prompt to its schema and schema version.",
        symbols=("STAGE_DEFINITIONS",),
    ),
    PythonSource(
        codebase="AI kabinetsreactie agent",
        relative_path="AI agents/AI kabinetsreactie agent/agents/reactie_analyse_agent.py",
        status="legacy",
        reason="Older monolithic kabinetsreactie prompt kept as legacy context next to the V2 staged pipeline.",
        symbols=("REACTIE_ANALYSE_INSTRUCTION",),
        include_classes=True,
    ),
]


PYTHON_GLOBS: list[PythonGlob] = [
    PythonGlob(
        codebase="AI adviescollege documenten - classificatie and metadata",
        pattern="AI agents/AI adviescollege documenten - classificatie and metadata/agents/metadata_agent/*_agent/prompt.py",
        status="active",
        reason="Metadata-agent prompts for the document-type specific metadata extraction.",
        include_prompt_constants=True,
    ),
    PythonGlob(
        codebase="AI adviescollege documenten - classificatie and metadata",
        pattern="AI agents/AI adviescollege documenten - classificatie and metadata/agents/metadata_agent/*_agent/schema.py",
        status="active",
        reason="Metadata-agent Pydantic schemas per document type.",
        include_classes=True,
        include_schema_constants=True,
    ),
    PythonGlob(
        codebase="AI adviescollege documenten - validatie",
        pattern="AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/*/prompt.py",
        status="active",
        reason="Active advice-report extraction prompts for recommendations, problems, links, canonicalization, and report analysis.",
        include_prompt_constants=True,
    ),
    PythonGlob(
        codebase="AI adviescollege documenten - validatie",
        pattern="AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/*/schema.py",
        status="active",
        reason="Pydantic output schemas paired with the advice-report extraction prompts.",
        include_classes=True,
        include_schema_constants=True,
    ),
    PythonGlob(
        codebase="AI kabinetsreactie agent",
        pattern="AI agents/AI kabinetsreactie agent/schemas/stage_*.py",
        status="active",
        reason="Stage-level Pydantic schemas for the V2 kabinetsreactie pipeline.",
        include_classes=True,
        include_schema_constants=True,
    ),
]


TEXT_SOURCES: list[TextSource] = [
    TextSource(
        codebase="matcher/instellingsbesluit",
        relative_path="matcher/instellingsbesluit/prompts/pipeline_error_explainer_prompt.md",
        status="technical",
        category="technical_prompt",
        reason="Technical prompt for explaining and improving failed instellingsbesluit runs.",
    ),
]


TEXT_GLOBS: list[TextGlob] = [
    TextGlob(
        codebase="AI adviescollege documenten - classificatie and metadata",
        pattern="AI agents/AI adviescollege documenten - classificatie and metadata/agents/classificatie_agents/sub_agents/classification_prompts/*.txt",
        status="active",
        category="prompt",
        reason="Domain-specific classification subprompt used by the verification waterfall.",
    ),
    TextGlob(
        codebase="AI kabinetsreactie agent",
        pattern="AI agents/AI kabinetsreactie agent/agents/*.txt",
        status="active",
        category="prompt",
        reason="V2 kabinetsreactie stage prompt text file.",
    ),
]


EXTRA_SCHEMA_SOURCES: list[PythonSource] = [
    PythonSource(
        codebase="AI adviescollege documenten - validatie",
        relative_path="AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/schemas/canonical_schemas.py",
        status="active",
        reason="Canonical recommendation, problem-definition, and policy-logic overlay schemas.",
        include_classes=True,
        include_schema_constants=True,
    ),
    PythonSource(
        codebase="AI adviescollege documenten - validatie",
        relative_path="AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/schemas/final_result.py",
        status="active",
        reason="Final advice-report extraction result schema used downstream in the thesis pipeline.",
        include_classes=True,
        include_schema_constants=True,
    ),
]


def collect_items() -> list[dict[str, Any]]:
    python_sources = (
        PYTHON_SOURCES
        + EXTRA_SCHEMA_SOURCES
        + expand_python_globs(PYTHON_GLOBS)
    )
    text_sources = TEXT_SOURCES + expand_text_globs(TEXT_GLOBS)

    items: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for spec in python_sources:
        for item in extract_python_source(spec):
            if item["id"] in seen_ids:
                continue
            seen_ids.add(item["id"])
            items.append(item)
    for spec in text_sources:
        item = extract_text_source(spec)
        if item["id"] in seen_ids:
            continue
        seen_ids.add(item["id"])
        items.append(item)
    return sorted(items, key=lambda item: (item["codebase"], item["source_path"], item["symbol_name"]))


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def render_markdown(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Thesis Prompt- En Schema-Export")
    lines.append("")
    lines.append(f"Gegenereerd: `{payload['generated_at']}`")
    lines.append(f"Exportversie: `{payload['export_version']}`")
    lines.append("")
    lines.append("Deze export bevat volledige promptteksten en compacte schema-uitleg.")
    lines.append("Het script leest alleen bronbestanden en gebruikt geen LLM, API of database.")
    lines.append("")
    lines.append("## Samenvatting")
    lines.append("")
    lines.append(f"- Items totaal: `{len(payload['items'])}`")
    lines.append(f"- Codebases: `{len(payload['counts_by_codebase'])}`")
    lines.append("- Uitgesloten: `.env`, caches, bestaande outputmappen en debug/runtime-artifacts.")
    lines.append("")
    lines.append("### Aantallen Per Codebase")
    lines.append("")
    for codebase, count in payload["counts_by_codebase"].items():
        lines.append(f"- `{codebase}`: `{count}`")
    lines.append("")

    current_codebase: str | None = None
    for item in payload["items"]:
        if item["codebase"] != current_codebase:
            current_codebase = item["codebase"]
            lines.append(f"## {current_codebase}")
            lines.append("")
        lines.append(f"### `{item['symbol_name']}`")
        lines.append("")
        lines.append(f"- Bron: `{item['source_path']}`")
        lines.append(f"- Type: `{item['symbol_type']}`")
        lines.append(f"- Categorie: `{item['category']}`")
        lines.append(f"- Status: `{item['status']}`")
        lines.append(f"- SHA256: `{item.get('sha256')}`")
        lines.append(f"- Thesis-relevantie: {item['reason_for_thesis']}")
        versions = item.get("prompt_or_schema_versions") or {}
        if versions:
            lines.append("- Versies:")
            for name, value in versions.items():
                lines.append(f"  - `{name}`: `{value}`")
        if item.get("warning"):
            lines.append(f"- Waarschuwing: {item['warning']}")
        lines.append("")

        if item.get("content") is not None:
            lines.append(fenced_block(str(item["content"]), "text"))
            lines.append("")
        elif item.get("schema_summary") is not None:
            lines.extend(render_schema_summary(item["schema_summary"]))
            lines.append("")
        elif item.get("source_excerpt") is not None:
            lines.append(fenced_block(str(item["source_excerpt"]), "python"))
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


MATCHER_ROOTS = {
    "matcher/instellingsbesluit": "matchers/01_instellingsmatcher",
    "matcher/advies": "matchers/02_adviesmatcher",
    "matcher/kabinetsreactie": "matchers/03_kabinetsreactie_matcher",
    "matcher/parlementair_v2": "matchers/04_parlementaire_matcher",
}


ADVIESEXTRACTIE_AGENT_FOLDERS = {
    "adviesrapport_gate": "agent_01_adviesrapport_gate",
    "aanbeveling_recall": "agent_02_aanbeveling_recall",
    "aanbeveling_precision": "agent_03_aanbeveling_precision",
    "probleem_definitie_recall": "agent_04_probleemdefinitie_recall",
    "probleem_definitie_precision": "agent_05_probleemdefinitie_precision",
    "probleem_definitie_analyse": "agent_06_probleemdefinitie_analyse",
    "verwijzing_extractie": "agent_07_verwijzingen",
    "beleidslogica_agent": "agent_08_beleidslogica",
    "advies_canonicalizer": "agent_09_canonicalizer",
    "rapport_analyse": "agent_10_rapport_analyse",
}


METADATA_AGENT_FOLDERS = {
    "aanvraag_agent": "aanvraag_metadata",
    "brief_agent": "brief_metadata",
    "kabinetsreactie_agent": "kabinetsreactie_metadata",
    "legacy_agent": "legacy_metadata",
    "rapport_agent": "rapport_metadata",
}


KABINETSREACTIE_STAGE_FOLDERS = {
    "01": "stage_01_segmentatie",
    "02": "stage_02_stramien",
    "03": "stage_03_reverse_recall",
    "04": "stage_04_candidate_pairs",
    "05": "stage_05_semantische_match",
    "06": "stage_06_positie_opvolging",
    "06a": "stage_06a_positie",
    "06b": "stage_06b_context",
    "07": "stage_07_voorlopige_labels",
    "08": "stage_08_audit",
    "09": "stage_09_eindanalyse",
}


def slugify(value: str) -> str:
    cleaned: list[str] = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in {"_", "-"}:
            cleaned.append("_")
        else:
            cleaned.append("_")
    slug = "".join(cleaned).strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug or "item"


def structured_path_for_item(item: dict[str, Any]) -> Path:
    codebase = item["codebase"]
    source_path = item["source_path"]

    if codebase in MATCHER_ROOTS:
        return matcher_structured_path(item, MATCHER_ROOTS[codebase])
    if codebase == "AI adviescollege documenten - classificatie and metadata":
        return classification_metadata_structured_path(item)
    if codebase == "AI adviescollege documenten - validatie":
        return adviesextractie_structured_path(item)
    if codebase == "AI kabinetsreactie agent":
        return ai_kabinetsreactie_structured_path(item)

    return Path("overig") / slugify(codebase) / default_item_filename(item)


def matcher_structured_path(item: dict[str, Any], root: str) -> Path:
    if item["status"] == "missing":
        return Path(root) / "legacy" / "missing_sources.md"
    if item["status"] == "manual":
        return Path(root) / "handmatige_controle" / default_item_filename(item)
    if item["status"] == "technical":
        return Path(root) / "technische_diagnose" / default_item_filename(item)
    if item["category"] == "version":
        return Path(root) / "versions.md"
    if item["category"] == "prompt":
        return Path(root) / "prompts" / default_item_filename(item)
    if item["category"] in {"schema", "schema_contract"}:
        return Path(root) / "schemas" / default_item_filename(item)
    return Path(root) / "contracten" / default_item_filename(item)


def classification_metadata_structured_path(item: dict[str, Any]) -> Path:
    source_path = item["source_path"]
    root = Path("ai_pipeline")

    if "/metadata_agent/" in source_path:
        return metadata_structured_path(item)

    if "/classification_agent/" in source_path:
        filename = "prompt.md" if item["category"] == "prompt" else default_item_filename(item)
        return root / "01_classificatie" / "agent_01_hoofdclassificatie" / filename
    if "/verification_agent/" in source_path:
        filename = "prompt.md" if item["category"] == "prompt" else default_item_filename(item)
        if item["symbol_type"] == "function":
            filename = f"{slugify(item['symbol_name'])}.md"
        return root / "01_classificatie" / "agent_02_verificatie" / filename
    if "/classification_prompts/" in source_path:
        return root / "01_classificatie" / "agent_03_subclassificatie" / "prompts" / source_filename_as_md(source_path)
    if source_path.endswith("classification_schemas.py"):
        return root / "01_classificatie" / "agent_03_subclassificatie" / "schema.md"
    if "/document_summary_agent/" in source_path:
        filename = "prompt.md" if item["category"] == "prompt" else "schema.md"
        return root / "01_classificatie" / "agent_04_document_summary" / filename

    return root / "01_classificatie" / default_item_filename(item)


def metadata_structured_path(item: dict[str, Any]) -> Path:
    source_path = item["source_path"]
    root = Path("ai_pipeline") / "02_metadata"
    parts = Path(source_path).parts

    for folder_name, output_folder in METADATA_AGENT_FOLDERS.items():
        if folder_name in parts:
            filename = "prompt.md" if item["category"] == "prompt" else "schema.md"
            return root / output_folder / filename

    if source_path.endswith("uniform_schema.py"):
        return root / "uniforme_metadata" / "schema.md"
    if source_path.endswith("common_schemas.py"):
        if item["category"] == "prompt":
            return root / "gedeelde_metadata_contracten" / "instructies.md"
        return root / "gedeelde_metadata_contracten" / "schema.md"
    return root / default_item_filename(item)


def adviesextractie_structured_path(item: dict[str, Any]) -> Path:
    source_path = item["source_path"]
    root = Path("ai_pipeline") / "03_adviesextractie"
    parts = Path(source_path).parts

    for agent_name, folder_name in ADVIESEXTRACTIE_AGENT_FOLDERS.items():
        if agent_name in parts:
            filename = "prompt.md" if item["category"] == "prompt" else "schema.md"
            return root / folder_name / filename

    if source_path.endswith("canonical_schemas.py"):
        return root / "finale_output" / "canonical_schema.md"
    if source_path.endswith("final_result.py"):
        return root / "finale_output" / "final_result_schema.md"
    return root / default_item_filename(item)


def ai_kabinetsreactie_structured_path(item: dict[str, Any]) -> Path:
    source_path = item["source_path"]
    root = Path("ai_pipeline") / "04_kabinetsreactie_agent"

    if item["status"] == "missing":
        return root / "legacy" / "missing_sources.md"
    if source_path.endswith("document_pipeline.py"):
        return root / "stage_registry.md"
    if "/agents/" in source_path and source_path.endswith(".txt"):
        return root / stage_folder_from_name(Path(source_path).name) / "prompt.md"
    if "/schemas/" in source_path and Path(source_path).name.startswith("stage_"):
        if Path(source_path).name == "stage_06_enums.py":
            return root / "shared" / "stage_06_enums_schema.md"
        return root / stage_folder_from_name(Path(source_path).stem.replace("stage_", "")) / "schema.md"
    return root / default_item_filename(item)


def stage_folder_from_name(value: str) -> Path:
    stem = Path(value).stem
    if stem.startswith("stage_"):
        stem = stem.removeprefix("stage_")
    stage_key = stem.split("_", 1)[0]
    return Path(KABINETSREACTIE_STAGE_FOLDERS.get(stage_key, f"stage_{slugify(stage_key)}"))


def source_filename_as_md(source_path: str) -> str:
    return f"{slugify(Path(source_path).stem)}.md"


def default_item_filename(item: dict[str, Any]) -> str:
    source_stem = slugify(Path(item["source_path"]).stem)
    symbol = slugify(item["symbol_name"])
    if item["symbol_name"] == "__classes__":
        return f"{source_stem}_schema.md"
    return f"{source_stem}_{symbol}.md"


def collision_safe_path(base_path: Path, item: dict[str, Any]) -> Path:
    base_stem = slugify(base_path.stem)
    source_stem = slugify(Path(item["source_path"]).stem)
    suffix = slugify(str(item["symbol_name"]))
    if item["symbol_name"] == "__classes__":
        suffix = "schema"
    parts = [base_stem]
    if source_stem != base_stem:
        parts.append(source_stem)
    parts.append(suffix)
    return base_path.with_name(f"{'_'.join(parts)}{base_path.suffix}")


def reset_structured_dir() -> None:
    target = STRUCTURED_DIR.resolve()
    export_root = EXPORT_DIR.resolve()
    if target == export_root or export_root not in target.parents:
        raise ValueError(f"Unsafe structured export target: {target}")
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)


def assign_structured_paths(items: list[dict[str, Any]]) -> None:
    proposed_paths: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        proposed_path = structured_path_for_item(item)
        proposed_paths.setdefault(proposed_path.as_posix(), []).append(item)

    final_paths: set[str] = set()
    for proposed_path_text, proposed_items in proposed_paths.items():
        proposed_path = Path(proposed_path_text)
        for item in proposed_items:
            final_path = proposed_path
            if len(proposed_items) > 1:
                final_path = collision_safe_path(proposed_path, item)
            structured_path = (STRUCTURED_DIR / final_path).relative_to(REPO_ROOT).as_posix()
            if structured_path in final_paths:
                raise ValueError(f"Structured export path collision: {structured_path}")
            final_paths.add(structured_path)
            item["structured_path"] = structured_path


def write_structured_export(payload: dict[str, Any]) -> None:
    reset_structured_dir()
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in payload["items"]:
        grouped.setdefault(item["structured_path"], []).append(item)

    for relative_path, items in sorted(grouped.items()):
        output_path = REPO_ROOT / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_structured_item_file(output_path, items), encoding="utf-8")

    write_component_readmes(payload, grouped)
    write_top_level_readmes()
    STRUCTURED_README_MD.write_text(render_structured_readme(payload), encoding="utf-8")
    STRUCTURED_INDEX_MD.write_text(render_structured_index(payload, grouped), encoding="utf-8")
    STRUCTURED_MANIFEST_JSON.write_text(
        json.dumps(
            {
                "export_version": payload["export_version"],
                "generated_at": payload["generated_at"],
                "item_count": len(payload["items"]),
                "counts_by_codebase": payload["counts_by_codebase"],
                "counts_by_status": payload["counts_by_status"],
                "files": {
                    path: [item["id"] for item in items]
                    for path, items in sorted(grouped.items())
                },
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def render_structured_item_file(output_path: Path, items: list[dict[str, Any]]) -> str:
    title = output_path.stem.replace("_", " ").title()
    lines = [f"# {title}", ""]
    for item in items:
        lines.append(f"## `{item['symbol_name']}`")
        lines.append("")
        lines.append(f"- Bron: `{item['source_path']}`")
        lines.append(f"- Codebase: `{item['codebase']}`")
        lines.append(f"- Type: `{item['symbol_type']}`")
        lines.append(f"- Categorie: `{item['category']}`")
        lines.append(f"- Status: `{item['status']}`")
        lines.append(f"- SHA256: `{item.get('sha256')}`")
        lines.append(f"- Thesis-relevantie: {item['reason_for_thesis']}")
        versions = item.get("prompt_or_schema_versions") or {}
        if versions:
            lines.append("- Versies:")
            for name, value in versions.items():
                lines.append(f"  - `{name}`: `{value}`")
        if item.get("warning"):
            lines.append(f"- Waarschuwing: {item['warning']}")
        lines.append("")
        if item.get("content") is not None:
            lines.append(fenced_block(str(item["content"]), "text"))
        elif item.get("schema_summary") is not None:
            lines.extend(render_schema_summary(item["schema_summary"]))
        elif item.get("source_excerpt") is not None:
            lines.append(fenced_block(str(item["source_excerpt"]), "python"))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_component_readmes(payload: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]) -> None:
    component_dirs: dict[Path, list[Path]] = {}
    for relative_path in grouped:
        path = Path(relative_path)
        try:
            local = path.relative_to(STRUCTURED_DIR.relative_to(REPO_ROOT))
        except ValueError:
            continue
        if len(local.parts) < 2:
            continue
        component_dir = STRUCTURED_DIR / local.parts[0] / local.parts[1]
        component_dirs.setdefault(component_dir, []).append(path)

    for component_dir, files in component_dirs.items():
        component_dir.mkdir(parents=True, exist_ok=True)
        relative_files = sorted(
            path.relative_to(component_dir.relative_to(REPO_ROOT)).as_posix()
            for path in files
            if path.name != "README.md"
        )
        title = component_dir.name.replace("_", " ").title()
        lines = [
            f"# {title}",
            "",
            "Leesbare deel-export voor prompts en schema's. Deze map is bedoeld om vanaf GitHub direct te openen.",
            "",
            "## Bestanden",
            "",
        ]
        for relative_file in relative_files:
            lines.append(f"- [{relative_file}]({relative_file})")
        component_dir.joinpath("README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_top_level_readmes() -> None:
    readmes = {
        STRUCTURED_DIR / "matchers" / "README.md": [
            "# Matchers",
            "",
            "Losse prompt- en schema-export per matcher.",
            "",
            "- [Instellingsmatcher](01_instellingsmatcher/)",
            "- [Adviesmatcher](02_adviesmatcher/)",
            "- [Kabinetsreactie matcher](03_kabinetsreactie_matcher/)",
            "- [Parlementaire matcher](04_parlementaire_matcher/)",
        ],
        STRUCTURED_DIR / "ai_pipeline" / "README.md": [
            "# AI Pipeline",
            "",
            "Losse prompt- en schema-export per AI-pipelineonderdeel.",
            "",
            "- [Classificatie](01_classificatie/)",
            "- [Metadata](02_metadata/)",
            "- [Adviesextractie](03_adviesextractie/)",
            "- [Kabinetsreactie agent](04_kabinetsreactie_agent/)",
        ],
    }
    for path, lines in readmes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def render_structured_readme(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Thesisexport Prompts En Schema's",
            "",
            "Deze map is de leesbare GitHub-bijlage bij de thesis.",
            "Gebruik de links hieronder om per onderdeel de losse prompt- en schema-bestanden te openen.",
            "",
            "## Hoofdmappen",
            "",
            "- [Matchers](matchers/)",
            "- [AI pipeline](ai_pipeline/)",
            "- [Volledige bestandsindex](INDEX.md)",
            "- [Machineleesbare manifest](manifest.json)",
            "",
            "## Structuur",
            "",
            "```text",
            "structured/",
            "  matchers/",
            "    01_instellingsmatcher/",
            "    02_adviesmatcher/",
            "    03_kabinetsreactie_matcher/",
            "    04_parlementaire_matcher/",
            "  ai_pipeline/",
            "    01_classificatie/",
            "    02_metadata/",
            "    03_adviesextractie/",
            "    04_kabinetsreactie_agent/",
            "```",
            "",
            "## Aantallen",
            "",
            f"- Items totaal: `{len(payload['items'])}`",
            f"- Actief: `{payload['counts_by_status'].get('active', 0)}`",
            f"- Handmatig: `{payload['counts_by_status'].get('manual', 0)}`",
            f"- Technisch: `{payload['counts_by_status'].get('technical', 0)}`",
            f"- Ontbrekende legacy-bron: `{payload['counts_by_status'].get('missing', 0)}`",
            "",
            "De grote bestanden een map hoger blijven bestaan voor volledige controle:",
            "",
            "- `prompts_schemas_export.md`",
            "- `prompts_schemas_export.json`",
        ]
    ).rstrip() + "\n"


def render_structured_index(payload: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# Gestructureerde Prompt- En Schema-Export",
        "",
        f"Gegenereerd: `{payload['generated_at']}`",
        f"Items totaal: `{len(payload['items'])}`",
        "",
        "Gebruik `README.md` als GitHub-ingang. Dit bestand is de volledige lijst met losse exportbestanden.",
        "",
        "```text",
        "structured/",
        "  matchers/",
        "    01_instellingsmatcher/",
        "    02_adviesmatcher/",
        "    03_kabinetsreactie_matcher/",
        "    04_parlementaire_matcher/",
        "  ai_pipeline/",
        "    01_classificatie/",
        "    02_metadata/",
        "    03_adviesextractie/",
        "    04_kabinetsreactie_agent/",
        "```",
        "",
        "## Aantallen Per Codebase",
        "",
    ]
    for codebase, count in payload["counts_by_codebase"].items():
        lines.append(f"- `{codebase}`: `{count}`")
    lines.append("")
    lines.append("## Bestanden")
    lines.append("")
    for path, items in sorted(grouped.items()):
        display_path = Path(path).relative_to(STRUCTURED_DIR.relative_to(REPO_ROOT)).as_posix()
        label = ", ".join(item["symbol_name"] for item in items[:3])
        if len(items) > 3:
            label += f" (+{len(items) - 3})"
        lines.append(f"- [{display_path}]({display_path}) - {label}")
    return "\n".join(lines).rstrip() + "\n"


def render_schema_summary(schema_summary: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    if not schema_summary:
        lines.append("_Geen klassen gevonden in dit schema-bestand._")
        return lines
    for class_info in schema_summary:
        bases = ", ".join(class_info.get("bases") or [])
        lines.append(f"- Klasse `{class_info['name']}` op regel `{class_info['line']}`")
        if bases:
            lines.append(f"  - Bases: `{bases}`")
        if class_info.get("docstring"):
            doc = str(class_info["docstring"]).strip().replace("\n", " ")
            lines.append(f"  - Docstring: {doc}")
        fields = class_info.get("fields") or []
        if fields:
            field_text = ", ".join(
                f"{field['name']}: {field.get('annotation') or '?'}"
                for field in fields[:40]
            )
            suffix = "" if len(fields) <= 40 else f" ... (+{len(fields) - 40} velden)"
            lines.append(f"  - Velden: {field_text}{suffix}")
        enum_values = class_info.get("enum_values") or []
        if enum_values:
            enum_text = ", ".join(
                f"{entry['name']}={entry.get('value')!r}"
                for entry in enum_values[:40]
            )
            suffix = "" if len(enum_values) <= 40 else f" ... (+{len(enum_values) - 40} waarden)"
            lines.append(f"  - Enum/constanten: {enum_text}{suffix}")
        validators = class_info.get("validators") or []
        if validators:
            validator_text = ", ".join(
                f"{entry['name']}@{entry['line']}"
                for entry in validators[:40]
            )
            suffix = "" if len(validators) <= 40 else f" ... (+{len(validators) - 40} validators)"
            lines.append(f"  - Validators/normalizers: {validator_text}{suffix}")
    return lines


def fenced_block(text: str, language: str) -> str:
    fence = "```"
    while fence in text:
        fence += "`"
    return f"{fence}{language}\n{text.rstrip()}\n{fence}"


def validate_payload(payload: dict[str, Any]) -> None:
    items = payload["items"]
    if not items:
        raise ValueError("Export has no items.")
    source_paths = [item["source_path"] for item in items]
    for source_path in source_paths:
        assert_safe_source_path(source_path)

    required_fragments = {
        "matcher/parlementair_v2/ai_review/prompt_builder.py::SYSTEM_PROMPT": False,
        "matcher/kabinetsreactie/run_vlam_response_judge.py::SYSTEM_PROMPT": False,
        "matcher/kabinetsreactie/run_vlam_response_to_other_advice_chooser.py::SYSTEM_PROMPT": False,
        "AI agents/AI adviescollege documenten - validatie/agents/advies_rapport_extractie_agent/agents/advies_canonicalizer/prompt.py::ADVIES_CANONICALIZER_INSTRUCTION": False,
        "AI agents/AI kabinetsreactie agent/agents/01_kabinetsreactie_segmentatie_agent_instruction.txt::01_kabinetsreactie_segmentatie_agent_instruction.txt": False,
        "AI agents/AI kabinetsreactie agent/agents/09_eindanalyse_agent_instruction.txt.txt::09_eindanalyse_agent_instruction.txt.txt": False,
    }
    ids = {item["id"] for item in items}
    missing = [item_id for item_id in required_fragments if item_id not in ids]
    if missing:
        raise ValueError("Required export items missing: " + ", ".join(missing))


def main() -> None:
    items = collect_items()
    assign_structured_paths(items)
    payload = {
        "export_version": EXPORT_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(REPO_ROOT),
        "outputs": {
            "markdown": relative_display(OUTPUT_MD),
            "json": relative_display(OUTPUT_JSON),
            "structured_index": relative_display(STRUCTURED_INDEX_MD),
            "structured_manifest": relative_display(STRUCTURED_MANIFEST_JSON),
        },
        "counts_by_codebase": count_by(items, "codebase"),
        "counts_by_category": count_by(items, "category"),
        "counts_by_status": count_by(items, "status"),
        "items": items,
    }
    validate_payload(payload)
    write_structured_export(payload)
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload), encoding="utf-8")
    print(f"Wrote {relative_display(STRUCTURED_INDEX_MD)}")
    print(f"Wrote {relative_display(STRUCTURED_MANIFEST_JSON)}")
    print(f"Wrote {relative_display(OUTPUT_MD)}")
    print(f"Wrote {relative_display(OUTPUT_JSON)}")
    print(f"Exported {len(items)} items across {len(payload['counts_by_codebase'])} codebases.")


if __name__ == "__main__":
    main()

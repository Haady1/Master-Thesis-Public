# Build Arbiter Header

## `build_arbiter_header`

- Bron: `AI agents/AI adviescollege documenten - classificatie and metadata/agents/classificatie_agents/verification_agent/prompt.py`
- Codebase: `AI adviescollege documenten - classificatie and metadata`
- Type: `function`
- Categorie: `schema_contract`
- Status: `active`
- SHA256: `93593f0faad4fefe999ee75c83637346d01494b016ba3a5d912669361205a16a`
- Thesis-relevantie: Verification and arbiter prompts for classification checks.

```python
def build_arbiter_header(main_category: str, second_main_category: str) -> str:
    """Build the arbiter framing header for dual-domain verification."""
    result = ARBITER_FRAMING_TEMPLATE.replace(
        "{main_category}", main_category
    ).replace(
        "{second_main_category}", second_main_category
    ).replace(
        "{BEKENDE_ADVIESCOLLEGES_PLACEHOLDER}",
        format_bekende_adviescolleges_xml()
    )
    return result
```

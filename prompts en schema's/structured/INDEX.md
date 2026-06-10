# Gestructureerde Prompt- En Schema-Export

Gegenereerd: `2026-06-05T22:26:22.503903+00:00`
Items totaal: `138`

Gebruik `README.md` als GitHub-ingang. Dit bestand is de volledige lijst met losse exportbestanden.

```text
structured/
  matchers/
    01_instellingsmatcher/
    02_adviesmatcher/
    03_kabinetsreactie_matcher/
    04_parlementaire_matcher/
  ai_pipeline/
    01_classificatie/
    02_metadata/
    03_adviesextractie/
    04_kabinetsreactie_agent/
```

## Aantallen Per Codebase

- `AI adviescollege documenten - classificatie and metadata`: `35`
- `AI adviescollege documenten - validatie`: `22`
- `AI kabinetsreactie agent`: `25`
- `matcher/advies`: `18`
- `matcher/instellingsbesluit`: `19`
- `matcher/kabinetsreactie`: `14`
- `matcher/parlementair_v2`: `5`

## Bestanden

- [ai_pipeline/01_classificatie/agent_01_hoofdclassificatie/prompt.md](ai_pipeline/01_classificatie/agent_01_hoofdclassificatie/prompt.md) - CLASSIFICATION_INSTRUCTION
- [ai_pipeline/01_classificatie/agent_02_verificatie/build_arbiter_header.md](ai_pipeline/01_classificatie/agent_02_verificatie/build_arbiter_header.md) - build_arbiter_header
- [ai_pipeline/01_classificatie/agent_02_verificatie/prompt_arbiter_framing_template.md](ai_pipeline/01_classificatie/agent_02_verificatie/prompt_arbiter_framing_template.md) - ARBITER_FRAMING_TEMPLATE
- [ai_pipeline/01_classificatie/agent_02_verificatie/prompt_verification_framing.md](ai_pipeline/01_classificatie/agent_02_verificatie/prompt_verification_framing.md) - VERIFICATION_FRAMING
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/bestuur_governance.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/bestuur_governance.md) - BESTUUR_GOVERNANCE.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/brief_administratief.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/brief_administratief.md) - BRIEF_ADMINISTRATIEF.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/brief_inhoudelijk.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/brief_inhoudelijk.md) - BRIEF_INHOUDELIJK.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/communicatie.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/communicatie.md) - COMMUNICATIE.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/correspondentie_inkomend.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/correspondentie_inkomend.md) - CORRESPONDENTIE_INKOMEND.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/instrumenten.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/instrumenten.md) - INSTRUMENTEN.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/interne_stukken.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/interne_stukken.md) - INTERNE_STUKKEN.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/juridisch_hr.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/juridisch_hr.md) - JURIDISCH_HR.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/rapport_advies.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/rapport_advies.md) - RAPPORT_ADVIES.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/rapport_onderzoek.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/rapport_onderzoek.md) - RAPPORT_ONDERZOEK.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/rapport_overig.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/rapport_overig.md) - RAPPORT_OVERIG.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/varia.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/varia.md) - VARIA.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/vergaderdocumenten.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/prompts/vergaderdocumenten.md) - VERGADERDOCUMENTEN.txt
- [ai_pipeline/01_classificatie/agent_03_subclassificatie/schema.md](ai_pipeline/01_classificatie/agent_03_subclassificatie/schema.md) - __classes__
- [ai_pipeline/01_classificatie/agent_04_document_summary/prompt.md](ai_pipeline/01_classificatie/agent_04_document_summary/prompt.md) - DOCUMENT_SUMMARY_INSTRUCTION
- [ai_pipeline/01_classificatie/agent_04_document_summary/schema.md](ai_pipeline/01_classificatie/agent_04_document_summary/schema.md) - __classes__
- [ai_pipeline/02_metadata/aanvraag_metadata/prompt.md](ai_pipeline/02_metadata/aanvraag_metadata/prompt.md) - AANVRAAG_AANKONDIGING_METADATA_INSTRUCTION
- [ai_pipeline/02_metadata/aanvraag_metadata/schema.md](ai_pipeline/02_metadata/aanvraag_metadata/schema.md) - __classes__
- [ai_pipeline/02_metadata/brief_metadata/prompt.md](ai_pipeline/02_metadata/brief_metadata/prompt.md) - BRIEF_METADATA_INSTRUCTION
- [ai_pipeline/02_metadata/brief_metadata/schema.md](ai_pipeline/02_metadata/brief_metadata/schema.md) - __classes__
- [ai_pipeline/02_metadata/gedeelde_metadata_contracten/instructies_common_schemas_self_check_instruction.md](ai_pipeline/02_metadata/gedeelde_metadata_contracten/instructies_common_schemas_self_check_instruction.md) - SELF_CHECK_INSTRUCTION
- [ai_pipeline/02_metadata/gedeelde_metadata_contracten/instructies_common_schemas_thema_codes_instruction.md](ai_pipeline/02_metadata/gedeelde_metadata_contracten/instructies_common_schemas_thema_codes_instruction.md) - THEMA_CODES_INSTRUCTION
- [ai_pipeline/02_metadata/gedeelde_metadata_contracten/instructies_common_schemas_tracking_keywords_instruction.md](ai_pipeline/02_metadata/gedeelde_metadata_contracten/instructies_common_schemas_tracking_keywords_instruction.md) - TRACKING_KEYWORDS_INSTRUCTION
- [ai_pipeline/02_metadata/gedeelde_metadata_contracten/schema.md](ai_pipeline/02_metadata/gedeelde_metadata_contracten/schema.md) - __classes__
- [ai_pipeline/02_metadata/kabinetsreactie_metadata/prompt.md](ai_pipeline/02_metadata/kabinetsreactie_metadata/prompt.md) - KABINETSREACTIE_METADATA_INSTRUCTION
- [ai_pipeline/02_metadata/kabinetsreactie_metadata/schema.md](ai_pipeline/02_metadata/kabinetsreactie_metadata/schema.md) - __classes__
- [ai_pipeline/02_metadata/legacy_metadata/prompt.md](ai_pipeline/02_metadata/legacy_metadata/prompt.md) - LEGACY_METADATA_INSTRUCTION
- [ai_pipeline/02_metadata/legacy_metadata/schema.md](ai_pipeline/02_metadata/legacy_metadata/schema.md) - __classes__
- [ai_pipeline/02_metadata/rapport_metadata/prompt.md](ai_pipeline/02_metadata/rapport_metadata/prompt.md) - RAPPORT_METADATA_INSTRUCTION
- [ai_pipeline/02_metadata/rapport_metadata/schema.md](ai_pipeline/02_metadata/rapport_metadata/schema.md) - __classes__
- [ai_pipeline/02_metadata/uniforme_metadata/schema.md](ai_pipeline/02_metadata/uniforme_metadata/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_01_adviesrapport_gate/prompt.md](ai_pipeline/03_adviesextractie/agent_01_adviesrapport_gate/prompt.md) - ADVIESRAPPORT_GATE_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_01_adviesrapport_gate/schema.md](ai_pipeline/03_adviesextractie/agent_01_adviesrapport_gate/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_02_aanbeveling_recall/prompt.md](ai_pipeline/03_adviesextractie/agent_02_aanbeveling_recall/prompt.md) - AANBEVELING_RECALL_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_02_aanbeveling_recall/schema.md](ai_pipeline/03_adviesextractie/agent_02_aanbeveling_recall/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_03_aanbeveling_precision/prompt.md](ai_pipeline/03_adviesextractie/agent_03_aanbeveling_precision/prompt.md) - AANBEVELING_PRECISION_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_03_aanbeveling_precision/schema.md](ai_pipeline/03_adviesextractie/agent_03_aanbeveling_precision/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_04_probleemdefinitie_recall/prompt.md](ai_pipeline/03_adviesextractie/agent_04_probleemdefinitie_recall/prompt.md) - PROBLEEM_DEFINITIE_RECALL_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_04_probleemdefinitie_recall/schema.md](ai_pipeline/03_adviesextractie/agent_04_probleemdefinitie_recall/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_05_probleemdefinitie_precision/prompt.md](ai_pipeline/03_adviesextractie/agent_05_probleemdefinitie_precision/prompt.md) - PROBLEEM_DEFINITIE_PRECISION_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_05_probleemdefinitie_precision/schema.md](ai_pipeline/03_adviesextractie/agent_05_probleemdefinitie_precision/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_06_probleemdefinitie_analyse/prompt.md](ai_pipeline/03_adviesextractie/agent_06_probleemdefinitie_analyse/prompt.md) - PROBLEEM_DEFINITIE_ANALYSE_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_06_probleemdefinitie_analyse/schema.md](ai_pipeline/03_adviesextractie/agent_06_probleemdefinitie_analyse/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_07_verwijzingen/prompt.md](ai_pipeline/03_adviesextractie/agent_07_verwijzingen/prompt.md) - VERWIJZINGEN_EXTRACTIE_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_07_verwijzingen/schema.md](ai_pipeline/03_adviesextractie/agent_07_verwijzingen/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_08_beleidslogica/prompt.md](ai_pipeline/03_adviesextractie/agent_08_beleidslogica/prompt.md) - BELEIDSLOGICA_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_08_beleidslogica/schema.md](ai_pipeline/03_adviesextractie/agent_08_beleidslogica/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_09_canonicalizer/prompt.md](ai_pipeline/03_adviesextractie/agent_09_canonicalizer/prompt.md) - ADVIES_CANONICALIZER_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_09_canonicalizer/schema.md](ai_pipeline/03_adviesextractie/agent_09_canonicalizer/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/agent_10_rapport_analyse/prompt.md](ai_pipeline/03_adviesextractie/agent_10_rapport_analyse/prompt.md) - RAPPORT_ANALYSE_INSTRUCTION
- [ai_pipeline/03_adviesextractie/agent_10_rapport_analyse/schema.md](ai_pipeline/03_adviesextractie/agent_10_rapport_analyse/schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/finale_output/canonical_schema.md](ai_pipeline/03_adviesextractie/finale_output/canonical_schema.md) - __classes__
- [ai_pipeline/03_adviesextractie/finale_output/final_result_schema.md](ai_pipeline/03_adviesextractie/finale_output/final_result_schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/legacy/missing_sources.md](ai_pipeline/04_kabinetsreactie_agent/legacy/missing_sources.md) - __source_file__
- [ai_pipeline/04_kabinetsreactie_agent/shared/stage_06_enums_schema.md](ai_pipeline/04_kabinetsreactie_agent/shared/stage_06_enums_schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_01_segmentatie/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_01_segmentatie/prompt.md) - 01_kabinetsreactie_segmentatie_agent_instruction.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_01_segmentatie/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_01_segmentatie/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_02_stramien/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_02_stramien/prompt.md) - 02_stramien_analyse_agent_instruction.txt.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_02_stramien/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_02_stramien/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_03_reverse_recall/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_03_reverse_recall/prompt.md) - 03_adviesverwijzing_reverse_recall_agent_instruction.txt.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_03_reverse_recall/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_03_reverse_recall/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_04_candidate_pairs/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_04_candidate_pairs/prompt.md) - 04_candidate_pair_retrieval_agent_instruction.txt.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_04_candidate_pairs/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_04_candidate_pairs/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_05_semantische_match/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_05_semantische_match/prompt.md) - 05_semantische_match_agent_instruction.txt.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_05_semantische_match/schema_stage_05_semantische_match_schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_05_semantische_match/schema_stage_05_semantische_match_schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_05_semantische_match/schema_stage_05_semantische_match_semantischematchbasis.md](ai_pipeline/04_kabinetsreactie_agent/stage_05_semantische_match/schema_stage_05_semantische_match_semantischematchbasis.md) - SemantischeMatchBasis
- [ai_pipeline/04_kabinetsreactie_agent/stage_06_positie_opvolging/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_06_positie_opvolging/prompt.md) - 06_kabinetspositie_en_opvolging_agent_instruction.txt.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_06_positie_opvolging/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_06_positie_opvolging/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_06a_positie/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_06a_positie/prompt.md) - 06a_kabinetspositie_agent_instruction.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_06a_positie/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_06a_positie/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_06b_context/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_06b_context/prompt.md) - 06b_opvolgingscontext_agent_instruction.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_06b_context/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_06b_context/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_07_voorlopige_labels/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_07_voorlopige_labels/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_08_audit/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_08_audit/prompt.md) - 08_audit_en_reconciliatie_agent_instruction.txt.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_08_audit/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_08_audit/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_09_eindanalyse/prompt.md](ai_pipeline/04_kabinetsreactie_agent/stage_09_eindanalyse/prompt.md) - 09_eindanalyse_agent_instruction.txt.txt
- [ai_pipeline/04_kabinetsreactie_agent/stage_09_eindanalyse/schema.md](ai_pipeline/04_kabinetsreactie_agent/stage_09_eindanalyse/schema.md) - __classes__
- [ai_pipeline/04_kabinetsreactie_agent/stage_registry.md](ai_pipeline/04_kabinetsreactie_agent/stage_registry.md) - STAGE_DEFINITIONS
- [matchers/01_instellingsmatcher/prompts/llm_judge_discovery_document_classification_system_prompt.md](matchers/01_instellingsmatcher/prompts/llm_judge_discovery_document_classification_system_prompt.md) - DISCOVERY_DOCUMENT_CLASSIFICATION_SYSTEM_PROMPT
- [matchers/01_instellingsmatcher/prompts/llm_judge_document_classification_system_prompt.md](matchers/01_instellingsmatcher/prompts/llm_judge_document_classification_system_prompt.md) - DOCUMENT_CLASSIFICATION_SYSTEM_PROMPT
- [matchers/01_instellingsmatcher/prompts/llm_judge_known_college_url_validation_system_prompt.md](matchers/01_instellingsmatcher/prompts/llm_judge_known_college_url_validation_system_prompt.md) - KNOWN_COLLEGE_URL_VALIDATION_SYSTEM_PROMPT
- [matchers/01_instellingsmatcher/prompts/llm_judge_system_prompt.md](matchers/01_instellingsmatcher/prompts/llm_judge_system_prompt.md) - SYSTEM_PROMPT
- [matchers/01_instellingsmatcher/prompts/llm_judge_visible_college_metadata_audit_system_prompt.md](matchers/01_instellingsmatcher/prompts/llm_judge_visible_college_metadata_audit_system_prompt.md) - VISIBLE_COLLEGE_METADATA_AUDIT_SYSTEM_PROMPT
- [matchers/01_instellingsmatcher/schemas/llm_judge_discovery_document_classification_output_schema.md](matchers/01_instellingsmatcher/schemas/llm_judge_discovery_document_classification_output_schema.md) - DISCOVERY_DOCUMENT_CLASSIFICATION_OUTPUT_SCHEMA
- [matchers/01_instellingsmatcher/schemas/llm_judge_document_classification_output_schema.md](matchers/01_instellingsmatcher/schemas/llm_judge_document_classification_output_schema.md) - DOCUMENT_CLASSIFICATION_OUTPUT_SCHEMA
- [matchers/01_instellingsmatcher/schemas/llm_judge_expected_output_schema.md](matchers/01_instellingsmatcher/schemas/llm_judge_expected_output_schema.md) - EXPECTED_OUTPUT_SCHEMA
- [matchers/01_instellingsmatcher/schemas/llm_judge_known_college_url_validation_output_schema.md](matchers/01_instellingsmatcher/schemas/llm_judge_known_college_url_validation_output_schema.md) - KNOWN_COLLEGE_URL_VALIDATION_OUTPUT_SCHEMA
- [matchers/01_instellingsmatcher/schemas/llm_judge_schema.md](matchers/01_instellingsmatcher/schemas/llm_judge_schema.md) - __classes__
- [matchers/01_instellingsmatcher/schemas/llm_judge_visible_college_metadata_audit_output_schema.md](matchers/01_instellingsmatcher/schemas/llm_judge_visible_college_metadata_audit_output_schema.md) - VISIBLE_COLLEGE_METADATA_AUDIT_OUTPUT_SCHEMA
- [matchers/01_instellingsmatcher/technische_diagnose/diagnostic_judge_expected_diagnostic_schema.md](matchers/01_instellingsmatcher/technische_diagnose/diagnostic_judge_expected_diagnostic_schema.md) - EXPECTED_DIAGNOSTIC_SCHEMA
- [matchers/01_instellingsmatcher/technische_diagnose/diagnostic_judge_prompt_path.md](matchers/01_instellingsmatcher/technische_diagnose/diagnostic_judge_prompt_path.md) - PROMPT_PATH
- [matchers/01_instellingsmatcher/technische_diagnose/diagnostic_judge_schema.md](matchers/01_instellingsmatcher/technische_diagnose/diagnostic_judge_schema.md) - __classes__
- [matchers/01_instellingsmatcher/technische_diagnose/pipeline_error_explainer_prompt_pipeline_error_explainer_prompt_md.md](matchers/01_instellingsmatcher/technische_diagnose/pipeline_error_explainer_prompt_pipeline_error_explainer_prompt_md.md) - pipeline_error_explainer_prompt.md
- [matchers/01_instellingsmatcher/versions_llm_judge_classifier_prompt_version.md](matchers/01_instellingsmatcher/versions_llm_judge_classifier_prompt_version.md) - CLASSIFIER_PROMPT_VERSION
- [matchers/01_instellingsmatcher/versions_llm_judge_discovery_classifier_prompt_version.md](matchers/01_instellingsmatcher/versions_llm_judge_discovery_classifier_prompt_version.md) - DISCOVERY_CLASSIFIER_PROMPT_VERSION
- [matchers/01_instellingsmatcher/versions_llm_judge_known_college_url_validation_prompt_version.md](matchers/01_instellingsmatcher/versions_llm_judge_known_college_url_validation_prompt_version.md) - KNOWN_COLLEGE_URL_VALIDATION_PROMPT_VERSION
- [matchers/01_instellingsmatcher/versions_llm_judge_visible_college_metadata_audit_prompt_version.md](matchers/01_instellingsmatcher/versions_llm_judge_visible_college_metadata_audit_prompt_version.md) - VISIBLE_COLLEGE_METADATA_AUDIT_PROMPT_VERSION
- [matchers/02_adviesmatcher/handmatige_controle/export_chatgpt_review_write_prompt_file.md](matchers/02_adviesmatcher/handmatige_controle/export_chatgpt_review_write_prompt_file.md) - _write_prompt_file
- [matchers/02_adviesmatcher/handmatige_controle/export_kandidaten_chatgpt_prompt_header.md](matchers/02_adviesmatcher/handmatige_controle/export_kandidaten_chatgpt_prompt_header.md) - PROMPT_HEADER
- [matchers/02_adviesmatcher/prompts/llm_judge_system_prompt.md](matchers/02_adviesmatcher/prompts/llm_judge_system_prompt.md) - SYSTEM_PROMPT
- [matchers/02_adviesmatcher/prompts/vlam_promotion_system_prompt.md](matchers/02_adviesmatcher/prompts/vlam_promotion_system_prompt.md) - SYSTEM_PROMPT
- [matchers/02_adviesmatcher/schemas/comparative_review_expected_output_contract.md](matchers/02_adviesmatcher/schemas/comparative_review_expected_output_contract.md) - _expected_output_contract
- [matchers/02_adviesmatcher/schemas/comparative_review_known_relation_roles.md](matchers/02_adviesmatcher/schemas/comparative_review_known_relation_roles.md) - KNOWN_RELATION_ROLES
- [matchers/02_adviesmatcher/schemas/comparative_review_role_guidance.md](matchers/02_adviesmatcher/schemas/comparative_review_role_guidance.md) - _role_guidance
- [matchers/02_adviesmatcher/schemas/comparative_review_schema.md](matchers/02_adviesmatcher/schemas/comparative_review_schema.md) - __classes__
- [matchers/02_adviesmatcher/schemas/llm_judge_allowed_llm_labels.md](matchers/02_adviesmatcher/schemas/llm_judge_allowed_llm_labels.md) - ALLOWED_LLM_LABELS
- [matchers/02_adviesmatcher/schemas/llm_judge_judgement_contract.md](matchers/02_adviesmatcher/schemas/llm_judge_judgement_contract.md) - JUDGEMENT_CONTRACT
- [matchers/02_adviesmatcher/schemas/llm_judge_schema.md](matchers/02_adviesmatcher/schemas/llm_judge_schema.md) - __classes__
- [matchers/02_adviesmatcher/schemas/promotion_policy_coerce_vlam_promotion_result.md](matchers/02_adviesmatcher/schemas/promotion_policy_coerce_vlam_promotion_result.md) - coerce_vlam_promotion_result
- [matchers/02_adviesmatcher/schemas/promotion_policy_schema.md](matchers/02_adviesmatcher/schemas/promotion_policy_schema.md) - __classes__
- [matchers/02_adviesmatcher/schemas/vlam_promotion_schema.md](matchers/02_adviesmatcher/schemas/vlam_promotion_schema.md) - __classes__
- [matchers/02_adviesmatcher/versions_comparative_review_comparative_review_prompt_version.md](matchers/02_adviesmatcher/versions_comparative_review_comparative_review_prompt_version.md) - COMPARATIVE_REVIEW_PROMPT_VERSION
- [matchers/02_adviesmatcher/versions_llm_judge_llm_prompt_version.md](matchers/02_adviesmatcher/versions_llm_judge_llm_prompt_version.md) - LLM_PROMPT_VERSION
- [matchers/02_adviesmatcher/versions_promotion_policy_promotion_policy_version.md](matchers/02_adviesmatcher/versions_promotion_policy_promotion_policy_version.md) - PROMOTION_POLICY_VERSION
- [matchers/02_adviesmatcher/versions_vlam_promotion_vlam_promotion_prompt_version.md](matchers/02_adviesmatcher/versions_vlam_promotion_vlam_promotion_prompt_version.md) - VLAM_PROMOTION_PROMPT_VERSION
- [matchers/03_kabinetsreactie_matcher/handmatige_controle/build_chatgpt_kabinetsreactie_search_batches_prompt_header.md](matchers/03_kabinetsreactie_matcher/handmatige_controle/build_chatgpt_kabinetsreactie_search_batches_prompt_header.md) - PROMPT_HEADER
- [matchers/03_kabinetsreactie_matcher/prompts/run_vlam_response_judge_system_prompt.md](matchers/03_kabinetsreactie_matcher/prompts/run_vlam_response_judge_system_prompt.md) - SYSTEM_PROMPT
- [matchers/03_kabinetsreactie_matcher/prompts/run_vlam_response_to_other_advice_chooser_system_prompt.md](matchers/03_kabinetsreactie_matcher/prompts/run_vlam_response_to_other_advice_chooser_system_prompt.md) - SYSTEM_PROMPT
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_allowed_target_types.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_allowed_target_types.md) - ALLOWED_TARGET_TYPES
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_allowed_verdicts.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_allowed_verdicts.md) - ALLOWED_VERDICTS
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_build_vlam_user_payload.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_build_vlam_user_payload.md) - build_vlam_user_payload
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_coerce_vlam_response_output.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_coerce_vlam_response_output.md) - coerce_vlam_response_output
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_schema.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_judge_schema.md) - __classes__
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_to_other_advice_chooser_allowed_choices.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_to_other_advice_chooser_allowed_choices.md) - ALLOWED_CHOICES
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_to_other_advice_chooser_build_choice_payload.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_to_other_advice_chooser_build_choice_payload.md) - build_choice_payload
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_to_other_advice_chooser_coerce_chooser_output.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_to_other_advice_chooser_coerce_chooser_output.md) - coerce_chooser_output
- [matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_to_other_advice_chooser_schema.md](matchers/03_kabinetsreactie_matcher/schemas/run_vlam_response_to_other_advice_chooser_schema.md) - __classes__
- [matchers/03_kabinetsreactie_matcher/versions_run_vlam_response_judge_prompt_version.md](matchers/03_kabinetsreactie_matcher/versions_run_vlam_response_judge_prompt_version.md) - PROMPT_VERSION
- [matchers/03_kabinetsreactie_matcher/versions_run_vlam_response_to_other_advice_chooser_prompt_version.md](matchers/03_kabinetsreactie_matcher/versions_run_vlam_response_to_other_advice_chooser_prompt_version.md) - PROMPT_VERSION
- [matchers/04_parlementaire_matcher/prompts/prompt_builder_system_prompt.md](matchers/04_parlementaire_matcher/prompts/prompt_builder_system_prompt.md) - SYSTEM_PROMPT
- [matchers/04_parlementaire_matcher/schemas/prompt_builder_expected_output_schema.md](matchers/04_parlementaire_matcher/schemas/prompt_builder_expected_output_schema.md) - EXPECTED_OUTPUT_SCHEMA
- [matchers/04_parlementaire_matcher/schemas/schemas_schema.md](matchers/04_parlementaire_matcher/schemas/schemas_schema.md) - __classes__
- [matchers/04_parlementaire_matcher/versions_prompt_builder_prompt_version.md](matchers/04_parlementaire_matcher/versions_prompt_builder_prompt_version.md) - PROMPT_VERSION
- [matchers/04_parlementaire_matcher/versions_schemas_schema_version.md](matchers/04_parlementaire_matcher/versions_schemas_schema_version.md) - SCHEMA_VERSION

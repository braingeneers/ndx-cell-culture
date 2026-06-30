# Schema Reference

This page summarizes the user-facing fields in `ndx-cell-culture`. The authoritative machine-readable schema lives in `spec/ndx-cell-culture.extensions.yaml`.

Requirement terms:

- Required: constructor/schema required in the current draft.
- Optional: omitted values are allowed.
- Recommended terms: documented vocabulary guidance, not hard enum validation in the current draft. Use `ndx_cell_culture.validate_recommended_terms` for opt-in checking.

## CellCultureSubject

Extends core `NWB.Subject`.

Inherited from `NWB.Subject` and not redefined by this extension:

| Field | Guidance |
| --- | --- |
| `subject_id` | Stable NWB subject identifier. |
| `species` | Formal binomial preferred. |
| `sex` | Use core NWB/PyNWB recommended values `F`, `M`, `U`, `O`. |
| `description` | Short human-readable subject summary. |
| `age` | Usually not used for cultured preparations; do not use for culture age. |
| `age__reference` | Core subject age reference; do not use for culture timing. |
| `date_of_birth` | Usually not applicable for cultured preparations. |
| `genotype` | Avoid for structured engineered edits; use `GeneticVariant`. |
| `strain` | Usually animal-centric. |
| `weight` | Usually not meaningful for cell cultures/organoids. |

Extension-owned link:

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `culture` | Required | link to `CellCulture` | Recorded or described cultured neural preparation cataloged in `CultureExperimentContext`. |

## CellCulture

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `culture_id` | Required | text attribute | Stable culture identifier. |
| `culture_type` | Required | text attribute | Recommended terms: `dissociated_culture`, `spheroid`, `organoid`, `assembloid`, `slice`, `explant`, `other`; `batch` is prohibited. |
| `sample_label` | Required | text attribute | Human-readable label. |
| `species` | Required | text attribute | Culture-level convenience/search value; may mirror subject species. |
| `culture_subtype` | Optional | text attribute | Regional/subtype identity such as `cortical`, `thalamic`, `midbrain`, `hippocampal`, `retinal`, `spinal`, `assembloid`, `tumor_organoid`, `other`. |
| `batch_label` | Optional | text attribute | Lightweight grouping/search label only; not a batch object. |
| `age` | Optional | text attribute | Prefer ISO-8601 duration such as `P120D`; pilot lab labels such as `day45` are allowed. |
| `age_reference` | Optional | text attribute | Recommended terms include `days_in_vitro`, `days_post_induction`, `days_post_aggregation`, `days_post_differentiation`, `days_since_plated`, `days_since_sectioning`, `other`. |
| `disease_or_diagnosis` | Optional | text attribute | Disease background or diagnosis. |
| `reference_genome` | Optional | text attribute | Assembly/annotation context; not a substitute for `Subject.genotype`. |
| `notes` | Optional | text attribute | Free-text remarks. |
| `source_lines` | Optional/repeated | object references to `CellLine` | Source line or lines used to create this culture. Pass a list of `CellLine` objects; read back as an object-reference vector. |
| `parent_cultures` | Optional/repeated | object references to `CellCulture` | Parent or input cultures used to derive this culture. Use for slices, directoids/connectoids, assembloids, and other culture-derived preparations. |
| `GeneticVariant` children | Optional/repeated | child groups | Culture-attached genetic variants. |
| `ConstructApplication` children | Optional/repeated | child groups | Culture-attached construct applications. |
| `CultureProtocol` child | Optional | child group | Structured derivation/preparation protocol. |

## CellLine

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `cell_line_id` | Required | text attribute | Stable cell-line identifier. |
| `cell_line_type` | Required | text attribute | Recommended terms: `donor`, `parental_cell_line`, `derived_cell_line`, `immortalized_line`, `other`. |
| `sample_label` | Required | text attribute | Human-readable label. |
| `species` | Required | text attribute | Formal binomial preferred. |
| `cell_source_type` | Required | text attribute | Recommended terms: `iPSC`, `ESC`, `primary_tissue`, `primary_cells`, `tumor_line`, `immortalized_line`, `other`. |
| `cell_line_name` | Optional | text attribute | Canonical/common line name. |
| `cell_line_rrid` | Optional | text attribute | RRID when available. |
| `clone_id` | Optional | text attribute | Clone identifier for a clonal derived line. |
| `clonal_status` | Optional | text attribute | Recommended terms: `clonal`, `polyclonal`, `mixed`, `unknown`. |
| `passage_number` | Optional | text attribute | Passaging information; do not use culture-age fields on `CellLine`. |
| `disease_or_diagnosis` | Optional | text attribute | Disease background or diagnosis. |
| `reference_genome` | Optional | text attribute | Assembly/annotation context such as `GRCh38`. |
| `notes` | Optional | text attribute | Free-text remarks. |
| `parent_cell_line` | Optional | object reference to `CellLine` | Parent or source line for a derived line. Pass a `CellLine` object; read back as a one-element object-reference vector. |
| `GeneticVariant` children | Optional/repeated | child groups | Variants attached at line level. |
| `ConstructApplication` children | Optional/repeated | child groups | Construct applications attached at line level. |

## Provenance

Provenance is represented directly on catalog entries:

- use `CellLine.parent_cell_line` for cell-line derivation;
- use `CellCulture.source_lines` for source lines used to create a culture;
- use `CellCulture.parent_cultures` for parent/input cultures used to derive another culture.

These fields are stored as NWB object-reference datasets so referenced `CellLine` and `CellCulture` catalog entries are not duplicated.

## GeneticVariant

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `variant_id` | Required | text attribute | Stable variant identifier. |
| `target_symbol` | Required | text attribute | Gene symbol or target name. |
| `target_coordinates` | Optional | text attribute | Genomic coordinates, transcript notation, or locus. |
| `edit_type` | Required | text attribute | Recommended terms include `knockout`, `knockin`, `point_mutation`, `deletion`, `duplication`, `inversion`, `tag_insertion`, `reporter_insertion`, `CRISPRi_targeting`, `CRISPRa_targeting`, `other`. |
| `edit_description` | Optional | text attribute | Human-readable edit description. |
| `method` | Required | text attribute | Recommended terms include `CRISPR-Cas9`, `base_editing`, `prime_editing`, `TALEN`, `ZFNs`, `homologous_recombination`, `other`. |
| `delivery_method` | Optional | text attribute | Edit-delivery method such as `RNP`, `plasmid`, `lentivirus`, `AAV`, `electroporation`, `lipofection`, `other`. |
| `zygosity_or_edit_state` | Optional | text attribute | Recommended terms include `heterozygous`, `homozygous`, `biallelic`, `hemizygous`, `mosaic`, `unknown`, `other`. |
| `validation_status` | Optional | text attribute | Recommended terms: `planned`, `screened`, `validated`, `failed`, `unknown`. |
| `validation_method` | Optional | text attribute | Recommended terms include `Sanger`, `amplicon_seq`, `WGS`, `WES`, `ONT`, `ddPCR`, `PCR`, `fluorescence imaging`, `other`. |
| `notes` | Optional | text attribute | Free-text remarks. |
| `related_application` | Optional | link to `ConstructApplication` | Related construct application. |

## ConstructApplication

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `application_id` | Required | text attribute | Stable application identifier. |
| `source` | Optional | text attribute | Construct source, catalog, vendor, plasmid, person, or lab. |
| `delivery_route` | Optional | text attribute | Broad route such as `transduction`, `transfection`, `microinjection`, `cell_fusion`, `other`. |
| `delivery_mechanism` | Optional | text attribute | Technical mechanism such as `lipofection`, `polymer_transfection`, `calcium_phosphate`, `electroporation`, `nucleofection`, `nanoparticle_mediated`, `other`; do not use `microinjection` here. |
| `vector_type` | Required | text attribute | Vector/reagent class such as `AAV`, `lentivirus`, `retrovirus`, `plasmid`, `transposon`, `RNP`, `minicircle_dna`, `linear_dna`, `rna`, `mrna`, `sirna`, `crispr_rna`, `adenovirus`, `baculovirus`, `herpes_simplex_virus`, `other`. |
| `payload` | Required | text attribute | Gene, cassette, tool, or reagent delivered. |
| `promoter` | Optional | text attribute | Expression promoter if known. |
| `genomic_persistence_state` | Optional | text attribute | Recommended terms include `genomically_integrated`, `episomal_or_extragenomic`, `transient_nonintegrating`, `unknown`, `other`. |
| `application_time_relative_to_recording` | Optional | text attribute | Human-readable timing relative to recording. |
| `age_modified` | Optional | text attribute | Culture age at application. |
| `age_modified_reference` | Optional | text attribute | Reference event for `age_modified`. |
| `expression_status` | Optional | text attribute | Recommended terms: `planned`, `observed`, `validated`, `failed`, `unknown`. |
| `validation_method` | Optional | text attribute | Method used to confirm expression/delivery. |
| `notes` | Optional | text attribute | Free-text remarks. |

## CultureProtocol

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `protocol_id` | Required | text attribute | Stable protocol identifier. |
| `protocol_name` | Optional | text attribute | Human-readable protocol name. |
| `protocol_uri` | Optional | text attribute | Direct protocol URI. |
| `protocol_doi` | Optional | text attribute | Protocol DOI. |
| `protocol_version` | Optional | text attribute | Version/revision label. |
| `patterning_summary` | Optional | text attribute | Short patterning summary, not a full protocol. |
| `media_summary` | Optional | text attribute | Short media summary. |
| `notes` | Optional | text attribute | Free-text remarks. |

## CultureExperimentContext

Extends core `LabMetaData`.

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `name` | Required by `LabMetaData` | group name | Recommended value: `culture_experiment_context`. |
| `CellLine` children | Optional/repeated | child groups | Reusable cell-line catalog entries for this NWB file. |
| `CellCulture` children | Optional/repeated | child groups | Reusable culture catalog entries for this NWB file. |
| `ExperimentContext` child | Optional | child group | Recording/session context for this file. |
| `Pharmacology` children | Optional/repeated | child groups | Pharmacology rows linked to experiment context. |

## ExperimentContext

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `experiment_id` | Required | text attribute | Stable experiment context identifier. |
| `session_id` | Optional | text attribute | Session/date/acquisition label. |
| `age_at_recording` | Required | text attribute | Culture age at recording. |
| `age_reference` | Optional | text attribute | Reference event for `age_at_recording`. |
| `recording_platform` | Required | text attribute | Recommended terms: `MEA`, `patch_clamp`, `calcium_imaging`, `multimodal`, `other`. |
| `media_or_bath` | Optional | text attribute | Recording media, bath, or ACSF. |
| `experimental_setup` | Optional | text attribute | Short setup summary. |
| `notes` | Optional | text attribute | Free-text remarks. |
| `temperature_c` | Optional | float32 attribute | Recording temperature in Celsius. |
| `recording_duration_s` | Optional | float32 attribute | Recording duration in seconds. |
| `spontaneous_activity` | Optional | bool attribute | Search flag. |
| `electrical_stimulation` | Optional | bool attribute | Search flag; detailed waveforms belong in core NWB stimulus data. |
| `optical_stimulation` | Optional | bool attribute | Search flag; detailed waveforms belong in core NWB stimulus data. |
| `pharmacology_present` | Optional | bool attribute | Search flag. |
| `subject` | Required | link to `CellCultureSubject` | Subject recorded in this experiment. |
| `culture` | Required | link to `CellCulture` | Culture recorded in this experiment. |
| `device` | Optional | link to core `Device` | Core NWB recording device. |

## Pharmacology

| Field | Requirement | Type | Guidance |
| --- | --- | --- | --- |
| `pharmacology_id` | Required | text attribute | Stable pharmacology identifier. |
| `agent` | Required | text attribute | Compound/reagent name. |
| `concentration` | Optional | text attribute | Flexible value or range for search. |
| `concentration_unit` | Optional | text attribute | Recommended terms: `M`, `mM`, `uM`, `nM`, `pM`, `%`, `mg/mL`, `ug/mL`, `ng/mL`, `other`. |
| `purpose` | Optional | text attribute | Purpose or interpretation note. |
| `notes` | Optional | text attribute | Free-text remarks. |
| `start_time_s` | Optional | float32 attribute | Start time relative to recording start. |
| `end_time_s` | Optional | float32 attribute | End time relative to recording start. |
| `experiment` | Required | link to `ExperimentContext` | Experiment context this intervention belongs to. |

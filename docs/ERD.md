# ERD (MVP)

`users` 1—N `applicant_profiles`

`universities` 1—N `education_programs`

`program_groups` 1—N `education_programs`

`universities` + `program_groups` -> `admission_thresholds`, `tuition_fees`, `historical_cutoffs`

`program_groups` -> `grant_allocations`

`forecast_runs` links `users`, `applicant_profiles`, `universities`, `program_groups`

`source_documents` referenced by fact tables via `source_id`

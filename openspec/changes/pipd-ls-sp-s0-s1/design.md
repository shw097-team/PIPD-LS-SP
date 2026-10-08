# Design

The deterministic compiler owns normalization, schema validation, semantic invariant
validation, dependency graph, artifact identity/hash, profile compute + safety veto,
technology admission resolution, claim enforcement, package/projection and readback.
No LLM judgement sits on that path (總藍圖 §5.9.1). Artifacts are content-addressed so
the same input lock reproduces the same ids; only epoch fields may differ (G-S4-REPLAY).

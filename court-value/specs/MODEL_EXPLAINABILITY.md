# Model Explainability

CourtValue explainability has two layers:

1. **Global Explainability**
   - XGBoost gain-based feature importance.
   - Returned as top-ranked features and relative importance.

2. **Local Explainability (Per Player)**
   - SHAP TreeExplainer generates feature attributions.
   - Top positive and negative drivers are surfaced.
   - Each attribution includes direction and deterministic interpretation text.

Design principles:
- No agents in V1.
- Explainability is descriptive and directional.
- Output supports analyst judgment and communication.

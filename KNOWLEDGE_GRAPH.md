# Knowledge Graph — Live Representation
*Last Updated: 2026-10-27 03:50:11*

```mermaid
flowchart TD
    linalg_vec["Vector as Displacement"]
    linalg_span["Linear Combinations & Span"]
    linalg_trans["Matrices as Linear Transforms"]
    linalg_det["Determinant (Area/Volume Scaling)"]
    linalg_vec --> linalg_span
    linalg_span --> linalg_trans
    linalg_trans --> linalg_det
    style linalg_vec fill:#2e7d32,stroke:#1b5e20,color:#fff
    style linalg_span fill:#2e7d32,stroke:#1b5e20,color:#fff
    style linalg_trans fill:#f57c00,stroke:#e65100,color:#fff
    style linalg_det fill:#37474f,stroke:#263238,color:#fff
```

### Legend
- 🟢 **Green (Mastered):** Confirmed understanding via active recall.
- 🟠 **Orange (Learning):** Active in-progress topic.
- 🔴 **Red (Gap / Misconception):** Diagnosed misconception to repair.
- ⚪ **Gray (Planned):** Next dependency path.

# Reconstructed Architecture

```text
Aegis desktop services/scanner
        | canonical events + health + evidence refs
        v
Companion Bridge / authenticated transport
        |
        +-- iOS Companion UI
        +-- Manual command/search
        +-- Optional voice
        +-- Optional ChatGPT assistant
        +-- Diagnostics/recovery
```

The Companion is a consumer/control surface, not a scanner dependency.

Every command declares:
- mode
- requested capability
- correlation_id
- idempotency_key

The bridge rejects anything outside current authority.

# Module brief

The design for a change that stays inside one module. Use the words from `codebase-design`: module, interface, seam, adapter. Keep every heading. Write "unchanged" or "no new seam" when a section has nothing.

```markdown
# Brief: <change>

- Spec: <issue link or path>
- Module: <name in the code>
- Decision: <decision.md, or "interface already settled">

## Interface

<what a caller must know: signature, invariants, ordering, error modes>

## Seam

<where the interface lives, the dependency category, and the adapters. An adapter only when two exist>

## Hidden

<what the implementation keeps from callers>

## Tests

| Acceptance criterion | Observable outcome at the interface |
| --- | --- |
```

Every acceptance criterion in the spec gets one row. The test crosses the interface, not the implementation.

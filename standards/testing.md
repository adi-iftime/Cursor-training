# Testing standards (blueprint)

- **Levels:** Unit for pure logic; integration for I/O and contracts; smoke/e2e where product risk warrants.
- **CI:** Required checks named in workflow config; failing checks block merge unless explicitly waived with ticket.
- **Data:** Where possible, fixture-based or sandbox warehouse tests; never run destructive tests against production.

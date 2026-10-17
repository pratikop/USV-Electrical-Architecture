# Engineering review - concept revision D

**Independent conceptual study — unbuilt and unvalidated.**

## Scope and present maturity

This is a preliminary electrical concept for a supervised civilian environmental-monitoring USV. The files establish a design basis and show analytical sizing and documentation methods. They do not authorize procurement, construction or operation.

The strongest present evidence is the traceable load budget, feeder-resistance arithmetic, distinction between propulsion and service supplies, preliminary material quantities, and planned verification. The weakest evidence is the unverified propulsion assumption and the absence of selected component data.

## Open engineering issues

| ID | Issue | Required input / next action | Release implication |
|---|---|---|---|
| O01 | Two-hour endurance depends on an assumed 600 W propulsion load | Obtain hull resistance / thruster input data and representative duty cycle | Mission duration cannot be promised |
| O02 | 100 Ah battery mass and displacement not assessed | Review pack mass, buoyancy, stability and mounting with mechanical engineer | Battery size remains a concept assumption |
| O03 | Cable thermal ratings are assumed | Select cable; apply ambient/bundle/installation derating and terminal limits | Cable cross sections not released |
| O04 | Battery fault current / fuse coordination unknown | Obtain pack/BMS data and fuse time-current / let-through / interrupt data | Candidate fuse sizes are not validated protection selections |
| O05 | Controllers and converter not selected | Verify minimum terminal voltage, full-charge/transient voltage, inrush, regeneration and current limiting | No compatibility claim |
| O06 | Propulsion permit is a functional proposal | Complete reset, supplies, feedback, watchdog and independent disable design; assess failures | No safety integrity or automatic-control implementation claim |
| O07 | Field terminal allocations are illustrative | Obtain vendor pinouts; select connectors, shields, data termination and routing | No production connection or harness release |
| O08 | Enclosure heat, ingress and corrosion unresolved | Establish loss model, ambient conditions, enclosure cooling/condensation and bonding approach | IP67 is an assembly target, not a tested rating |
| O09 | Applicable marine requirements not assessed | Agree craft category, jurisdiction and verification basis with competent reviewer | No certification or compliance claim |

## Review discipline

- Inputs are labelled assumptions; arithmetic outputs are labelled calculated estimates.
- Proposed tests remain NOT RUN until dated evidence exists.
- A DXF audit checks file structure, not electrical correctness or AutoCAD application behaviour.
- The positive and return circuits require a competent schematic/connectivity review before use.
- Any numerical change must trigger review of affected drawings, cable quantities, protection and test limits.

No reviewer approval has been obtained. This issue register makes the concept's maturity explicit; it does not close the issues.

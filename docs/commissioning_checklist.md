# Proposed commissioning test record

**Independent conceptual study — unbuilt and unvalidated.**

Every test is NOT RUN. This is a proposed checklist, not a record of commissioning experience. Run only after design release and an approved supervised test plan. No uncontrolled short-circuit, BMS bypass or lithium-pack fault-injection test is proposed. Use current-limited laboratory supplies for logic checks; disconnect propulsion or use an approved guarded load arrangement. Do not dry-run a water-cooled thruster. All numeric targets below are preliminary project targets, not certification limits.

Record for each test: date, operator/reviewer, procedure revision, selected equipment serial numbers, calibrated instrument IDs, supply/load conditions, measured values, pass/fail, evidence path and corrective action. Present state: date blank; result NOT RUN; evidence none.

| ID / requirement | Proposed method | Acceptance / evidence | Status |
|---|---|---|---|
| T01 / R02-R09 | Drawing/BOM/datasheet review before energizing | Resolve all release gates; ratings and actual routing signed off; record fuse curves and prospective fault current | NOT RUN |
| T02 / R09 | De-energized inspection: polarity, wire tags, source protection, continuity, crimps, torque and strain relief | Wiring matches released drawing; intended return continuous; unintended +/return/metal continuity absent; manufacturer torque recorded | NOT RUN |
| T03 / R02 | Review pack/BMS documentation and approved status interface; verify charge restrictions and expected protective responses | Pack limits match system; charge/discharge permissions recorded; never test by deliberately shorting pack | NOT RUN |
| T04 / R02/R04 | Current-limited supply sweep 22.4-29.2 V at panel input; add agreed feeder drop; load service outputs to 60 W | 12 V bus 11.4-12.6 V at panel; endpoints within device limits; no unintended reset; input current and thermal record | NOT RUN |
| T05 / R03/R05 | Approved electronic loads at controller inputs emulate simultaneous 600 W electrical loads; measure path drops and temperature | Cable-only drop <=3% at 22.4 V; terminal voltage above selected ESC UV limit; total path and connection drops recorded; temperatures below all derated ratings | NOT RUN |
| T06 / R06 | With props disconnected/guarded, operate S1 at several commands; restore S1 and power-cycle control | K1 opens, permit disappears, hotel remains live; proposed power-removal time <=0.5 s; no re-arm without manual reset; actual time captured | NOT RUN |
| T07 / R07/R10 | Inject missing/stale heartbeat >1 s, sensor disconnection and controller reboot on bench | Neutral then K1 open as specified; no automatic re-arm; fault visible; proposed 1 Hz records include timestamp, position and sensor-valid flag | NOT RUN |
| T08 / R08 | Approved enclosure inspection and ingress test with electronics protected; review EMC/corrosion/condensation plan | Assembly meets selected ingress procedure; no water at electrical terminations; record method and limits; no self-certification claim | NOT RUN |
| T09 / R03/R06 | Reviewed motor/ESC setup in guarded wet facility; evaluate stop, ESC alarm and single-branch loss; simulate welded K1 feedback without making a live welded contact | Document thrust/power response and DC transients; detect feedback mismatch and inhibit re-arm; do not claim single-fault tolerance | NOT RUN |
| T10 / R01 | Only after prior gates: supervised sheltered-water endurance trial with recovery boat, logged V/I/SOC, temperature and mission conditions | Complete 2 h while remaining within pack limits and the planned 80% SOC window; no unexpected resets or overheating; report measured Wh separately from predictions | NOT RUN |

The T06 0.5 s target concerns commanded propulsion power removal, not zero thrust or stopped vessel motion. Residual energy, controller faults and drifting require separate risk review. T05 cannot prove fuse clearing/selectivity; demonstrate those with supplier curves and qualified review under T01, not destructive battery tests. An insulation test voltage is not specified: isolate sensitive devices and follow selected manufacturers' limits.

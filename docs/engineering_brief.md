# ENV-USV-01 | Electrical concept, revision A

**Independent conceptual study — unbuilt and unvalidated.**

Author: Pratik Prabhakar Shinde. Independent portfolio study, 17 October 2026. No employer involvement, proprietary information, certification, construction, simulation or measured performance is claimed. The study demonstrates a proposed engineering workflow; the author should reproduce the calculations and explain the assumptions before submission.

## Purpose and boundary

Civilian environmental monitoring on a small, approximately 2-3 m nonconductive USV in sheltered water, within visual supervision and with a recovery boat available. Payload: temperature, conductivity and turbidity instrument package, logging position and water-quality data. A two-hour mission is the sizing target. Hull size is descriptive only; displacement, speed, stability and battery mass feasibility are unresolved. No offshore capability or autonomous navigation safety is demonstrated.

Included: DC architecture, load estimates, feeder calculations, interface allocation, preliminary material quantities and proposed commissioning checks. Excluded: hull/propeller selection, hydrodynamics, production harnesses, detailed controller firmware, navigation software, charging hardware design and certification. No sonar, weapons or surveillance payloads.

## Requirements and traceability

| ID | Proposed requirement / acceptance target | Evidence now | Future verification |
|---|---|---|---|
| R01 | Two-hour mission at assumed 600 W combined cruise propulsion | Analytical energy budget; 37.4% energy margin | T10 endurance measurement |
| R02 | Battery 25.6 V nominal, planning range 22.4-29.2 V | 8-series LiFePO4 assumption | T03 selected pack/BMS data; T04 voltage sweep |
| R03 | Independent port/starboard protected DC feeders, 600 W electrical peak each | Block/wiring drawings, 40 A candidate fuses | T05 controller/load tests; T09 stop test |
| R04 | Regulated 12 V, 60 W baseline auxiliary/payload demand | Load budget and 120 W converter requirement | T04 output 11.4-12.6 V under specified loads |
| R05 | Cable-only propulsion DC path drop <=3% at simultaneous peak | 2.07% estimate; excludes connection losses | T05 measured terminal voltage and thermal check |
| R06 | Local stop removes propulsion permit; auxiliary supply retained | Proposed K1 circuit, no safety integrity claim | T06 stop/re-arm; T09 fault scenarios |
| R07 | Loss of valid heartbeat for >1 s requests neutral then opens K1 | Behaviour requirement only; no code implemented | T07 injected loss and restart scenarios |
| R08 | Sealed deck electrical enclosure, target IP67 as assembled | Procurement target only | T08 approved enclosure/ingress procedure |
| R09 | Dedicated insulated positive/negative conductors; no hull return | Concept wiring and cable schedule | T02 return/bonding review and continuity |
| R10 | Environmental data and GNSS timestamps logged, target 1 Hz | Proposed RS-485/Ethernet interfaces | T07 simulated sensor record and timestamp check |

## Design decisions to defend

1. **24 V class propulsion:** half the current of 12 V for equal electrical power; manageable battery size and fewer series cells than a 48 V class system. No claim that the choice is globally optimal. A 48 V system should be reconsidered if real propulsion demand increases.
2. **One battery, two feeders:** simple architecture appropriate to a small portfolio project. Branch faults may be isolated only if fuse coordination is confirmed. Battery, BMS, main fuse and converter remain single points of failure; this is not a redundant vessel.
3. **12 V auxiliary bus stays live after propulsion stop:** preserves telemetry and position logging while K1 opens. It is still lost on pack/BMS/main-disconnect failure. Independent recovery power is a future option.
4. **No onboard charger:** pack is removed, isolated and charged ashore using an approved pack-compatible charger. Operational charge interlocks and low-temperature charge restrictions must come from the selected battery manufacturer.
5. **Nonconductive hull assumption:** no hull current return. A non-isolated DC/DC gives a shared DC negative reference. Exposed metal bonding, shielding, corrosion and any intentional negative-to-bond connection remain subject to a dedicated review; do not improvise a seawater earth.
6. **Stop philosophy:** local S1 normally closed contact interrupts K1 coil independently of the mission computer. SR1 is a conceptual manual-reset permit relay; K2 is a normally open watchdog-permit contact. Both must close to energize K1. No automatic re-arm after supply restoration, heartbeat restoration or stop reset. Exact relay/feedback circuit is not designed. A welded K1 can defeat isolation; feedback detection and independent controller-disable input are required follow-up work. This is not a certified emergency-stop circuit.
7. **Fail on loss of communication:** propose neutral command, then remove propulsion permit after >1 s without heartbeat. Drift is a resulting hazard; restrict trials to a controlled area with retrieval available. Neutral-before-open reduces switching stress but must not delay local stop. Contactor DC breaking capability, ESC capacitance, precharge, regenerative voltage and suppression/drop-out timing remain open.
8. **Sensor separation:** route data away from motor power, cross at right angles where needed, use twisted data pairs and follow selected-device shield guidance. RS-485 is allocated to water-quality payload; Ethernet to logger/radio; CAN to controllers only if supported, with two end terminations as required. These are interface proposals, not tested compatibility.

## Illustrative connection plan

| Connection | Proposed allocation | Status |
|---|---|---|
| X1 | Battery service connector: + / - / optional BMS status | Vendor pinout and interlock TBD |
| X2, X3 | Port / starboard controller DC+ and DC- | Power contacts and disconnect-under-load prohibition TBD |
| X4 | 12 V service panel + / return | Converter output protection F5; branch fuses downstream |
| X5 | Water sensor: 1=+12 V, 2=return, 3=RS485 A, 4=RS485 B | Illustrative logical allocation, NOT vendor pinout |
| X6 | Deck stop / permit loop | Contact rating, circuit feedback and connector pins TBD |

Port/starboard thruster phase leads are vendor-supplied assemblies, not sized by DC feeder calculations. This is not a production connection plan. No connector is authorized for procurement until its current rating, sealing, pinout, keying and mating requirements are verified.

## Preliminary harness / cable quantities

| ID | From / to | One-way m | Conductors | Copper mm2 per conductor | Provisioned conductor-m incl. 20% |
|---|---|---:|---|---:|---:|
| C01 | B1 / F0 / Q0 / distribution and return | 1 | + and - | 25 | 2.4 |
| C02 | F1 / K1 bus to ESC1 and return | 3 | + and - | 10 | 7.2 |
| C03 | F2 / K1 bus to ESC2 and return | 3 | + and - | 10 | 7.2 |
| C04 | F3 / converter input and return | 2 | + and - | 2.5 | 4.8 |
| C05 | F4 / stop-permit-coil circuit and return | 2 equivalent route | Loop, exact segments TBD | 0.75 | 4.8 provisional |
| C06 | Converter / F5 / 12 V panel and return | 0.5 | + and - | 2.5 | 1.2 |

C01 includes short distribution links in its assumed 1 m envelope; add real segment lengths after layout. Fuse F0 is adjacent to the battery positive terminal; protect any unavoidable short unfused section mechanically. Q0 disconnects both conductors. Only positive conductors are fused in this proposed common-negative arrangement. Verify this grounding/protection arrangement against the selected applicable rules.

12 V branches: F6=3 A navigation (autopilot+GNSS, 18 W); F7=2 A computer/logger (10 W); F8=2 A radio (12 W); F9=2 A water payload (10 W); F10=2 A indication/monitoring (10 W). Assume each + and return route is <=2 m using 0.75 mm2 cable with assumed derated ampacity >=5 A. Total provision: 24 conductor-m at 0.75 mm2 plus C05 4.8 = 28.8 conductor-m. Worst branch at 1.5 A: deltaV=2*2*0.0225*1.5/0.75=0.180 V; plus C06 0.045 V gives 0.225 V (1.88%). Upstream DC drop is rejected by the regulated converter if input headroom is adequate. Termination loss is extra. Each branch fuse passes the same provisional 1.25I<=In<=Iz screening rule. F5 7.5 A limits the service panel below the full converter rating; additional payloads require rechecking it.

## Open release gates

- Choose pack, ESC, motor, DC/DC and cable datasheets. Confirm mass, load profile, environmental ratings and continuous/peak current limits.
- Establish actual derated cable ampacity from insulation, ambient temperature, bundle size, routing and terminal ratings. Present values are assumed, not table selections.
- Determine battery prospective fault current and every relevant fuse interrupt rating. Validate selectivity and energy let-through against BMS, wiring and device withstand. Never infer selective clearing from fuse ratios.
- Validate ESC undervoltage operation at remote terminals, full-charge/transient voltage, motor-stall limiting, input inrush/precharge and regenerative-energy handling.
- Resolve bonding/corrosion, enclosure condensation and cooling. Converter dissipation is approximately 6.7 W at baseline; controller and battery heat are not modelled.
- Complete stop/arming hardware logic, feedback and fault response with competent review. No automatic recovery thrust is allowed by the proposed requirements.
- Identify the applicable jurisdiction, craft category and rules; review relevant small-craft DC electrical, battery and marine equipment requirements with current official texts. No compliance assessment has been performed.

## Sources and provenance

Accessed 17 October 2026. Manufacturer guidance supports the method, not the assumed loads, cable ampacities or component compatibility.

- Quantum Systems role description: https://career.quantum-systems.com/o/electrical-engineer-mfd-4 (alignment to drawings, BOM and proposed setting-to-work procedures only).
- Victron Energy, Wiring Unlimited, section 4: https://www.victronenergy.com/media/pg/The_Wiring_Unlimited_book/en/dc-wiring.html (cable resistance, voltage drop and DC protection selection principles).
- Blue Sea Systems, Circuit Protection: https://www.bluesea.com/resources/96 (protection at distribution branches and cable-size transitions).
- User-supplied CV/background: Bachelor of Electrical Engineering, ongoing TU Dortmund master's, over three years electrical experience including approximately 14 months at Zener Maritime. No employer deliverables are reproduced.

All project numbers are explicitly assumed or analytically calculated. No physical or simulated performance has been validated. AutoCAD, MATLAB/Simulink, Python and Excel are supported background tools; this package uses Python-generated vector diagrams and calculations. EPLAN, production harness design, automation programming and USV/UUV integration remain learning areas.

# Preliminary BOM / material take-off

**Independent conceptual study — unbuilt and unvalidated.**

Functional specifications only. No selected manufacturer, confirmed compatibility, supplier quote, purchase price or procurement release. Quantities are preliminary. All DC power switchgear and fuses: candidate voltage rating >=60 V DC; adequate breaking/interrupt rating must be established from fault-current analysis.

| Tag | Qty | Item / minimum conceptual requirement | Selection hold |
|---|---:|---|---|
| B1 | 1 | 8S LiFePO4, 25.6 V nominal, 100 Ah; BMS >=100 A continuous; status output preferred | Capacity, fault current, BMS limits, temperature protection, mass, ingress |
| F0 | 1 | 80 A battery fuse and touch-safe holder, source-adjacent | Interrupt rating, time-current curve, thermal derating |
| Q0 | 1 | Two-pole manual battery isolator, >=100 A continuous | DC load break rating and accessibility |
| BB1/BB2 | 1 pair | Covered positive and negative distribution bars, >=100 A | Temperature, short-circuit withstand, terminals |
| K1 | 1 | DC propulsion contactor, >=100 A continuous; coil compatible with 22.4-29.2 V; auxiliary feedback | DC break at >=60 A actual circuit, welded-contact response, suppression |
| F1/F2 | 2 | 40 A controller feeder fuses and holders | Controller inrush/stall, interrupt and coordination data |
| ESC1/ESC2 | 2 | Controller, >=30 A continuous at environment, electrical input limited to 600 W each; compatible with motor | Operate down to <=21 V and above 29.2 V plus transient review; command interface TBD |
| M1/M2 | 2 | Civilian thruster assemblies including phase leads; assumed 300 W cruise / 600 W peak electrical input each | Thrust, speed, motor/ESC compatibility, thermal duty |
| F3 | 1 | 10 A DC/DC input fuse and holder | Input inrush and interrupt data |
| D1 | 1 | Non-isolated DC/DC, regulated 12 V, 120 W; working input encompasses 21-30 V | Actual range, transient margin, EMC, efficiency and thermal derating |
| F4 | 1 | 1 A control fuse and holder | Coil inrush; relay input burden included in 4 W assumption |
| S1 / SR1 / K2 | 1 each | NC local propulsion stop / manual-reset permit relay / normally open watchdog permit relay | Exact hardware logic, no auto re-arm, failure behaviour and contact ratings |
| F5 | 1 | 7.5 A converter-output panel fuse and holder | Output short-circuit current must clear protection or safely current-limit |
| F6-F10 | 5 | Service fuses/holders: 3 A, 2 A, 2 A, 2 A, 2 A | Device inrush, fault behaviour, connector and wire ratings |
| A1 | 1 | Autopilot and I/O, 12 W assumption | 12 V compatibility, watchdog, controller interfaces |
| A2 | 1 | Computer/logger, 10 W assumption | 12 V input, data storage and timestamping |
| A3 | 1 | GNSS/heading module, 6 W assumption | 12 V input, interface and antenna installation |
| A4 | 1 | Telemetry radio, 12 W assumption | Peak TX power, supply inrush, legal radio use |
| P1 | 1 set | Temperature/conductivity/turbidity payload, combined 10 W assumption; RS-485 proposed | Sensor specifications, isolated transceiver needs and protocols |
| A5 | 1 set | Deck indication light 5 W; leak/temperature monitoring 5 W | Not a declaration of navigation-light compliance |
| ENC1 | 1 | Sealed service enclosure and mounting plate, assembled IP67 target | Heat rejection, condensation, seal and penetrations |
| Cable 25 | 2.4 conductor-m | Tinned stranded copper 25 mm2 | Actual derated ampacity >=80 A required, assumed 100 A |
| Cable 10 | 14.4 conductor-m | Tinned stranded copper 10 mm2 | Actual derated ampacity >=40 A required, assumed 50 A |
| Cable 2.5 | 6.0 conductor-m | Tinned stranded copper 2.5 mm2 | Actual derated ampacity >=10 A required, assumed 20 A |
| Cable 0.75 | 28.8 conductor-m | Tinned stranded copper 0.75 mm2 | Actual derated ampacity >=3 A required, assumed 5 A |
| Data / connectors | 1 provisional lot | CAN/RS-485 twisted pairs, Ethernet, sealed connectors X1-X6, glands, strain reliefs | Measured routes, pinouts, shield and termination plan TBD |
| Terminations | 1 provisional lot | Lugs/ferrules, covers, labels, clamps, fasteners and seal accessories | Terminal-count MTO follows detailed connection plan |

Cable quantities include 20% routing allowance and both current-carrying conductors. These are conductor-metres, not metres of two-core cable. Motor phase leads and data cables are excluded from these lengths and remain a vendor/route take-off. No mass or cost total is claimed.

# USV Electrical Architecture

**Pratik Prabhakar Shinde**

**Independent conceptual study — unbuilt and unvalidated.**

Electrical architecture for a small civilian unmanned surface vessel used for water-quality monitoring. The study covers battery distribution, twin propulsion feeders, regulated auxiliary supplies, sensor interfaces, cable sizing, protection screening and a preliminary material take-off.

[View the five-sheet drawing set](pdf/USV_Electrical_Drawings_RevE.pdf) · [DXF drawings](cad/) · [Engineering calculations](calculations/calculations.md)

![Main DC distribution and propulsion feeders](previews/E-002.svg)

## Design basis

The concept assumes a 2–3 m nonconductive vessel operating in sheltered water under visual supervision. A 25.6 V, 100 Ah LiFePO4 battery supplies two propulsion feeders and a regulated 12 V auxiliary bus. The mission target is two hours of environmental data collection.

| Parameter | Design assumption |
|---|---:|
| Battery planning voltage range | 22.4–29.2 V |
| Propulsion electrical demand | 2 × 300 W cruise; 2 × 600 W peak |
| Auxiliary and sensor demand | 60 W |
| DC/DC converter | 12 V, 120 W; assumed 90% efficiency |
| Usable SOC window | 80% |
| Separate capacity allowance | 90% |

The auxiliary load comprises the autopilot, GNSS, data logger, telemetry radio, water-quality sensors, indication and monitoring electronics.

## Calculated results

| Result | Estimate |
|---|---:|
| Battery demand at assumed cruise | 670.7 W |
| Planning energy | 1,843 Wh |
| Energy required for a two-hour mission | 1,341 Wh |
| Estimated endurance | 2.75 h |
| Main-plus-propulsion cable voltage drop | 0.464 V / 2.07% |
| Estimated endurance at 900 W combined propulsion | 1.90 h |

Results are analytical estimates based on the stated inputs. Propulsion demand, hull feasibility and battery mass remain to be established. Cable ampacities and fuse ratings are preliminary; installation derating, fault current, coordination and component compatibility require detailed design. The voltage-drop estimate excludes contact and protection-device losses.

## Drawing register

| Drawing | Title | Source | Preview |
|---|---|---|---|
| E-001 | Design basis, architecture and power budget | [DXF](cad/E-001.dxf) | [SVG](previews/E-001.svg) |
| E-002 | Main DC distribution and propulsion feeders | [DXF](cad/E-002.dxf) | [SVG](previews/E-002.svg) |
| E-003 | Auxiliary services and sensor interfaces | [DXF](cad/E-003.dxf) | [SVG](previews/E-003.svg) |
| E-004 | Propulsion permit and proposed commissioning procedures | [DXF](cad/E-004.dxf) | [SVG](previews/E-004.svg) |
| E-005 | Cable schedule, preliminary materials and drawing notes | [DXF](cad/E-005.dxf) | [SVG](previews/E-005.svg) |

The DXFs contain editable geometric entities, text and named layers. Sheet format is A3 landscape, with model-space coordinates in paper millimetres. Schematics are not to scale. Device tags and terminal allocations are conceptual references rather than selected manufacturer pinouts.

## Engineering documents

- [Requirements, design decisions and interfaces](docs/engineering_brief.md)
- [Preliminary bill of materials](docs/preliminary_bom.md)
- [Proposed commissioning procedures](docs/commissioning_plan.md)

## CAD tool and deliverables

**CAD tool: AutoCAD**

Electrical drawings are supplied as editable DXF R2013 files, with PDF and SVG plots. DXF operation in AutoCAD has been confirmed by the project author.

Calculation inputs are stored in `calculations/inputs.json`; the [calculation source](calculations/calculate.py) and [drawing source](scripts/build_cad.py) are included for reproducibility. Schematic geometry, protection ratings and annotations must be revised together when numerical inputs change.

## References

- [Victron Energy — Wiring Unlimited: DC wiring](https://www.victronenergy.com/media/pg/The_Wiring_Unlimited_book/en/dc-wiring.html)
- [Blue Sea Systems — Circuit Protection](https://www.bluesea.com/resources/96)

Manufacturer guidance supports the calculation method; loads and ampacity values are study assumptions. This project is independent of any employer and does not represent a certified or production-released vessel design.

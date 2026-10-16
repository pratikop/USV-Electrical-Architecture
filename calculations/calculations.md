# Calculation record

Independent conceptual study — unbuilt and unvalidated.

All inputs are design assumptions. No hull model, dynamic simulation or hardware measurement.

## Energy and power

Hotel load = 60 W at 12 V; DC/DC input = 66.67 W.
Cruise = 2 x 300 + 60/0.90 + 4 = 670.67 W.
Simultaneous peak = 2 x 600 + 60/0.90 + 4 = 1270.67 W.
Nominal energy = 25.6 x 100 = 2560 Wh.
Planning energy = nominal x 0.80 x 0.90 = 1843.2 Wh.
The 0.80 factor is the usable SOC window; 0.90 is a separate capacity/temperature/age allowance.
No propulsion efficiency factor is applied: thruster demand is assumed electrical input power.
Two-hour mission = 1341.3 Wh; energy margin = 37.4%.
Estimated endurance = 2.75 h. Not a range or sea-trial result.
Cable losses are not added to this coarse mission estimate; resistance calculations below expose them.
The allowance is not a substitute for later loss, mass, thermal and propulsion validation.

## Cable and fuse screening

I = P/V; R_loop = 2 L rho/A; deltaV = I R_loop; P_loss = I^2 R_loop.
rho = 0.0225 ohm mm2/m is an intentionally conservative copper resistance assumption.
Lengths are ONE WAY; resistance includes an equal-length dedicated copper return.
Currents use P/V at the reference bus voltage. Constant-power loads require a later iterative check including device drops.
1.25 x I <= fuse <= assumed derated ampacity is a project screening rule, not a compliance rule.
Ampacities below are placeholders, NOT verified cable-table or product values.

| Circuit | I A | 1.25 I A | L m | A mm2 | Fuse A | Assumed Iz A | Drop V | Drop % | Loss W |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C01 | 56.73 | 70.91 | 1 | 25 | 80 | 100 | 0.102 | 0.46 | 5.79 |
| C02 | 26.79 | 33.48 | 3 | 10 | 40 | 50 | 0.362 | 1.61 | 9.69 |
| C03 | 26.79 | 33.48 | 3 | 10 | 40 | 50 | 0.362 | 1.61 | 9.69 |
| C04 | 5.95 | 7.44 | 2 | 2.5 | 10 | 20 | 0.214 | 0.96 | 1.28 |
| C05 | 0.18 | 0.22 | 2 | 0.75 | 1 | 5 | 0.021 | 0.10 | 0.00 |
| C06 | 5.00 | 6.25 | 0.5 | 2.5 | 7.5 | 20 | 0.045 | 0.38 | 0.22 |

Main + propulsion feeder = 0.464 V (2.07% at 22.4 V), below the assumed 3% total DC-feeder target.
This excludes fuse, switch, contactor, connector and motor-phase losses. Remaining margin must cover them.
DC/DC terminal voltage bound = 22.4 - 0.316 = 22.084 V before contact losses.
Controller input bound is approximately 21.94 V; require operation at <=21 V minimum and >=29.2 V maximum, plus assessed transients.
At full 120 W converter rating, main current = 59.70 A; 1.25 I = 74.63 A < 80 A.
F0 80 A and F1/F2 40 A are candidate sizes only. A 2:1 ratio does not demonstrate selectivity.
Obtain time-current curves, inrush/stall limits, BMS trip data and prospective short-circuit current.
All protection and switching devices must be rated for DC (candidate voltage >=60 V DC).
Interrupt rating must exceed prospective fault current; no interrupt rating is released here.
BMS >=100 A continuous is an assumed procurement requirement; it is not the primary cable fuse.

## Endurance sensitivity

| Total propulsion input W | Calculated endurance h |
|---:|---:|
| 300 | 4.97 |
| 600 | 2.75 |
| 900 | 1.90 |

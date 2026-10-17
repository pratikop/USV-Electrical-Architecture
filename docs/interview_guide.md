# Interview preparation

**Independent conceptual study — unbuilt and unvalidated.**

## A truthful 60-second introduction

“I prepared an independent electrical concept for a small civilian water-quality monitoring USV. My professional background includes electrical drawings, material take-offs, system-upgrade analysis and retrofit inspections, including approximately 14 months at Zener Maritime. This study lets me demonstrate how I would structure requirements, power distribution, feeder calculations, a preliminary BOM and proposed commissioning checks. It has not been built, simulated dynamically, tested or certified. I am developing my skills in EPLAN, production harness design, automation programming and USV integration.”

Use this introduction after reviewing and understanding the package. Describe only the design reviews, software work and tests actually completed.

## Questions to rehearse

**Why 24 V?** At the same 1.2 kW electrical input, 12 V would require about 100 A while 24 V requires about 50 A. Lower current reduces I-squared-R losses for the same cable. The actual 22.4 V minimum is used for worst operating-current estimates. A 48 V alternative should be considered if propulsion power grows.

**Why is the endurance 2.75 hours?** 25.6 V x 100 Ah = 2560 Wh nominal. Apply an 80% usable SOC window and a separate 90% capacity allowance: 1843.2 Wh planning energy. Divide by 600 W propulsion + 60/0.90 W auxiliary input + 4 W coils = 670.7 W. This ignores explicit connection losses and is not a sea-trial promise. At 900 W propulsion the estimate falls to 1.90 h.

**Can you show a cable calculation?** For one 600 W feeder at 22.4 V, I = 26.8 A. Three metres one way, with a copper return, gives R = 2 x 3 x 0.0225 / 10 = 0.0135 ohm, so drop = 0.362 V. Add 0.102 V in the shared main feeder: about 0.464 V or 2.07%. Use the generated results for the exact value; terminal and protection-device losses are extra. Cable thermal ampacity still needs actual installation data.

**Are 40 A and 80 A fuses coordinated?** Unknown. The ratio alone proves nothing. I need fault current, device withstand, BMS behaviour, inrush and time-current/let-through curves before releasing fuse types and interrupt ratings.

**What happens when communications fail?** The proposed response is neutral then propulsion-permit removal after a one-second heartbeat timeout. No implementation is claimed. It can leave the craft drifting, so the concept assumes supervised sheltered-water operation and recovery support. Local stop bypasses the mission computer. A welded contactor remains an unresolved hardware failure.

**What is your biggest uncertainty?** Actual propulsion electrical demand and whether the battery mass is feasible. Next are cable derating, fault-current/coordination data, controller transients and stop-circuit integrity.

**Which parts map to the role?** Block diagrams, illustrative multi-line wiring, preliminary cable take-offs, functional BOM and proposed setting-to-work tests. These do not demonstrate five years of serial-ship design, production harness release, EPLAN competence or automation commissioning.

**What would you do next with a team?** Agree hull/mission/load requirements with mechanical and software colleagues, obtain vendor data, validate component interfaces, update the power/thermal/fault analysis, complete detailed terminal drawings and review the test plan before any build.

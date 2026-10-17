# Proposed commissioning procedures

Author: Pratik Prabhakar Shinde

**Independent conceptual study — unbuilt and unvalidated.**

These procedures define the intended verification sequence for a future implementation. They have not been executed. Acceptance targets are preliminary project criteria, subject to selected component limits and design review.

## Pre-energization

Confirm selected-device voltage/current ratings, battery fault-current data, fuse interrupt ratings and coordination, cable derating, polarity, return paths, terminal torque, strain relief and pack/BMS limits. Record the released drawing revision and instruments used.

## Auxiliary supply

Use a current-limited source over the intended input range, including feeder-drop allowance. Apply the 60 W auxiliary load and record converter input current, panel/end-device voltages and temperature. Proposed panel target: 11.4–12.6 V, with endpoints inside selected-device limits and no unintended reset.

## Propulsion feeder verification

Use an approved guarded load arrangement to emulate the assumed simultaneous propulsion demand. Measure main and branch voltage drops separately from device/contact drops. Proposed cable-only target: no more than 3% of 22.4 V. Confirm controller terminal voltages remain above undervoltage limits and conductor/terminal temperatures remain within their derated ratings.

## Permit and fault response

With propulsion disconnected or safely guarded, operate the local stop and inject a stale heartbeat. The proposed response retains auxiliary power, removes propulsion permit and requires deliberate manual re-arm. Local-stop power-removal target: 0.5 s or less. Proposed heartbeat timeout: more than 1 s. Record contactor drop-out and transient behaviour. Power removal does not demonstrate zero thrust or stopped vessel motion.

## Environmental and operational verification

Follow an approved enclosure ingress procedure and manufacturer-compatible wet motor testing. A later sheltered-water endurance trial would log voltage, current, energy, SOC, temperatures and operating conditions over the two-hour mission, with recovery support available.

Do not deliberately short the battery or dry-run water-cooled thrusters. Fault-current and fuse-clearing assessment uses supplier data and qualified analysis rather than destructive pack testing. For each procedure, retain instrument identification, operating conditions, measured values, acceptance assessment and evidence.

"""Analytical estimates only. Standard-library Python; no simulation or measurements.
Edit inputs.json, run python3 calculate.py. Outputs are reproducible snapshots.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def calculate(a):
    hotel = sum(a['hotel_loads_w'].values())
    overhead = hotel / a['dc_dc_efficiency'] + a['control_coils_w']
    cruise = a['propulsion_count'] * a['propulsion_cruise_w_each'] + overhead
    peak = a['propulsion_count'] * a['propulsion_peak_w_each'] + overhead
    energy = a['battery_nominal_v'] * a['battery_ah']
    usable = energy * a['usable_soc_fraction'] * a['capacity_allowance']
    powers = {'total_peak':peak, 'motor_peak':a['propulsion_peak_w_each'],
              'converter_rating':a['dc_dc_output_rating_w']/a['dc_dc_efficiency'],
              'coils':a['control_coils_w'], 'hotel':hotel}
    rows = []
    for c in a['circuits']:
        current = powers[c['load']] / c['voltage_v']
        resistance = 2*c['length_one_way_m']*a['rho_ohm_mm2_per_m']/c['area_mm2']
        drop = current * resistance
        design = current*a['design_current_factor']
        rows.append(dict(c, current_a=current, design_current_a=design,
                         loop_resistance_ohm=resistance, drop_v=drop,
                         drop_pct=100*drop/c['voltage_v'], cable_loss_w=current**2*resistance,
                         provisional_inequality=design<=c['fuse_a']<=c['assumed_derated_ampacity_a']))
    # End-to-end sums use main feeder at simultaneous peak as a conservative bound.
    motor_drop = rows[0]['drop_v']+rows[1]['drop_v']
    converter_drop = rows[0]['drop_v']+rows[3]['drop_v']
    # Main feeder screening at full converter rating, rather than 60 W hotel demand.
    full_converter_peak = a['propulsion_count']*a['propulsion_peak_w_each']+powers['converter_rating']+a['control_coils_w']
    return {'status':a['status'], 'method':'Analytical estimates, not simulation or measurement',
            'hotel_w':hotel, 'cruise_battery_w':cruise, 'peak_battery_w':peak,
            'nominal_energy_wh':energy, 'planning_energy_wh':usable,
            'mission_energy_wh':cruise*a['mission_h'], 'estimated_endurance_h':usable/cruise,
            'energy_margin_fraction':usable/(cruise*a['mission_h'])-1,
            'peak_battery_current_a':peak/a['battery_min_v'],
            'main_full_converter_current_a':full_converter_peak/a['battery_min_v'],
            'main_full_converter_design_current_a':full_converter_peak/a['battery_min_v']*a['design_current_factor'],
            'propulsion_path_drop_v':motor_drop, 'propulsion_path_drop_pct':motor_drop/a['battery_min_v']*100,
            'converter_path_drop_v':converter_drop,
            'circuits':rows,
            'sensitivity':[{'total_propulsion_w':p, 'endurance_h':usable/(p+overhead)} for p in (300,600,900)]}

if __name__ == '__main__':
    a = json.loads((ROOT/'inputs.json').read_text())
    r = calculate(a)
    (ROOT/'results.json').write_text(json.dumps(r, indent=2, ensure_ascii=False)+'\n')
    lines = ['# Calculation record', '', a['status'], '',
             'All inputs are design assumptions. No hull model, dynamic simulation or hardware measurement.', '',
             '## Energy and power', '',
             f"Hotel load = {r['hotel_w']:.0f} W at 12 V; DC/DC input = {r['hotel_w']/a['dc_dc_efficiency']:.2f} W.",
             f"Cruise = 2 x 300 + 60/0.90 + 4 = {r['cruise_battery_w']:.2f} W.",
             f"Simultaneous peak = 2 x 600 + 60/0.90 + 4 = {r['peak_battery_w']:.2f} W.",
             f"Nominal energy = 25.6 x 100 = {r['nominal_energy_wh']:.0f} Wh.",
             f"Planning energy = nominal x 0.80 x 0.90 = {r['planning_energy_wh']:.1f} Wh.",
             'The 0.80 factor is the usable SOC window; 0.90 is a separate capacity/temperature/age allowance.',
             'No propulsion efficiency factor is applied: thruster demand is assumed electrical input power.',
             f"Two-hour mission = {r['mission_energy_wh']:.1f} Wh; energy margin = {100*r['energy_margin_fraction']:.1f}%.",
             f"Estimated endurance = {r['estimated_endurance_h']:.2f} h. Not a range or sea-trial result.",
             'Cable losses are not added to this coarse mission estimate; resistance calculations below expose them.',
             'The allowance is not a substitute for later loss, mass, thermal and propulsion validation.', '',
             '## Cable and fuse screening', '',
             'I = P/V; R_loop = 2 L rho/A; deltaV = I R_loop; P_loss = I^2 R_loop.',
             'rho = 0.0225 ohm mm2/m is an intentionally conservative copper resistance assumption.',
             'Lengths are ONE WAY; resistance includes an equal-length dedicated copper return.',
             'Currents use P/V at the reference bus voltage. Constant-power loads require a later iterative check including device drops.',
             '1.25 x I <= fuse <= assumed derated ampacity is a project screening rule, not a compliance rule.',
             'Ampacities below are placeholders, NOT verified cable-table or product values.', '',
             '| Circuit | I A | 1.25 I A | L m | A mm2 | Fuse A | Assumed Iz A | Drop V | Drop % | Loss W |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for c in r['circuits']:
        lines.append(f"| {c['id']} | {c['current_a']:.2f} | {c['design_current_a']:.2f} | {c['length_one_way_m']} | {c['area_mm2']} | {c['fuse_a']} | {c['assumed_derated_ampacity_a']} | {c['drop_v']:.3f} | {c['drop_pct']:.2f} | {c['cable_loss_w']:.2f} |")
    lines += ['', f"Main + propulsion feeder = {r['propulsion_path_drop_v']:.3f} V ({r['propulsion_path_drop_pct']:.2f}% at 22.4 V), below the assumed 3% total DC-feeder target.",
              'This excludes fuse, switch, contactor, connector and motor-phase losses. Remaining margin must cover them.',
              f"DC/DC terminal voltage bound = 22.4 - {r['converter_path_drop_v']:.3f} = {22.4-r['converter_path_drop_v']:.3f} V before contact losses.",
              'Controller input bound is approximately 21.94 V; require operation at <=21 V minimum and >=29.2 V maximum, plus assessed transients.',
              f"At full 120 W converter rating, main current = {r['main_full_converter_current_a']:.2f} A; 1.25 I = {r['main_full_converter_design_current_a']:.2f} A < 80 A.",
              'F0 80 A and F1/F2 40 A are candidate sizes only. A 2:1 ratio does not demonstrate selectivity.',
              'Obtain time-current curves, inrush/stall limits, BMS trip data and prospective short-circuit current.',
              'All protection and switching devices must be rated for DC (candidate voltage >=60 V DC).',
              'Interrupt rating must exceed prospective fault current; no interrupt rating is released here.',
              'BMS >=100 A continuous is an assumed procurement requirement; it is not the primary cable fuse.',
              '', '## Endurance sensitivity', '', '| Total propulsion input W | Calculated endurance h |', '|---:|---:|']
    lines += [f"| {s['total_propulsion_w']} | {s['endurance_h']:.2f} |" for s in r['sensitivity']]
    (ROOT/'calculations.md').write_text('\n'.join(lines)+'\n')
    assert all(c['provisional_inequality'] for c in r['circuits'])
    assert r['propulsion_path_drop_pct'] < 3
    print(f"Analytical checks complete: {r['cruise_battery_w']:.2f} W cruise, {r['estimated_endurance_h']:.2f} h estimated endurance.")

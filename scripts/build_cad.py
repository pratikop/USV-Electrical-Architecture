"""Generate editable AutoCAD-compatible DXF and matching A3 PDF/SVG plots.
Geometric electrical symbols are simplified conventions, not a certified symbol library.
No AutoCAD instance is used. DXF R2013, model space in paper millimetres, plot 1:1.
"""
from pathlib import Path
import json, math, shutil
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black, white, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/'calculations'))
from calculate import calculate
INPUTS=json.loads((ROOT/'calculations'/'inputs.json').read_text())
RESULTS=calculate(INPUTS)
STATUS='Independent conceptual study — unbuilt and unvalidated.'
CW,CH=420,297

class Sheet:
    def __init__(self,number,title):
        self.number=number;self.title=title;self.ops=[]
        self.doc=ezdxf.new('R2013');self.doc.units=4
        self.doc.header['$MEASUREMENT']=1
        self.doc.linetypes.new('STUDY_DASHED',dxfattribs={'description':'Concept mechanical link','pattern':[2.4,1.4,-1.0]})
        for name,col,lw in [('BORDER',7,35),('POWER',7,35),('RETURN',4,25),('CONTROL',3,25),('DEVICE',7,25),('TEXT',7,18),('NOTES',8,18),('TERMINAL',7,25)]:
            self.doc.layers.new(name,dxfattribs={'color':col,'lineweight':lw})
        self.doc.styles.new('CAD_TEXT',dxfattribs={'font':'txt'})
        self.m=self.doc.modelspace()
        self.frame()
    def line(self,x1,y1,x2,y2,layer='POWER',dashed=False):
        self.m.add_line((x1,y1),(x2,y2),dxfattribs={'layer':layer,'linetype':'STUDY_DASHED' if dashed else 'BYLAYER'})
        self.ops.append(('line',x1,y1,x2,y2,layer,dashed))
    def rect(self,x,y,w,h,layer='DEVICE'):
        for a,b,c,d in [(x,y,x+w,y),(x+w,y,x+w,y+h),(x+w,y+h,x,y+h),(x,y+h,x,y)]:self.line(a,b,c,d,layer)
    def circle(self,x,y,r=1.1,layer='TERMINAL',filled=False):
        if filled:
            self.m.add_solid([(x-r,y-r),(x+r,y-r),(x-r,y+r),(x+r,y+r)],dxfattribs={'layer':layer})
        else:
            self.m.add_circle((x,y),r,dxfattribs={'layer':layer})
        self.ops.append(('circle',x,y,r,filled))
    def text(self,x,y,t,h=2.5,layer='TEXT'):
        self.m.add_text(t,dxfattribs={'height':h,'style':'CAD_TEXT','layer':layer,'insert':(x,y)})
        self.ops.append(('text',x,y,t,h,layer))
    def lines(self,x,y,items,h=2.5,step=4.4):
        for i,t in enumerate(items):self.text(x,y-i*step,t,h)
    def node(self,x,y):self.circle(x,y,.65,filled=True)
    def terminal(self,x,y,label,above=True):
        self.circle(x,y,1.1);self.text(x-4,y+(3 if above else -5),label,2.1)
    def block(self,x,y,w,h,tag,desc):
        self.rect(x,y,w,h);self.text(x+2,y+h-5,tag,3)
        self.lines(x+2,y+h-10,desc,h=2.3,step=4)
    def fuse(self,x,y,tag,rating,wire=''):
        self.line(x-7,y,x-3,y);self.rect(x-3,y-1.8,6,3.6)
        self.line(x-2.3,y-1.1,x+2.3,y+1.1,'DEVICE');self.line(x+3,y,x+7,y)
        self.text(x-6,y+5,tag,2.7);self.text(x-6,y-6,rating,2.2)
        if wire:self.text(x+9,y+2,wire,2)
    def no(self,x,y,tag,label='',nc=False):
        self.line(x-6,y,x-2,y,'CONTROL');self.line(x+2,y,x+6,y,'CONTROL')
        self.line(x-2,y-2,x-2,y+2,'DEVICE');self.line(x+2,y-2,x+2,y+2,'DEVICE')
        if nc:self.line(x-3,y-2.7,x+3,y+2.7,'DEVICE')
        self.text(x-6,y+5,tag,2.6)
        if label:self.text(x-6,y-6,label,2.1)
    def coil(self,x,y,tag):
        self.rect(x-5,y-3,10,6);self.line(x-9,y,x-5,y,'CONTROL');self.line(x+5,y,x+9,y,'CONTROL')
        self.text(x-4,y+6,tag,2.7);self.text(x-5,y-7,'A1   A2',2)
    def frame(self):
        self.rect(10,10,400,277,'BORDER')
        for i in range(8):
            x=10+i*50;self.line(x,284,x,287,'BORDER');self.text(x+23,288,str(i+1),2)
        for i,z in enumerate('ABCDE'):
            y=55+i*46;self.text(5,y,z,2.4);self.text(412,y,z,2.4)
        self.text(16,277,self.number+'  '+self.title.upper(),4)
        self.text(16,269,STATUS,2.6)
        self.line(10,263,410,263,'BORDER')
        self.line(10,47,410,47,'BORDER')
        self.text(15,38,'ENV-USV-01  |  CIVILIAN WATER-QUALITY MONITORING',3)
        self.text(15,30,self.title,3.2)
        self.text(15,22,'Prepared for: Pratik Prabhakar Shinde   |   CONCEPT DESIGN / FOR DISCUSSION',2.4)
        self.text(15,15,'DXF generated with Python. Not drafted or validated inside AutoCAD.',2.2)
        self.line(285,10,285,47,'BORDER');self.line(350,10,350,47,'BORDER')
        self.text(289,39,'DRAWING: '+self.number,2.7);self.text(289,31,'REV: C / 17 OCT 2026',2.5)
        self.text(289,23,'CHECK: NOT REVIEWED',2.5);self.text(289,15,'APPROVAL: NOT ISSUED',2.4)
        self.text(354,39,'A3 / 420 x 297 mm',2.5);self.text(354,31,'SCALE: NTS',2.5)
        self.text(354,23,'UNITS: mm (sheet)',2.3);self.text(354,15,'PLOT: 1:1 / LANDSCAPE',2.1)
    def table(self,x,y,widths,headers,rows,row_h=9,h=2.4):
        height=(len(rows)+1)*row_h;self.rect(x,y-height,sum(widths),height)
        xx=x
        for w in widths[:-1]:xx+=w;self.line(xx,y-height,xx,y,'DEVICE')
        for i in range(1,len(rows)+1):self.line(x,y-i*row_h,x+sum(widths),y-i*row_h,'DEVICE')
        for i,row in enumerate([headers]+rows):
            xx=x
            for t,w in zip(row,widths):self.text(xx+2,y-i*row_h-row_h*.64,str(t),h);xx+=w
        return y-height
    def save(self):
        self.doc.set_modelspace_vport(297,center=(210,148.5))
        p=ROOT/'cad'/f'{self.number}.dxf';self.doc.saveas(p)
        audit=ezdxf.readfile(p).audit()
        if audit.has_errors:raise ValueError(str(audit.errors))
        self.svg(ROOT/'previews'/f'{self.number}.svg')
    def plot(self,c):
        c.saveState();c.scale(mm,mm)
        for o in self.ops:
            if o[0]=='line':
                _,x1,y1,x2,y2,layer,dash=o;c.setStrokeColor(black);c.setLineWidth(.35 if layer in ('BORDER','POWER') else .18)
                c.setDash([1.4,1] if dash else []);c.line(x1,y1,x2,y2)
            elif o[0]=='circle':
                _,x,y,r,filled=o;c.setDash([]);c.setLineWidth(.2);c.setFillColor(black if filled else white);c.circle(x,y,r,fill=1,stroke=1)
            else:
                _,x,y,t,h,_=o;c.setFillColor(black);c.setFont('EngineeringText',h*1.25);c.drawString(x,y,t)
        c.restoreState();c.showPage()
    def svg(self,path):
        parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 297" width="1680" height="1188"><rect width="420" height="297" fill="white"/>']
        for o in self.ops:
            if o[0]=='line':
                _,x1,y1,x2,y2,layer,dash=o;sw=.35 if layer in ('BORDER','POWER') else .18
                parts.append(f'<line x1="{x1}" y1="{297-y1}" x2="{x2}" y2="{297-y2}" stroke="black" stroke-width="{sw}"/>')
            elif o[0]=='circle':
                _,x,y,r,filled=o;parts.append(f'<circle cx="{x}" cy="{297-y}" r="{r}" fill="{"black" if filled else "white"}" stroke="black" stroke-width=".2"/>')
            else:
                _,x,y,t,h,_=o;parts.append(f'<text x="{x}" y="{297-y}" font-family="Arial,Helvetica,sans-serif" font-size="{h*1.3}">{escape(t)}</text>')
        parts.append('</svg>');path.write_text('\n'.join(parts),encoding='utf-8')

def basis():
    s=Sheet('E-001','Design basis, single-line architecture and power budget')
    s.text(16,253,'1. DESIGN BASIS',3.2)
    s.lines(16,246,['Mission: 2 h sheltered-water environmental survey; visual supervision and recovery support.',
                     'Nonconductive 2-3 m hull assumed. Displacement, speed, thrust and battery mass are unresolved.',
                     'B1: 8S LiFePO4 / 25.6 V nominal / 100 Ah / planning range 22.4-29.2 V.',
                     'No charger aboard. Remove/isolate pack for approved shore charging. No AC system in scope.'],h=2.6,step=5.5)
    s.text(16,216,'2. FUNCTIONAL SINGLE-LINE (RETURNS OMITTED ON THIS SHEET)',3.2)
    s.block(16,177,53,28,'B1 + BMS',['25.6 V / 100 Ah','BMS >=100 A assumed'])
    s.line(69,191,83,191);s.block(83,177,56,28,'F0 / Q0',['80 A main fuse','2-pole manual isolator'])
    s.line(139,191,155,191);s.line(155,153,155,191)
    s.line(155,191,172,191);s.block(172,177,53,28,'K1 / F1-F2',['Propulsion contactor','2 x 40 A DC feeders'])
    s.line(225,191,240,191);s.line(240,180,240,202)
    s.line(240,202,257,202);s.block(257,193,66,21,'ESC1 / M1',['Port: 300 / 600 W'])
    s.line(240,180,257,180);s.block(257,169,66,21,'ESC2 / M2',['Stbd: 300 / 600 W'])
    s.line(155,153,172,153);s.block(172,138,65,27,'F3 / D1 / F5',['24 V class -> 12 V','120 W DC/DC; 7.5 A out'])
    s.line(237,151,257,151);s.block(257,138,138,27,'F6-F10 / 12 V SERVICES',['Autopilot, GNSS, logger, telemetry, payload','60 W baseline; detailed branches on E-003'])
    s.text(16,126,'3. POWER BUDGET - ASSUMED ELECTRICAL INPUTS',3.2)
    s.table(16,120,[106,34,34,60],['LOAD','CRUISE W','PEAK W','BASIS'],[
        ['Propulsion (2 thrusters)','600','1200','2 x 300 / 600 W'],
        ['12 V services','60','60','D1 output load'],
        ['D1 conversion loss','6.7','6.7','90% efficiency'],
        ['Permit/control coils','4','4','Allowance incl. relay drives'],
        ['TOTAL AT BATTERY','670.7','1270.7','Simultaneous peak']],row_h=9,h=2.4)
    s.lines(263,118,['ENERGY ESTIMATE (NOT MEASURED)',
        'Nominal: 25.6 x 100 = 2560 Wh',
        f"Planning: {RESULTS['planning_energy_wh']:.0f} Wh (SOC x capacity factors)",
        f"Mission: {RESULTS['cruise_battery_w']:.1f} W x {INPUTS['mission_h']:g} h = {RESULTS['mission_energy_wh']:.0f} Wh",
        f"Estimated endurance: {RESULTS['estimated_endurance_h']:.2f} h",
        f"At 900 W propulsion: {RESULTS['sensitivity'][2]['endurance_h']:.2f} h",
        'Cable/contact losses not explicitly added.',
        'See calculations/calculations.md.'],h=2.45,step=6.8)
    return s

def main_power():
    s=Sheet('E-002','Main DC distribution and propulsion feeders')
    s.text(16,253,'POWER CIRCUITS / SIMPLIFIED DEVICE SYMBOLS / ALL CONTACTS SHOWN DE-ENERGIZED',3)
    # + and - rails with double-pole isolation
    s.text(16,233,'B1 +',3);s.line(34,234,48,234);s.fuse(55,234,'-F0','80 A')
    s.line(62,234,81,234);s.no(87,234,'-Q0:1','1-2');s.line(93,234,125,234)
    s.text(16,187,'B1 -',3);s.line(34,188,81,188,'RETURN');s.no(87,188,'-Q0:2','3-4');s.line(93,188,400,188,'RETURN')
    s.line(87,198,87,223,'NOTES',dashed=True);s.text(16,201,'Q0 POLES MECHANICALLY LINKED',2.2)
    s.text(16,221,'C01 +/- : 25 mm2; 1 m each',2.35);s.text(16,215,'F0 adjacent to battery +.',2.35)
    s.line(125,234,125,204);s.node(125,234);s.line(125,234,159,234)
    s.no(165,234,'-K1:1','1/L1-2/T1');s.line(171,234,210,234)
    s.line(210,234,210,214);s.node(210,234)
    s.line(210,234,228,234);s.fuse(235,234,'-F1','40 A');s.line(242,234,273,234)
    s.terminal(261,234,'X2:1');s.text(246,241,'W101',2.2)
    s.block(273,222,46,27,'-ESC1',['DC+ : 1','DC- : 2']);s.line(296,222,296,188,'RETURN');s.node(296,188)
    s.line(319,235,344,235);s.block(344,222,51,27,'-M1',['Port thruster','Vendor phase leads'])
    s.text(324,239,'U/V/W',2.2);s.text(299,211,'W102 / X2:2',2.2)
    s.text(247,215,'C02: 2 x 10 mm2 / 3 m one way',2.4)
    s.line(210,214,210,163);s.line(210,163,228,163);s.fuse(235,163,'-F2','40 A')
    s.line(242,163,273,163);s.terminal(261,163,'X3:1');s.text(246,170,'W111',2.2)
    s.block(273,151,46,27,'-ESC2',['DC+ : 1','DC- : 2'])
    # return routed to right of rail branch, no ambiguous crossing connections
    s.line(296,151,296,140,'RETURN');s.line(296,140,400,140,'RETURN');s.line(400,140,400,188,'RETURN');s.node(400,188)
    s.text(302,143,'W112 / X3:2',2.2)
    s.line(319,164,344,164);s.block(344,151,51,27,'-M2',['Stbd thruster','Vendor phase leads']);s.text(324,169,'U/V/W',2.2)
    s.text(247,133,'C03: 2 x 10 mm2 / 3 m one way',2.4)
    # nonprop service links above return rail, separate off-sheet references
    s.line(125,204,165,204);s.text(130,210,'W020 / DC+ TO E-003:A',2.25);s.circle(165,204,.8)
    s.node(125,204);s.line(125,204,125,178);s.line(125,178,165,178);s.text(128,171,'W030 / DC+ TO E-004:A',2.25);s.circle(165,178,.8)
    s.line(116,188,116,154,'RETURN');s.node(116,188);s.line(116,154,165,154,'RETURN');s.text(119,146,'W000 / RETURN TO E-003:B, E-004:B',2.1)
    s.text(16,121,'FEEDER / PROTECTION CALCULATION BASIS',3)
    s.table(16,115,[36,37,36,36,37,52],['CIRCUIT','I (A)','1.25 I','mm2','FUSE A','DROP V'],[
        ['C01 main','56.73','70.91','25','80','0.102'],
        ['C02 / C03','26.79','33.48','10','40','0.362 each'],
        ['C04 D1 in','5.95','7.44','2.5','10','0.214 at 120 W']],row_h=9,h=2.3)
    s.lines(260,113,['I = P / 22.4 V; Rloop = 2 L rho / A',
        'rho = 0.0225 ohm mm2/m (assumed)',
        'Main + motor feeder: 0.464 V / 2.07%',
        'Excludes contact/fuse/switch losses.',
        'Wire numbers identify conductors, not vendor pins.',
        'No dot at wire crossing = no connection.'],h=2.3,step=5.4)
    s.lines(16,68,['HOLD: cable ampacity / battery fault current / fuse interrupt rating and selectivity / ESC inrush, UV and regeneration.',
        'Switchgear voltage rating >=60 V DC is a target; actual DC breaking capability and fault withstand must be checked.'],h=2.4,step=5.3)
    return s

def services():
    s=Sheet('E-003','12 V services, field terminals and sensor interfaces')
    s.text(16,253,'24 V CLASS TO 12 V SUPPLY / NON-ISOLATED CONVERTER / DEDICATED COPPER RETURNS',3)
    s.text(16,234,'A / W020 FROM E-002',2.5);s.line(62,226,80,226);s.fuse(87,226,'-F3','10 A')
    s.line(94,226,120,226);s.text(98,232,'W201',2.2)
    s.block(120,204,76,33,'-D1 / 120 W',['IN+ 1 / IN- 2','OUT+ 3 / OUT- 4','12 V regulated / 90% assumed'])
    s.line(196,226,217,226);s.fuse(224,226,'-F5','7.5 A');s.line(231,226,246,226)
    s.text(203,239,'C06: 2 x 2.5 mm2 / 0.5 m',2.3)
    s.line(246,226,246,89);s.text(251,233,'W210 / +12 V PANEL',2.3)
    s.text(16,193,'B / W000 FROM E-002',2.5);s.line(62,185,145,185,'RETURN');s.line(145,185,145,204,'RETURN')
    s.line(182,204,182,177,'RETURN');s.line(182,177,401,177,'RETURN');s.line(401,177,401,82,'RETURN')
    s.text(198,180,'W200 / 12 V RETURN (COMMON DC NEGATIVE)',2.25)
    s.text(16,215,'C04: 2 x 2.5 mm2 / 2 m',2.2)
    loads=[(164,'F6','3 A','A1 / A3','Autopilot + GNSS','18 W / 1.50 A','X4:1/2','W211 / W212'),
           (146,'F7','2 A','A2','Computer / logger','10 W / 0.83 A','X4:3/4','W221 / W222'),
           (128,'F8','2 A','A4','Telemetry radio','12 W / 1.00 A','X4:5/6','W231 / W232'),
           (110,'F9','2 A','P1','Water-quality payload','10 W / 0.83 A','X5:1/2','W241 / W242'),
           (92,'F10','2 A','A5','Indication / monitoring','10 W / 0.83 A','X4:7/8','W251 / W252')]
    for y,tag,rat,load,desc,power,term,wire in loads:
        s.node(246,y);s.line(246,y,258,y);s.fuse(265,y,'-'+tag,rat)
        s.line(272,y,305,y);s.terminal(290,y,term.split('/')[0]);s.text(276,y-6,wire,1.95)
        s.rect(305,y-6,82,12);s.text(308,y+1,load+'  '+desc,2.4);s.text(308,y-3.4,power,2.2)
        s.line(387,y,401,y,'RETURN');s.node(401,y)
    s.text(16,166,'FIELD INTERFACE ALLOCATION',3)
    s.table(16,159,[20,46,37,93],['TERM','SIGNAL','CONDUCTOR','REMARK'],[
        ['X5:1','+12 V','W241','From F9'],['X5:2','DC RETURN','W242','To W200'],
        ['X5:3','RS-485 A','D301','Twisted pair; vendor labels TBD'],
        ['X5:4','RS-485 B','D302','To logger serial interface'],
        ['X4','Services +/-','See branches','Odd + / even return; logical only']],row_h=9,h=2.2)
    s.lines(16,94,['All terminal allocations are study references, NOT manufacturer pinouts.',
        'Data/shield/termination requirements depend on selected devices.',
        'Motor command links and antenna/feedthrough installation not detailed.'],h=2.3,step=5.2)
    s.lines(16,70,['BRANCH WIRING: <=2 m one way; + and return each 0.75 mm2. Baseline 12 V load = 5.0 A.',
        'Worst branch drop 0.180 V; plus C06 0.045 V = 0.225 V / 1.88%. Contact losses extra.',
        'F5 limits usable panel load below D1 full 120 W rating. Recheck protection before adding payloads.'],h=2.4,step=5.2)
    return s

def controls():
    s=Sheet('E-004','Propulsion permit concept and commissioning checks')
    s.text(16,253,'HARDWARE PERMIT PATH - FUNCTIONAL CONTACT DIAGRAM, NOT A RELEASED SAFETY CIRCUIT',3)
    s.text(16,237,'A / W030 FROM E-002',2.5)
    y=220
    s.line(23,y,46,y,'CONTROL');s.fuse(53,y,'-F4','1 A');s.line(60,y,89,y,'CONTROL')
    s.no(95,y,'-S1','11-12 / NC',nc=True);s.line(101,y,147,y,'CONTROL')
    s.no(153,y,'-SR1','13-14 / NO');s.line(159,y,205,y,'CONTROL')
    s.no(211,y,'-K2','13-14 / NO');s.line(217,y,267,y,'CONTROL')
    s.coil(276,y,'-K1');s.line(285,y,384,y,'RETURN');s.text(322,y+5,'B / W000 TO E-002',2.3)
    s.text(66,y+11,'W301',2.3);s.text(113,y+11,'W302',2.3);s.text(169,y+11,'W303',2.3);s.text(229,y+11,'W304',2.3)
    s.text(16,201,'C05: 0.75 mm2; 2 m equivalent loop assumption; suppression and relay supply wiring are not detailed.',2.5)
    s.block(16,151,108,36,'-SR1 / MANUAL PERMIT',['Functional module; not selected.',
        'Requires deliberate reset/arm action.',
        'No auto re-arm after power/stop reset.',
        'Reset and feedback terminals TBD.'])
    s.block(141,151,113,36,'-K2 / WATCHDOG PERMIT',['NO contact only while heartbeat valid.',
        '>1 s timeout -> neutral, then open K1.',
        'HW/SW implementation not provided.',
        'Failure-high behaviour unresolved.'])
    s.block(271,151,124,36,'-K1 / PROPULSION CONTACTOR',['Main contact on E-002; hotel stays live.',
        'Auxiliary feedback needed for fault detection.',
        'Coil suppression / drop-out time TBD.',
        'Welded contact can defeat isolation.'])
    s.text(16,140,'PROPOSED TESTS - ALL NOT RUN / RECORD INSTRUMENTS, CONDITIONS, VALUES, PASS/FAIL AND EVIDENCE',2.7)
    s.table(16,132,[31,82,249],['TEST','METHOD','PROPOSED ACCEPTANCE / HOLD POINT'],[
        ['T01-03','Pre-energization review','Datasheets, fault current, polarity, torque, return continuity and BMS limits approved.'],
        ['T04','Current-limited supply','12 V panel remains 11.4-12.6 V at 60 W; no reset over intended input range.'],
        ['T05','Guarded load emulation','Cable-only propulsion path drop <=3%; ESC input above UV limit; thermal limits met.'],
        ['T06-07','Stop / heartbeat loss','Proposed K1 power removal <=0.5 s on local stop; >1 s timeout response; manual re-arm.'],
        ['T08-09','Ingress / wet motor setup','Approved facility/procedure; record transients; fault/feedback response reviewed.'],
        ['T10','Supervised water trial','2 h within pack/SOC/thermal limits; log V/I/Wh and conditions; recovery support.']],row_h=9.5,h=2.25)
    s.lines(16,57,['No deliberate pack short circuit. No dry-running water-cooled thrusters. Power removal does not prove stopped thrust or vessel motion.'],h=2.4)
    return s

def schedule():
    s=Sheet('E-005','Cable schedule, preliminary materials and drawing notes')
    s.text(16,253,'CABLE TAKE-OFF - CONDUCTOR-METRES, INCLUDING 20% ROUTING ALLOWANCE',3)
    s.table(16,246,[24,129,31,35,31,31,79],['ID','FROM / TO','L ONE-WAY','CORE mm2','CORES','PROV. m','PROTECTION / HOLD'],[
        ['C01','B1 / F0 / Q0 / DC bars','1.0 m','25','2','2.4','F0 80 A / assumed Iz 100 A'],
        ['C02','K1 / F1 / ESC1 + return','3.0 m','10','2','7.2','F1 40 A / assumed Iz 50 A'],
        ['C03','K1 / F2 / ESC2 + return','3.0 m','10','2','7.2','F2 40 A / assumed Iz 50 A'],
        ['C04','F3 / D1 input + return','2.0 m','2.5','2','4.8','F3 10 A / assumed Iz 20 A'],
        ['C05','F4 / stop-permit / K1 coil','2.0 m eq.','0.75','2 eq.','4.8','F4 1 A / assumed Iz 5 A'],
        ['C06','D1 / F5 / 12 V panel','0.5 m','2.5','2','1.2','F5 7.5 A / assumed Iz 20 A'],
        ['12V-BR','F6-F10 / service loads','2 m each','0.75','2 x 5','24.0','F6 3 A; F7-F10 2 A']],row_h=8,h=2.1)
    s.text(16,172,'PRELIMINARY FUNCTIONAL BOM (NO PART NUMBERS OR COST CLAIM)',3)
    s.table(16,165,[45,18,154,143],['TAG','QTY','FUNCTIONAL SPECIFICATION','RELEASE HOLD'],[
        ['B1 / F0 / Q0','1 set','25.6 V 100 Ah; 80 A fuse; >=100 A isolator','Fault current, BMS, DC break, mass'],
        ['K1 / ESC / M','1/2/2','>=100 A contactor; 600 W peak per propulsion branch','ESC UV <=21 V; inrush / regen / cooling'],
        ['D1 / F3-F10','1 set','12 V 120 W DC/DC and branch fuse/holder set','Actual voltage range, protection coordination'],
        ['S1 / SR1 / K2','1 each','NC local stop; manual permit; watchdog permit','Exact reset / feedback and fault behaviour'],
        ['A1-A5 / P1','1 set','Autopilot, GNSS, logger, radio, monitoring, sensors','Supply compatibility, data protocols and EMC'],
        ['ENC / cabling','1 lot','Sealed enclosure, glands, connectors, copper, terminals','IP67 assembly target; heat / corrosion review']],row_h=8,h=2.2)
    s.text(16,101,'GENERAL DRAWING / DESIGN NOTES',3)
    s.lines(16,94,[
        '1. NTS schematic sheets. Model-space coordinates are paper mm. Open DXF in AutoCAD; plot A3 landscape 1:1.',
        '2. Simplified conventional symbols only. Tags/terminal allocations are illustrative, not vendor connection instructions.',
        '3. All ampacities are assumptions. Validate installation derating, connector ratings and fuse curves before design release.',
        '4. Single battery, BMS and converter remain common failure points. No redundancy or standards compliance is claimed.',
        '5. Rev C: clearer review status, linked energy calculations and engineering evidence/review records; no hardware change.',
        '6. Sources: Victron Wiring Unlimited, DC wiring; Blue Sea Systems Circuit Protection. Full links in docs/engineering_brief.md.',
        '7. No drawings created in AutoCAD, hardware measurements, dynamic simulation or employer involvement are claimed.'
    ],h=2.35,step=5.25)
    return s

if __name__=='__main__':
    font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    if font.exists():pdfmetrics.registerFont(TTFont('EngineeringText',str(font)))
    else:pdfmetrics.registerFont(pdfmetrics.Font('EngineeringText','Helvetica','WinAnsiEncoding'))
    sheets=[basis(),main_power(),services(),controls(),schedule()]
    pdf=ROOT/'pdf'/'USV_Electrical_Drawings_RevC.pdf'
    c=canvas.Canvas(str(pdf),pagesize=(CW*mm,CH*mm))
    c.setTitle('ENV-USV-01 Electrical Concept Drawing Set Rev C');c.setAuthor('Prepared for Pratik Prabhakar Shinde; AI-assisted conceptual study')
    for sh in sheets:sh.save();sh.plot(c)
    c.save()
    print(f'Created {len(sheets)} audited DXF sheets and {pdf}')

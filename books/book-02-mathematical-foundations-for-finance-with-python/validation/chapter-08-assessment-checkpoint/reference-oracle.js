/* Supplemental references only;does not execute Python sources. */
const rows=[
{name:"P8 stationary quantity",actual:50/.4,expected:125,tolerance:0},
{name:"P8 profit at maximizer",actual:-600+50*125-.2*125**2,expected:2525,tolerance:0},
{name:"P9 A'(3)",actual:150*Math.exp(.18),expected:179.5826,tolerance:0.00005},
{name:"P10 first",actual:-50000*Math.exp(-.2),expected:-40936.5377,tolerance:0.00005},
{name:"P10 second",actual:250000*Math.exp(-.2),expected:204682.6883,tolerance:0.00005},
{name:"P11 first",actual:-5*(10000*Math.exp(-.2))*.001,expected:-40.9365,tolerance:0.00005},
{name:"P11 second",actual:(-.005+.5*.005**2)*(10000*Math.exp(-.2)),expected:-40.8342,tolerance:0.00005},
{name:"P11 exact",actual:10000*Math.exp(-.2)*Math.expm1(-.005),expected:-40.8344,tolerance:0.00005},
{name:"P12 simple",actual:(84-80)/80,expected:0.05,tolerance:0},
{name:"P12 log",actual:Math.log(1.05),expected:0.0487902,tolerance:5e-8},
{name:"P13 elasticity",actual:-600/400,expected:-1.5,tolerance:0},
{name:"P14 quantity",actual:900/(45-15),expected:30,tolerance:0},
{name:"P14 slope",actual:-900/(45-15)**2,expected:-1,tolerance:0},
{name:"P15 yield",actual:(110-100)/100,expected:0.1,tolerance:0},
{name:"P15 dP/dy",actual:-1000/11,expected:-90.9091,tolerance:0.00005},
{name:"P15 inverse",actual:-11/1000,expected:-0.011,tolerance:0},
{name:"P16 inflection ordinate",actual:2**3-6*2**2+4,expected:-12,tolerance:0},
{name:"P18 forward",actual:1261/100,expected:12.61,tolerance:0},
{name:"P18 backward",actual:1141/100,expected:11.41,tolerance:0},
{name:"P18 centered",actual:1201/100,expected:12.01,tolerance:0},
{name:"P19 quadratic second",actual:2,expected:2,tolerance:0}
];
for(const r of rows)r.passed=Math.abs(r.actual-r.expected)<=r.tolerance;
console.log(JSON.stringify({engine:'Supplemental JavaScript',python_executions:0,rows},null,2));
if(rows.some(r=>!r.passed))throw Error('reference mismatch');

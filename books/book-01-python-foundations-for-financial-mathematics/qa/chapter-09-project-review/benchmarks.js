function deriveExpectations() {
  function gcd(a,b){a=a<0n?-a:a;while(b){[a,b]=[b,a%b];}return a;}
  function rational(n,d=1n){if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
  function add(a,b){return rational(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
  function mul(a,b){return rational(a[0]*b[0],a[1]*b[1]);}
  function power(a,n){return rational(a[0]**BigInt(n),a[1]**BigInt(n));}
  function record(label,a){let n=a[0],d=a[1],sign=n<0n?"-":"";n=n<0n?-n:n;let decimal=sign+(n/d).toString()+".";n%=d;for(let k=0;k<30;k++){n*=10n;decimal+=(n/d).toString();n%=d;}return {label,numerator:a[0].toString(),denominator:d.toString(),decimal_truncated_30_places:decimal};}
  const monthly=rational(201n,200n);
  const fv=mul([1000n,1n],power(monthly,24));
  const ear=add(power(monthly,12),[-1n,1n]);
  const dfs=[0,12,24,36].map(n=>power([150n,151n],n));
  const amounts=[-1000n,400n,500n,300n];
  const pvs=dfs.map((df,i)=>mul([amounts[i],1n],df));
  const npv=pvs.reduce(add,[0n,1n]);
  const exact=[record("P1 monthly FV",fv),record("P2 EAR decimal rate",ear),
    record("P3 break-even NPV",add([-1000n,1n],mul([1100n,1n],[10n,11n]))),
    record("P4 rate cross-check: (1.10)^2",power([11n,10n],2)),
    record("P7 same-date net",[-100n+40n+60n,1n]),
    ...pvs.map((a,i)=>record("demo PV event "+(i+1),a)),record("demo total NPV",npv)];
  const checks=[
    {label:"P1 displayed 1127.16",passed:Math.round(Number(fv[0])/Number(fv[1])*100)===112716},
    {label:"P2 displayed 6.1678 percent",passed:Math.round(Number(ear[0])/Number(ear[1])*100*10000)===61678},
    {label:"P3 zero NPV exactly",passed:exact[2].numerator==="0"},
    {label:"P4 annual factor 1.21 exactly",passed:exact[3].numerator==="121"&&exact[3].denominator==="100"},
    {label:"P5 two years cross-check",passed:1210n*100n===1000n*121n},
    {label:"P7 zero net exactly",passed:exact[4].numerator==="0"},
    {label:"demo positive NPV",passed:npv[0]>0n}
  ];
  return {scope:"Supplemental JavaScript BigInt rational derivations; no Python source execution",exact,checks};
}
console.log(JSON.stringify(deriveExpectations(), null, 2));

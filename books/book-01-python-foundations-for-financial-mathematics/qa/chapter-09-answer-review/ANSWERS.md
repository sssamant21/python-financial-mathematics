# Section 9.17 — Prompt-by-prompt review

All amounts use year0 valuation and signed dated events unless the prompt states a different convention. Printed decimals below are display values; calculations use exact rational or high-precision unrounded intermediates. Source results and independent expectations are retained in results.json.

| Problem | Independent answer / interpretation | Executed or reviewed scope |
|---|---|---|
| 01 | 5500/1.08 =5092.59259259…; premium92.59259259… over5000 now | Observed exact PV and premium benchmark |
| 02 | [(0,−2000),(1,900),(3,1400)], valuation year0 | Full source literal extracted by AST; initial-year source assertion; no calendar engine |
| 03 | 2500(1+.06×3)=2950, simple annual | Observed inline source calculation and exact rational reference |
| 04 | 2500(53/50)^3=2977.54 | Observed FV and rational power |
| 05 | 8000(20/21)^4=6581.619798335…; rounded6581.62 | Observed PV and rational discounting |
| 06 | 3000(26/25)^5=3649.9587072; rounded3649.96 | Observed FV and rational power |
| 07 | (100/107)^3=.816297876890852… | Observed discount factor and rational power |
| 08 | 100/(11/10)+200/(11/10)^2=256.198347107… | Observed source NPV and exact dated sum |
| 09 | −1000+600/(11/10)+600/(11/10)^2=41.3223140496… | Positive under deterministic stated model; source NPV/independent rational sum; no uncertainty acceptance |
| 10 | (101/100)^12−1=.1268250301319697… =12.682503013…% | Source conversion and exact rational power |
| 11 | Annual1060; monthly1061.6778118645… | Source comparison/observed monthly value and exact rational reference |
| 12 | 1500 exp(.10)=1657.75637711347… | Observed source exponential and independent Decimal exponential |
| 13 | sqrt(4840/4000)−1=.10 | Observed source root and exact positive-root identity1.10²=1.21 |
| 14 | ln2/ln1.08=9.0064683420… modeled years; first complete annual credit10 | Observed source log ratio, Decimal logs and rational bracketing at9/10 |
| 15 | Continuous ln1.10=.0953101798043…; nominal monthly .0956896851468… | Source nominal conversion observed; continuous quote is supplemental Decimal derivation, not a source continuous-conversion function |
| 16 | PV2000 at zero rate; equal balances leave time nonunique | Observed source PV plus separately executed capstone nonunique-time method; scope is algebraic model |
| 17 | 1000(.95)^2=902.50 | Observed FV and exact rational factor |
| 18 | −100+40+60=0 at year0 for any valid discount rate | Observed NPV and rational sum; no hidden cost |
| 19 | Header year,amount; events0,−1000;1,400;2,800 | Source CSV parsing, count/first amount assertions and complete exact CSV literal checked |
| 20 | −1000+400(150/151)^12+500(150/151)^24+300(150/151)^36=31.81915881737… | Observed source NPV and exact rational reference; missing computed display corrected underF51 |

The default annual effective convention equals annual nominal only for frequency1. Problem20 instead uses8% nominal annually with twelve periods; monthly factor151/150. Problem15 percentage displays are9.531018% continuous and9.5690% nominal monthly. Fractional modeled horizons are distinct from complete credit dates. All twenty answer records are separate from88 section-local prompts and16 core workflows. Educational rubric and “independent reference checks” wording do not designate an external reviewer or certification.

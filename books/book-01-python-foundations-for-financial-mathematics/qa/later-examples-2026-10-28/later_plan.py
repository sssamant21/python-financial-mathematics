"""Explicit later-chapter fixtures, assemblies and output/state checks."""
PLANS=[]
def add(ch,n,indices,checks='',setup='',support=(),files=None,fixtures=(),stdout=None,exception=None,name=None,module_name='reviewed_example'):
 if ch==7:setup='import numpy as np\nimport pandas as pd\n'+setup
 if ch==8:setup='import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport matplotlib.dates as mdates\nfrom matplotlib.ticker import PercentFormatter\nfrom zoneinfo import ZoneInfo\n'+setup
 PLANS.append(dict(chapter=ch,section=n,indices=indices,checks=checks,setup=setup,support=list(support),files=files or {},fixtures=list(fixtures),stdout=stdout,expected_exception=exception,name=name or f'ch{ch:02}-s{n:02}',module_name=module_name))
# Chapter 4 introductory sequences are explicitly ordered in the manuscripts.
for sec,indices in [(1,[0,1]),(2,list(range(7))),(3,list(range(5))),(4,list(range(5))),(5,[0,1,2]),(6,[0,1,2]),(7,list(range(5))),(8,[0,1,2]),(9,[0,1,2]),(10,[0,1,2]),(11,[0,1,2,3]),(12,[0,1,2])]:add(4,sec,indices)
add(4,5,[4],"assert display_missing==['P002','P003']",support=[(4,5,3,'sets_lab.py')],name='set-report-import')
add(4,14,[0,1],"assert len(holdings)==3 and original==[{'security_id':'A','quantity':2}] and other==[]")
add(5,1,[0],"assert not called",setup="called=[]\nmain=lambda:called.append(True)",name='main-guard-import')
add(5,1,[0],"assert called==[True] and _caught_error.code==0",setup="called=[]\ndef main():\n called.append(True)\n return 0",exception='SystemExit',module_name='__main__',name='main-guard-execution')
add(5,3,[0,1,2],"assert parsed['amount']=='12.50' and not path.exists()")
# pandas context fixtures make labels, timestamps, missingness and grouping explicit.
add(7,1,[0,1,2],"assert math.isclose(wrong,.025) and math.isclose(contribution.sum(),.045);assert pd.isna(product.loc['B']);assert 'nan' in captured")
add(7,2,[0,1,2,3,4],"assert integer_labels.loc[0]==20 and integer_labels.iloc[0]==10;assert requested.loc['BETA']==300 and pd.isna(requested.loc['DELTA']);assert complete_total==1000 and missing.to_dict()=={'CASH':False,'DELTA':True}")
add(7,3,[0,1,2],"assert total==1000 and large.index.tolist()==['ALPHA','BETA'];assert example['check'].tolist()==[30,20,10]")
add(7,4,[0,1],"assert large.index.tolist()==['ALPHA','BETA'];assert t.loc['ALPHA','price']==100 and scenario.loc['ALPHA','market_value']==660",setup="t=pd.DataFrame({'quantity':[6.,3.,1.],'price':[100.,100.,100.],'market_value':[600.,300.,100.]},index=['ALPHA','BETA','CASH'])")
add(7,6,[0],"assert introduced.tolist()==[False,True,False] and parsed.isna().sum()==2 and parsed.iloc[0]==100")
add(7,7,[0],"assert partial.sum()==.06 and pd.isna(partial.sum(skipna=False))")
add(7,8,[0],"assert duplicate.tolist()==[True,False,True]",setup="normalized=pd.DataFrame({'asset':['A','B','A']})")
add(7,9,[0,1,2],"assert utc[0].isoformat()=='2026-01-30T14:30:00+00:00';assert inclusive.tolist()==[10,20,30] and window.tolist()==[10,20]",setup="series=pd.Series([10,20,30],index=pd.date_range('2026-01-01',periods=3,tz='UTC'));start=series.index[0];end=series.index[2]")
add(7,10,[1,0,2,3],"assert ranked['asset'].tolist()==['A','B'];assert eligible.equals(eligible_query);assert columns_only.columns.tolist()==['asset']",setup="table=pd.DataFrame({'asset':['B','A','C'],'market_value':[300.,300.,100.],'sector':['equity','equity','cash']});floor=300.;sector='equity'")
add(7,11,[0,1,2],"assert report.loc['equity','asset_count']==2 and report.loc['equity','opening_value']==900;assert sector_values.tolist()==[900,900,100];assert with_missing_key.ngroups==2",setup="table=pd.DataFrame({'sector':['equity','equity','cash'],'asset':['A','B','C'],'opening_value':[600.,300.,100.],'price_pnl':[60.,-15.,0.]})")
add(7,12,[0],"assert audit['_merge'].astype(str).tolist()==['left_only','both','right_only']",setup="holdings=pd.DataFrame({'asset':['A','B'],'currency':['USD','USD'],'valuation_date':['2026-01-01']*2,'quantity':[1.,2.]});quotes=pd.DataFrame({'asset':['B','C'],'currency':['USD','USD'],'valuation_date':['2026-01-01']*2,'price':[10.,20.]})")
add(7,13,[0,1],"assert result['volume'].tolist()==[3.,7.];assert result.index[0].isoformat()=='2026-01-01T00:30:00+00:00'",setup="table=pd.DataFrame({'volume':[1.,2.,3.,4.]},index=pd.date_range('2026-01-01',periods=4,freq='15min',tz='UTC'));result=pd.DataFrame()")
add(7,14,[0,1,2,3],"assert mean.iloc[:2].isna().all() and mean.iloc[2]==2 and std.iloc[2]==1;assert historical_mean.tolist()==[1.,1.5,2.,2.5];assert prior_mean.isna().sum()==3",setup="prices=pd.Series([1.,2.,3.,4.],index=pd.date_range('2026-01-01',periods=4,freq='15min',tz='UTC'));rolling_mean=prices.rolling(3,min_periods=3).mean()")
add(7,15,[0,1,2],"assert simple.iloc[0]!=simple.iloc[0];assert np.allclose(simple.iloc[1:],[.1,-.1]);assert np.allclose(gross.iloc[1:],[1.1,.9]);assert elapsed.iloc[1]==pd.Timedelta(days=1);assert math.isclose(log_return.iloc[1],math.log(1.1))",setup="prices=pd.Series([100.,110.,99.],index=pd.date_range('2026-01-01',periods=3,tz='UTC'))")
add(7,16,[0,1,2],"assert wide.shape==(3,2) and pd.isna(wide.loc[expected_times[1],'B']);assert complete_interval.tolist()==[False,False,False]",setup="expected_times=pd.date_range('2026-01-01',periods=3,tz='UTC');expected_assets=('A','B');records=pd.DataFrame({'time':[expected_times[0],expected_times[0],expected_times[1],expected_times[2],expected_times[2]],'asset':['A','B','A','A','B'],'price':[100.,200.,110.,121.,220.]})")
add(7,17,[0],"wide,ret,complete=panel(raw,('A','B'),grid);assert wide.shape==(3,2) and complete.tolist()==[False,True,True];assert np.allclose(ret.iloc[1:].to_numpy(),[[.1,.05],[.1,.05]])",setup="grid=pd.date_range('2026-01-01',periods=3,tz='UTC');raw=pd.DataFrame({'time':grid.repeat(2),'asset':['A','B']*3,'price':[100.,200.,110.,210.,121.,220.5]})",name='panel-function-direct-call')
# Plot snippets run under Agg with structural checks and explicit source grids.
add(8,2,list(range(6)),"assert line.get_linewidth()==2;assert balance_ax.get_xlabel()=='';assert len(balance_ax.texts)==1;assert Path('chart.png').read_bytes().startswith(b'\\x89PNG');assert '<svg' in Path('chart.svg').read_text();plt.close('all')",setup="from pathlib import Path\nx=[0,1,2];values=[1000,1050,1102.5];balances=values",name='matplotlib-figures-and-export')
add(8,3,[0,1],"assert ax.lines[0].get_label()=='Account A' and ax.lines[1].get_drawstyle()=='steps-post';assert list(ax.lines[1].get_ydata())==[10,20,20];plt.close('all')",setup="fig,ax=plt.subplots();x=[0,1,2];y=[100,110,105];days=[0,1,2];shares=[10,20,20]")
add(8,4,list(range(5)),"assert present.tolist()==[True,False,True] and aligned['price'].isna().tolist()==[False,True,False];assert len(x)==3 and ax.xaxis.get_major_formatter() is formatter;plt.close('all')",setup="grid=pd.date_range('2026-01-01',periods=3,freq='h',tz='UTC');index=grid[[0,2]];frame=pd.DataFrame({'price':[100.,110.]},index=index);fig,ax=plt.subplots()")
add(8,5,[0],"assert ax.yaxis.get_major_formatter().xmax==1.0;plt.close('all')",setup='fig,ax=plt.subplots()')
add(8,6,[0,1],"assert edges.tolist()==[-.1,-.02,0,.02,.1];assert candidate_edges[0]<=min(observed) and candidate_edges[-1]>=max(observed)",setup='observed=np.array([-.05,-.01,0.,.02,.05])')
add(8,7,[0,1],"assert pairs.shape==(2,2);assert len(ax.collections)==1 and ax.collections[0].get_offsets().shape==(2,2);plt.close('all')",setup="aligned=pd.DataFrame({'benchmark':[.01,float('nan'),.03],'asset':[.02,.04,.01]});x=[.01,.03];y=[.02,.01];fig,ax=plt.subplots()")
add(8,9,[0],"assert call_payoff.tolist()==[0.,0.,20.] and put_payoff.tolist()==[20.,0.,0.]",setup='terminal_prices=np.array([80.,100.,120.]);strike=100.')
add(8,11,[0],"assert balances.shape==(2,3);assert np.allclose(balances,[[100.,100.,100.],[100.,110.,121.]])",setup='rates=np.array([0.,.1]);years=np.array([0.,1.,2.]);principal=100.')
for tamper in [False,True]:
 setup="import dashboard\nfrom pathlib import Path\ninfo=dashboard.run('prices.csv','output/run01',pd.date_range('2026-01-01T00:00:00Z',periods=6,freq='D'))"
 if tamper:setup+="\np=Path('output/run01/dashboard.png');p.write_bytes(p.read_bytes()+b'controlled-tamper')"
 add(8,13,[2],"assert len(info['output_sha256'])==6" if not tamper else "assert 'Output digest mismatch: dashboard.png' in str(_caught_error)",setup=setup,support=[(8,13,0,'dashboard.py')],fixtures=[(8,13,'csv',0,'prices.csv')],stdout='All recorded output digests match.\n' if not tamper else None,exception='ValueError' if tamper else None,name='dashboard-digests-'+('tampered' if tamper else 'valid'))
# Stable arithmetic, stochastic illustrations, numerical methods and project drivers.
add(11,12,[0,1],stdout='False\nTrue\n1.01\n')
add(13,4,[0,1],"assert math.log1p(R)>0 and math.log(1+R)==0 and math.expm1(ell)>0",setup='R=1e-16;ell=1e-16')
for sec,idx in [(8,0),(14,0)]:add(13,sec,[idx],"assert abs(math.expm1(math.fsum(math.log1p(r) for r in returns)/len(returns))-(math.sqrt(.99)-1))<1e-15",setup='returns=[-.1,.1]')
add(13,11,[0],"assert len(returns)==5 and math.isclose(math.fsum(returns),.03)")
add(14,14,[0],"assert len(with_replacement)==10 and set(with_replacement)<=set(states);assert len(without_replacement)==len(set(without_replacement))==2")
add(14,15,[0],"assert captured=='[0.6394267984578837, 0.025010755222666936, 0.27502931836911926]\\n'",name='standard-library-seed-draw-order')
add(14,16,[1],"assert len(draws)==20000 and set(draws)<=set(PAYOFFS);assert exact_moments(PAYOFFS,WEIGHTS)[:2]==(5.,312.5);assert len(defaults)==20000 and all(0<=v<=10 for v in defaults);assert 'Bootstrap SE:' in captured and 'Manifest:' in captured",support=[(14,16,0,'financial_probability_simulator.py')],name='probability-experiment-driver')
add(15,14,[1],"assert dates==['2026-01-05','2026-01-06','2026-01-07','2026-01-08','2026-01-09'];assert summary['observations']==4 and len(summary['rolling_mean'])==3",support=[(15,14,0,'financial_statistics_toolkit.py')],fixtures=[(15,14,'csv',0,'prices.csv')],name='statistics-csv-driver')
add(16,5,[1],"assert np.allclose(np.cov(np.array(rows).T,ddof=1),[[1/6000,1/5000],[1/5000,1/3000]],rtol=0,atol=1e-18)",setup='import numpy as np')
add(17,3,[0],"assert math.isclose(bracketed.root,math.sqrt(2),abs_tol=1e-10) and math.isclose(newton_result.root,math.sqrt(2),abs_tol=1e-10)")
add(17,4,[0],"assert abs(npv(result.root))<1e-10 and math.isclose(result.root,(60+math.sqrt(27600))/200-1,abs_tol=1e-10)")
add(17,5,[0],"assert abs(vector.x[0]-2/3)<1e-5 and abs(vector.x[1]-1/3)<1e-5")
for n in [6,7]:add(17,n,[0],"assert np.allclose(result.x,[.4,.6],rtol=0,atol=1e-6)")
add(17,8,[0],"assert abs(value-1/3)<1e-10 and abs(pv-2000*(1-math.exp(-.1)))<1e-8")
add(17,9,[0],"assert np.allclose(pchip(tenors),zero_rates) and np.allclose(spline(tenors),zero_rates);assert math.isclose(float(np.exp(log_df_at_2_5)),math.exp(-.12),abs_tol=1e-12)")
add(17,10,[0],"assert abs(df_two-127/140)<1e-12")
add(17,11,[0,1,2,3],"assert math.isclose(log_return,math.log(1.001),abs_tol=1e-15);assert tail>0",setup='P0=100.;P1=100.1')
add(17,12,[0,1],"assert result.converged and abs(result.root-.1)<1e-10 and abs(value-exact)<1e-10")
add(17,13,[1],"assert result.converged and abs(result.root-.1)<1e-10 and abs(price_error(result.root))<1e-10")
add(18,2,[0],"assert len(draws)==5 and all(0<=v<1 for v in draws)",name='uniform-five-draws')
add(18,2,[1],"assert len(samples)==5 and all(math.isfinite(v) for v in samples)",name='normal-five-draws')
add(18,2,[2],"assert uniform.shape==normal.shape==(10000,);assert .48<uniform.mean()<.52 and .03<normal.mean()<.07",name='numpy-generator-arrays')
add(18,2,[3],"assert 0<=first<1",name='state-restore')
add(18,2,[4],"assert [c.spawn_key for c in children]==[(0,),(1,),(2,),(3,)];assert len(workers)==4",name='four-spawned-streams')
add(18,3,[0,1,2],"assert 0<=first<1 and [c.spawn_key for c in children]==[(0,),(1,)]")
add(18,13,[1],"assert remaining==0 and u.shape==(10000,) and 99.5<total/100000<100.5",name='numpy-batched-payoffs')
# Stage-specific capstone initializers and public example imports.
modules={5:'time_value',6:'cashflows',7:'loans',8:'bonds',9:'returns',10:'portfolio',11:'statistics',12:'simulation',13:'validation',14:'visualization'}
checks={5:"assert all(abs(float(a)-b)<1e-10 for a,b in zip(captured.splitlines(),[121.,100.]))",6:"assert math.isclose(value,500/121,abs_tol=1e-10)",7:"assert math.isclose(payment,121000/210,abs_tol=1e-10);assert abs(net_present_value(borrower_flows,rate))<1e-10",8:"assert abs(price-100)<1e-10 and abs(check-100)<1e-10",9:"assert math.isclose(total,-.01,abs_tol=1e-12)",10:"assert math.isclose(value,.04,abs_tol=1e-12)",11:"assert abs(summary.mean)<1e-12 and math.isclose(summary.sample_stddev,math.sqrt(.02),abs_tol=1e-12)",12:"assert len(run.terminal_values)==1000 and 95<summary.mean<105",13:"assert 'Price return: 10.00%' in captured",14:"from pathlib import Path\nassert Path('synthetic_price.png').read_bytes().startswith(b'\\x89PNG') and plt.get_fignums()==[]"}
for n in range(5,15):
 support=[(21,k,0,'financial_toolkit/'+modules[k]+'.py') for k in range(5,n+1)]
 # For stages 5–13 the initializer is itself an uncovered target, copied unchanged.
 targets=[(21,n,1,'financial_toolkit/__init__.py')]
 add(21,n,[2],checks[n],support=support,setup='import matplotlib.pyplot as plt' if n==14 else '',name=f'capstone-stage-{n:02}')
 PLANS[-1]['target_files']=targets if n<14 else []
 if n==14:PLANS[-1]['support'].append((21,14,1,'financial_toolkit/__init__.py'))

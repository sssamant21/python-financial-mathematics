"""Reviewed workflow selections and explicit state/output oracles."""
PLANS=[]
def add(ch,sec,indices,checks='',setup='',support=(),stdout=None,exception=None,name=None):
 checks=checks.replace('\n','\\n')
 PLANS.append(dict(chapter=ch,section=sec,indices=indices,checks=checks,setup=setup,support=list(support),stdout=stdout,expected_exception=exception,name=name or f'ch{ch:02}-s{sec:02}-'+ '-'.join(map(str,indices))))
# Chapter 1: independent variable-state and output checks for elementary examples.
add(1,5,[4],"assert captured.strip() == sys.executable")
add(1,6,[1,2,3,4,5],"assert principal==1000.0 and notional==10000000.0 and periods==3 and rate==.05",stdout="<class 'int'>\n<class 'float'>\n")
add(1,6,[6,8,9,10,11,12],"assert math.isclose(future_value,1157.625,abs_tol=1e-10)",setup='principal=1000.0; rate=.05; periods=3',stdout='1157.6250000000002\nFuture value: 1157.6250000000002\nFuture value: 1157.6250000000002\nFuture value: $1,157.63\n')
add(1,6,[7],setup='rate=.05; periods=3',exception='TypeError')
add(1,6,[13,15,16],"assert rate_per_period==.05",stdout='Interest rate: 5.00%\n')
add(1,6,[18,19],"assert math.isclose(future_value,1157.625,abs_tol=1e-10)",stdout='Future value: $1,157.63\n')
add(1,6,[22],"assert annual_effective_rate==5 and future_value==216000 and future_value != 1157.625",name='deliberate-percent-unit-error')
add(1,7,[1,3],"assert math.isclose(future_value,16288.94626777442,abs_tol=1e-9); assert (interest_rate,volatility,portfolio_weight)==(.0525,.18,.35)")
add(1,7,[6],"assert math.isclose(result,expected,rel_tol=1e-9)",setup='result=.1+.2; expected=.3; import math')
add(1,7,[8,9],"assert Decimal('0.1') != Decimal(.1)")
add(1,7,[19],"assert principal==Decimal('10000') and rate==Decimal('.05') and periods==3",setup="principal_text='10000';rate_text='.05';periods_text='3'")
add(1,8,[1,2,3,4,5],"assert total_cash_flow==1250 and net_amount==35000 and price_change==8 and interest==500 and weight==.25")
add(1,8,[6],exception='ZeroDivisionError')
add(1,8,[7,8,9,10],"assert full_years==2 and remaining_months==5; assert 17//5==3 and 17%5==2 and 2**3==8")
add(1,8,[14,15,16,17,18],"assert gain==3500 and gain_rate==.07 and net_cash_flow==750 and balance==10500 and result==160")
add(1,8,[19,20],"assert math.isclose(present_value,1000,abs_tol=1e-10); assert math.isclose(future_value,1157.625,abs_tol=1e-10)",setup='principal=1000.;rate=.05;periods=3;annual_rate=.05;years=3')
add(1,8,[21,23,24,25,26],"assert interest_usd==500 and spread_decimal==.0125 and math.isclose(total_rate,.0525) and increase==15 and new_value==114.99999999999999")
add(1,9,[0,1,2,3,4,5,6,7,8],"assert math.isclose(future_value,1157.625,abs_tol=1e-10)",setup='principal=1000.;annual_rate=.05;years=3;interest=50.;rate=.05;periods=3;a=2;b=3;x=2;n=3;A=1;B=2;C=3;D=4')
add(1,9,[11,12,13,17,18,19,20],"assert math.isclose(present_value,1000,abs_tol=1e-10)",setup='principal=1000.;rate=.05;periods=3')
add(1,9,[21],"assert relative_change==.08",setup='final_price=108.;initial_price=100.')
add(1,9,[22],"assert relative_change==107.0 and relative_change != .08",setup='final_price=108.;initial_price=100.',name='deliberate-precedence-error')
add(1,9,[23,24,25,27,28,29,30],"assert math.isclose(portfolio_return,.04,abs_tol=1e-14);assert average==20 and change_percent==10;assert math.isclose(future_value,1157.625,abs_tol=1e-10)",setup='weight_1=.6;return_1=.08;weight_2=.4;return_2=-.02;value_1=10;value_2=20;value_3=30;old_value=250;new_value=275;principal=1000.;rate=.05;periods=3;fees=10;stock_weight=.5;stock_return=.06;bond_weight=.3;bond_return=.03;cash_weight=.2;cash_return=.005')
add(1,9,[34],"assert return_rate==114 and return_rate != .15",setup='final_value=115;initial_value=100',name='deliberate-return-precedence-error')
add(1,10,[0],"assert math.isclose(future_value,11576.25,abs_tol=1e-9)",stdout='11576.250000000002\n')
# Input snippets are isolated to avoid one prompt consuming another's fixture.
inputs={1:('1000\n.05\n3\n',"assert principal==1000 and rate==.05 and periods==3;assert math.isclose(future_value,1157.625,abs_tol=1e-10)"),2:('Example Fund\n',"assert investment_name=='Example Fund'"),3:('1000\n',"assert principal=='1000'"),4:('1000\n3\n',"assert principal==1000 and periods==3"),5:('.05\n',"assert rate==.05"),6:('5\n',"assert rate==.05"),7:('5.25\n',"assert annual_rate==.0525;assert math.isclose(future_value,1165.913453125,abs_tol=1e-8)"),8:('5\n',"assert annual_rate==.05"),9:('3\n',"assert periods==3"),10:('bad\n',"assert 'Principal must be numeric.' in captured"),12:('nan\n',"assert 'Value must be finite.' in captured"),13:('  Fund A  \n',"assert investment_name=='Fund A'"),14:('1000\n5\n3\n',"assert math.isclose(future_value,1157.625,abs_tol=1e-10)"),21:('5.25\n3\n',"assert rate_percent==5.25 and years==3"),22:('5\n',"assert rate==.05 and math.isclose(future_value,1157.625,abs_tol=1e-10)"),23:('1000\n5\n3\n',"assert 'Future value: $1,157.63' in captured")}
for idx,(stdin,checks) in inputs.items():
 add(1,10,[idx],checks,setup='principal=1000.;years=3');PLANS[-1]['stdin']=stdin
add(1,10,[11],"assert captured=='Principal must be greater than zero for this model.\n'",setup='principal=-1')
add(1,10,[15,16,17,18,19,20],"assert formatted_value=='1,234.57' and value==1234.5678; assert 'Rate: 5.25%' in captured",setup='future_value=11576.25;result=11576.25;annual_rate=.0525')
add(1,11,[5],"assert math.isclose(a,b,rel_tol=1e-9)",setup='a=.1+.2;b=.3;import math')
add(1,11,[13,16,19],"assert float_result != .3 and fee==Decimal('.5125') and USD_CENT==Decimal('.01')",stdout='0.30000000000000004\n0.5125\n')
add(1,11,[24],"assert abs(total-10000)<.001 and total !=10000",name='million-float-accumulations')
add(1,11,[25],"assert total==Decimal('10000.00')",stdout='10000.00\n',name='million-decimal-accumulations')
add(1,11,[27],"assert fee==Decimal('15.63')",stdout='15.63\n')
add(1,12,list(range(14)),"assert interest==Decimal('1500.00') and ending_balance==Decimal('11500.00'); assert profit_loss==Decimal('800') and return_percent==Decimal('16');assert fee==Decimal('15.63') and total_paid==Decimal('1266.38');assert difference==tolerance; assert 'Values reconcile' in captured",name='calculator-components')
PLANS[-1]['stdin']='5\n'
add(1,13,[0,1,2,3],"assert account_balance+deposit-withdrawal==Decimal('10800');assert result==Decimal('11500');assert MONEY_QUANTUM==Decimal('.01')",setup="principal=Decimal('10000');rate=Decimal('.05');years=Decimal('3')")
# Companion context examples use explicitly recorded teaching inputs.
add(1,13,[1,7,9,14,15,21],"assert future_value==Decimal('1102.5000');assert ending_balance==Decimal('1100');assert display_interest==Decimal('100.00');assert 'Interest: $100.00' in captured",setup="present_value=Decimal('1000');rate=Decimal('.05');periods=2;principal=Decimal('1000');years=2;periods_per_year=12",support=[(1,12,0),(1,12,1)],name='companion-context-examples')
PLANS[-1]['companion']=True;PLANS[-1]['stdin']='1000\n5\n2\n'
# Chapter 2: complete teaching examples plus bounded prerequisite assemblies.
add(2,1,[0,1,2,3,11,12,14,15],"assert is_reconciled and not is_profitable and has_sufficient_balance and meets_requirement and is_within_limit; assert captured==\"<class 'bool'>\\n<class 'str'>\\nFalse\\nTrue\\nFalse\\nTrue\\nFalse\\nTrue\\n\"")
add(2,1,[6,7,17],"assert is_profitable and is_reconciled",setup="profit_loss=Decimal('10');difference=Decimal('.01');tolerance=Decimal('.01');account_balance=Decimal('10000')")
add(2,2,[1,5,12,13,14,15],"assert is_exact_value and not meets_minimum_balance and is_reconciled and is_valid_rate and requires_review",setup="balance=Decimal('1000');system_a=Decimal('100');system_b=Decimal('100.01');minimum_rate=Decimal('0');rate=Decimal('.05');maximum_rate=Decimal('.10');exposure=Decimal('20000');exposure_limit=Decimal('10000');materiality_threshold=Decimal('1000')")
add(2,3,[2,3,4,9,10,11,13,16,17],"assert status=='Accepted' and reached_target and reached_high_return and classification=='Meets Model Requirements';assert captured.count('Minimum balance satisfied.')==2",setup="balance=Decimal('12500');minimum_balance=Decimal('10000');return_rate=Decimal('.10');profit_loss=Decimal('100');target_return=Decimal('.05');investment_amount=Decimal('1000');minimum_investment=Decimal('500');rate=Decimal('.05');minimum_rate=Decimal('0')")
add(2,3,[14],"assert captured=='Rate is unavailable.\n'",setup='rate=None')
add(2,4,[1,2,3,8,9,10,11,12,13,14,15,16,17,19,27,28,29,30,31,32],"assert status=='Target Achieved' and classification=='High' and profit_loss==Decimal('1250');assert is_reconciled and requires_review and is_material;assert captured=='Send item for review.\n'",setup="system_a=Decimal('100');system_b=Decimal('100.01');tolerance=Decimal('.01');balance=Decimal('10000');return_rate=Decimal('.10');target_return=Decimal('.05');exposure=Decimal('20000');exposure_limit=Decimal('10000');difference=Decimal('.01');requires_review=True;amount=Decimal('15000');value=Decimal('1');materiality_threshold=Decimal('10000')")
add(2,5,[1,2,3,4,5,6,7,10,12,14,15,16],"assert calculated_fees==[Decimal('15'),Decimal('37.5'),Decimal('60')];assert meeting_target_count==2 and raw_fee==Decimal('37.5');assert transaction_amounts==[Decimal('1000'),Decimal('2500'),Decimal('4000')]")
add(2,6,[2,3,10,15],"assert balance==target_balance==Decimal('10000');assert outcome=='Target reached'",name='while-update-before-or-after')
add(2,6,[12],"assert balance==Decimal('10000') and periods==4",setup="balance=Decimal('8000');target_balance=Decimal('10000');contribution=Decimal('500');periods=0")
add(2,7,[7,8,9,10,11,12,13,14,15],"assert trace==[(Decimal('1000'),Decimal('200'),Decimal('1200')),(Decimal('1200'),Decimal('-50'),Decimal('1150')),(Decimal('1150'),Decimal('300'),Decimal('1450'))];assert difference==0 and total_cash_flow==0")
add(2,8,[0,2,3,4,5,6,7,8,9,10,11,12,14,15,17,18,19,20,21,22,23,27,28,29,32,33,34,35,36,37,38],"assert balance==0;assert periods==[1,2,3,4,5];assert number_of_periods==12;assert abs(present_value-Decimal(8284000)/Decimal(9261))<Decimal('1e-20')",name='range-timelines')
add(2,9,[0,3,5,6,7,8,9,10,11,12,13,14,16,17,18],"assert grand_total==750 and annual_total==420;assert period==36;assert 'Reject: risk too high' in captured and 'Large outflow' in captured and 'Grand total: 750' in captured",name='nested-complete-examples')
add(2,10,[1,2,3,5,6,7,8,9,12,15,16,18,20,21],"assert loan_balance==0 and year==10;assert 'Loan repaid in Month 12' in captured;assert 'Target was not reached within the projection.' in captured;assert 'Maximum attempts completed without success.' in captured",name='break-continue-complete-examples')
add(2,10,[10,11,13],"assert skipped_observations==1 and missing_count==1 and zero_count==1 and processed_count==2",setup='financial_data=[1,None,2];transactions=[None,0,5,-2]')
add(2,11,[0,1,4,11],"assert principal==Decimal('-10000') and years==-5;assert captured=='Missing cash flow.\n'")
add(2,11,[3,5,6,7,8,9,10,12],"assert annual_contribution==0;assert 'Annual rate must be finite.' in captured and 'Years must be an integer.' in captured",setup="annual_rate=Decimal('NaN');annual_contribution=None;annual_return=Decimal('-1');years=True;discount_rate=Decimal('.02');growth_rate=Decimal('.03')",name='defensive-validation-context')
# Split None-specific check from nonfinite-rate and negative-contribution checks.
PLANS[-1]['indices']=[3,8,9,10,12];PLANS[-1]['setup']="annual_rate=None;annual_contribution=None;years=True;discount_rate=Decimal('.02');growth_rate=Decimal('.03')";PLANS[-1]['checks']="assert annual_contribution==0;assert 'Annual rate is required.' in captured and 'Years must be an integer.' in captured"
add(2,11,[5,6,7],"assert captured=='Annual rate must be finite.\nAnnual contribution cannot be negative.\nAnnual return must exceed -100% for this model.\n'",setup="annual_rate=Decimal('NaN');annual_contribution=Decimal('-1');annual_return=Decimal('-1')")
add(2,13,[6,9,10,11],"assert annual_contribution==Decimal('6000');assert maximum_years==25;assert 'Usable Decimal rate.' in captured;assert balance==Decimal('100')*Decimal('1.05')**11+Decimal('10')",setup="annual_return=Decimal('.05');balance=Decimal('100');annual_contribution=Decimal('10')",name='chapter2-companion-context')
PLANS[-1]['companion']=True
# Chapter 3 assertions are supplied by the manuscript, supplemented by output/state checks.
add(3,1,[1,2,4],"assert next_balance(Decimal('1000'),Decimal('.05'),Decimal('100'))==Decimal('1150');assert present_value(Decimal('110'),Decimal('.10'),1)==Decimal('100')",support=[(3,1,0)])
add(3,2,[0,1,3,4,5,6,7],"assert captured.startswith('16288.94626777441406250000');show_balance();show_rate()")
add(3,2,[8,9,10,11,13,14,15,16,17,18,19,20],"assert callable(result);assert classify_cash_flow(Decimal('-1'))=='negative';assert total_cash_flows([Decimal('100'),Decimal('-20')])==Decimal('80')",support=[(3,2,13)],setup="current_balance=Decimal('100');target_balance=Decimal('100')")
add(3,2,[12],exception='NameError')
add(3,2,[21],"assert future_value(Decimal('1000'),Decimal('.05'),2)==Decimal('1100');assert future_value(Decimal('1000'),Decimal('.05'),2)!=Decimal('1102.50')",name='deliberate-simple-vs-compound-error')
add(3,3,[3,4,5,7,8,9,10,11,19,12,13,15,16,17,18,20,21],"assert account_balance==Decimal('10000');assert result==Decimal('16288.94626777441406250000');assert target_reached(Decimal('100'),Decimal('100')); flows=[];add_cash_flow(flows,Decimal('10'));assert flows==[Decimal('10')]",support=[(3,3,0),(3,3,19)])
add(3,3,[14],exception='TypeError',support=[(3,3,0)])
add(3,4,list(range(14)),"assert gain==Decimal('100');assert len(original)==3 and display_amount=='1102.50' and captured.count('250')>=1")
add(3,5,list(range(13)),"assert amount==Decimal('1102.50');assert first is not second;assert provided==[Decimal('300')];assert end_balance==Decimal('1150') and beginning_balance==Decimal('1155')")
add(3,6,list(range(18)),"assert active_rate==Decimal('.07');assert observations==[Decimal('100')];assert separate[0](Decimal('1000'))==Decimal('1030')")
add(3,7,list(range(9)),"assert amount==Decimal('1102.50') and incorrect_result=='1000';assert ending==Decimal('1100') and gain==Decimal('100')")
add(3,8,[0,1,2],"import doctest;stats=doctest.testmod(sys.modules[__name__]);assert stats.failed==0 and stats.attempted==1")
add(3,10,[1],"assert future_amount==Decimal('1102.50')",support=[(3,10,0,'rate_discounting_lab.py')])
add(3,11,[0,1,2],"assert fee_before_growth==Decimal('1039.50') and fee_after_growth==Decimal('1040')")
add(3,12,[0],"assert low_precision==Decimal('33.3333') and high_precision!=low_precision")
# Remaining context-bound illustrations receive named fixtures rather than accidental state.
add(2,1,[13],"assert captured==''",setup='is_profitable=True;is_reconciled=True;is_break_even=False;has_sufficient_balance=True;meets_minimum_balance=True;is_within_limit=True',name='boolean-name-expressions')
add(2,2,[3,7,9],"assert meets_minimum_balance and exceeds_exposure_limit and not has_reconciliation_exception and requires_review",setup="balance=Decimal('12500');minimum_balance=Decimal('10000');exposure=Decimal('20000');exposure_limit=Decimal('10000');difference=Decimal('.01');tolerance=Decimal('.01');exceeds_limit=True;is_unreconciled=False;is_material=True;value=None")
add(2,6,[9],"assert difference==0",setup="difference=Decimal('1');tolerance=Decimal('.01');refinement_step=Decimal('0')",name='bounded-refinement-placeholder-fixture')
add(2,7,[3],"assert captured=='100\n200\n'",setup="cash_flows=[Decimal('100'),Decimal('200')]")
add(2,8,[1,13,16,30,31,39],"assert cash_flow==Decimal('200');assert list(range(1,number_of_periods+1))==[1,2]",setup="start=1;stop=5;step=1;number_of_periods=2;cash_flows=[Decimal('100'),Decimal('200')]",name='range-context-expressions')
add(2,9,[4,20,24],"assert captured=='Approved\nApproved\n' and decision=='Approve'",setup="expected_return=.09;required_return=.08;risk_score=3;maximum_risk=4;meets_return_requirement=True;meets_risk_requirement=True;has_sufficient_liquidity=True")
add(2,9,[15],"assert portfolio_total==600 and security_total==300",setup='from types import SimpleNamespace\nportfolios=[[SimpleNamespace(value=100),SimpleNamespace(value=200)],[SimpleNamespace(value=300)]]',name='nested-portfolio-test-double')
add(2,10,[14],"assert processed==[1,2]",setup='values=[-1,1,2,3,4];processed=[]\nstop_condition=lambda value:value>=3\nskip_condition=lambda value:value<0\nprocess=processed.append',name='stop-skip-callback-test-doubles')
add(2,10,[17],"assert target_found and scenario==1 and period==1",setup='scenarios=[1,2];periods=[1,2];some_condition=True',name='nested-break-predicate-fixture')
add(2,10,[19],"assert captured=='Target not found\n'",setup="projected_balances=[Decimal('60'),Decimal('70')];target_balance=Decimal('100')",name='for-else-no-target')
add(2,10,[19],"assert captured=='' and balance==target_balance",setup="projected_balances=[Decimal('60'),Decimal('100')];target_balance=Decimal('100')",name='for-else-target')
add(2,11,[2],"assert future_value==Decimal('1157.625000')",setup="principal=Decimal('1000');annual_rate=Decimal('.05');years=3")

add(2,6,[11],"assert balance==Decimal('10000') and captured=='8500\\n9000\\n9500\\n10000\\n'",setup="balance=Decimal('8000');target_balance=Decimal('10000');contribution=Decimal('500')",name='while-update-then-print')
for frequency in [0,-1]:
 add(1,13,[14],setup='periods_per_year='+str(frequency),exception='ValueError',name='companion-invalid-frequency-'+str(frequency));PLANS[-1]['companion']=True

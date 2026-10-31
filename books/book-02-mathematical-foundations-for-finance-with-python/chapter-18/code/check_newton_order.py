"""Observed Section 18.4 proposals versus independent simple-root identities."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import section_18_04 as lab


def observed(c,lower,upper,max_iter,atol=2**-35):
    events=[]
    def f(x):
        value=float(F(x)*F(x)-c)
        events.append({'kind':'f','x':x,'value':value})
        return value
    def df(x):
        value=2*x
        events.append({'kind':'df','x':x,'value':value})
        return value
    result=lab.safeguarded_newton(f,df,lower,upper,atol,0,max_iter)
    return result,events


def audit_single(c,x,result,events):
    assert [e['kind'] for e in events]==['f','f','f','df','f','f']
    assert events[2]['x']==events[3]['x']==x
    proposal=events[4]['x']
    # Algebraically independent update and exact quadratic error identity.
    root=D(c).sqrt()
    dx=D(x)
    expected=(dx+D(c)/dx)/2
    allowance=2*D(math.ulp(proposal))
    assert abs(D(proposal)-expected)<=allowance
    error=dx-root
    next_error=D(proposal)-root
    assert abs(next_error-error*error/(2*dx))<=allowance
    assert next_error>0 and error>0
    assert result['status']=='max_iter' and result['iterations']==1
    assert result['newton_steps']==1 and result['bisection_steps']==0
    assert events[0]['x']<proposal<events[1]['x']
    a,b=result['bracket']
    assert D(a)<root<D(b)
    assert events[-1]['x']==result['root']
    assert result['residual']==events[-1]['value']
    assert abs(D(result['root'])-root)<=D(result['width'])/2+D(math.ulp(result['root']))
    return {'initial_error':error,'proposal_error':next_error,
            'coefficient':next_error/(error*error),'limit':1/(2*root)}


def audit_hybrid(c,result,events):
    a,b=events[0]['x'],events[1]['x']
    x=a+(b-a)/2
    cursor=2; newton=bisection=0; rows=[]
    for k in range(result['iterations']):
        fi,di,fp=events[cursor:cursor+3]
        assert [e['kind'] for e in (fi,di,fp)]==['f','df','f']
        assert fi['x']==di['x']==x
        candidate=x-fi['value']/di['value']
        accepted=a+(b-a)/4<candidate<b-(b-a)/4
        proposal=fp['x']
        if accepted:
            assert proposal==candidate
            independent=(D(x)+D(c)/D(x))/2
            assert abs(D(proposal)-independent)<=2*D(math.ulp(proposal))
            newton+=1
        else:
            assert proposal==a+(b-a)/2
            bisection+=1
        assert a<proposal<b
        # Known root, not callback sign multiplication, selects retained side.
        root=D(c).sqrt()
        if D(proposal)<root:
            a=proposal
        else:
            b=proposal
        assert D(a)<root<D(b)
        rows.append({'iteration':k+1,'kind':'newton' if accepted else 'bisection',
                     'proposal':proposal,'bracket':[a,b]})
        x=proposal;cursor+=3
    assert cursor==len(events)-1
    assert events[-1]['kind']=='f' and events[-1]['x']==result['root']
    assert result['residual']==events[-1]['value']
    assert result['newton_steps']==newton and result['bisection_steps']==bisection
    assert result['bracket']==(a,b) and result['width']==b-a
    assert result['status']=='converged'
    assert result['width']<=2**-35
    assert newton>0 and bisection>0
    assert len(events)==3*result['iterations']+3
    return rows


def check():
    rows=[];orders=[];hybrids=[];mutants=0
    with localcontext() as ctx:
        ctx.prec=100
        for c in (2,3,5):
            root=D(c).sqrt();family=[]
            for power in range(3,11):
                x=float(root)+2**-power
                result,events=observed(c,x-0.5,x+0.5,1)
                # Rounded bracket endpoints need not have requested x as midpoint.
                actual_x=events[2]['x']
                data=audit_single(c,actual_x,result,events)
                family.append(data)
                rows.append({'c':c,'power':power,'requested_center':x,'x':actual_x,'result':result,'events':events,
                             'reference':{k:str(v) for k,v in data.items()}})
                if c==2 and power==3:
                    for bad_result,bad_events in [
                        (dict(result,newton_steps=0),events),
                        (result,[dict(e,x=e['x']+0.01) if i==4 else e for i,e in enumerate(events)]),
                        (dict(result,status='converged'),events),
                    ]:
                        try:
                            audit_single(c,actual_x,bad_result,bad_events)
                        except AssertionError:
                            mutants+=1
            for first,second in zip(family,family[1:]):
                p=(second['proposal_error']/first['proposal_error']).ln()/(second['initial_error']/first['initial_error']).ln()
                assert D('1.9')<p<D('2.01')
                orders.append({'c':c,'observed_order':str(p)})
            assert abs(family[-1]['coefficient']/family[-1]['limit']-1)<D('0.001')
            result,events=observed(c,float(root)-0.5,float(root)+0.5,100)
            trace=audit_hybrid(c,result,events)
            hybrids.append({'c':c,'result':result,'events':events,'trace':trace})
        assert mutants==3
    return {'local_proposal_ladders':rows,'orders':orders,'full_hybrids':hybrids,
            'wrong_variants_detected':mutants,
            'scope':'24 isolated accepted Newton steps,21 local order ratios,3 actual hybrids; central safeguards may interrupt quadratic convergence; no universal hybrid-order claim'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))

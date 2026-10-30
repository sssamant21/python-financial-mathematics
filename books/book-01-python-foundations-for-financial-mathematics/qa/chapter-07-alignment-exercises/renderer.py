"""Supplemental E8 renderer for an already validated contributions() result.

Numeric fractions stay in the source report. Display strings alone use
percent formatting and contribution*100 percentage-point units.
"""
def render(report,total):
    lines=[]
    for asset,row in report.iterrows():
        lines.append(f'{asset}: weight {row["weight"]:.2%}; return {row["return"]:.2%}; contribution {100*row["contribution"]:.2f} pp')
    lines.append(f'Portfolio price return: {total:.2%}; contributions {100*total:.2f} pp')
    return '\n'.join(lines)+'\n'

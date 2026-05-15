#!/usr/bin/env python3
"""Generate 23 tile HTMLs for the 30-day deck (D3 + D8–D30).
D1, D2, D4, D5, D6, D7 reuse existing launch-week tiles.

Renders each tile as 1080×1350. Four layout variants (cover, stat, list, quote)
pick based on the post's template field. Output: d{N}_post.html files at root.
"""
import os
import textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))

# ── Post data · D3 + D8–D30 ──
POSTS = [
  # D3 · POV · text-only
  { 'day':3, 'phase':1, 'phaseName':'Launch', 'surface':'paper',
    'template':'list',
    'eyebrow':'D3 · POV · founder note',
    'hook':'A take on <em>FinOps</em> tooling.',
    'items':[
      ('It was built for the US AWS-first enterprise.', ''),
      ('Indian SaaS doesn\'t run like that.', 'Multi-cloud, INR billing, CTO-as-FinOps-team.'),
      ('You don\'t have a FinOps tool.', 'You have a dashboard.'),
    ],
    'foot':'Founder LinkedIn · text only',
  },

  # D8 · Onboarding
  { 'day':8, 'phase':2, 'phaseName':'Activate', 'surface':'dark',
    'template':'stat',
    'eyebrow':'D8 · Onboarding',
    'bignum':'<em>90</em>s',
    'numLabel':'From cloud credential to first finding.',
    'hook':'Connect read-only.<br><em>Watch us work.</em>',
    'foot':'zop.dev/signin · sq + vert · 30–60s',
  },
  # D9 · Smart Scheduling
  { 'day':9, 'phase':2, 'phaseName':'Activate', 'surface':'paper',
    'template':'stat',
    'eyebrow':'D9 · ZopNight · Smart Scheduling',
    'bignum':'<em>73</em>%',
    'numLabel':'Non-prod cycles reclaimable, average estate.',
    'hook':'Non-prod off. <em>By default.</em>',
    'foot':'zop.dev/night · live sched-grid · 15–20s',
  },
  # D10 · Auto-Remediation
  { 'day':10, 'phase':2, 'phaseName':'Activate', 'surface':'dark',
    'template':'list',
    'eyebrow':'D10 · ZopNight · Auto-Remediation',
    'hook':'Click to fix. <em>Or don\'t.</em>',
    'items':[
      ('20 certified rules.', 'Databases never touched.'),
      ('Opt-in by scope.', 'Reversible by design.'),
      ('Full audit log.', 'Every action, every actor, every time.'),
    ],
    'foot':'zop.dev/night · screen capture · 20s',
  },
  # D11 · ZopDay deploy
  { 'day':11, 'phase':2, 'phaseName':'Activate', 'surface':'paper',
    'template':'stat',
    'eyebrow':'D11 · ZopDay · Push to deploy',
    'bignum':'<em>4</em>m',
    'numLabel':'Cloud credential → live deploy. Same day.',
    'hook':'From <em>git push</em><br>to live deploy.',
    'foot':'zop.dev/day · CLI capture · 20–30s',
  },
  # D12 · ZopCloud
  { 'day':12, 'phase':2, 'phaseName':'Activate', 'surface':'dark',
    'template':'stat',
    'eyebrow':'D12 · ZopCloud · One workspace',
    'bignum':'<em>380</em>+',
    'numLabel':'Resource types under one inventory.',
    'hook':'Every cloud.<br><em>One credential.</em>',
    'foot':'zop.dev/cloud · PCB board · 15s',
  },
  # D13 · Sandbox
  { 'day':13, 'phase':2, 'phaseName':'Activate', 'surface':'paper',
    'template':'cover',
    'eyebrow':'D13 · Sandbox',
    'hook':'Try without<br><em>signing up.</em>',
    'sub':'Real anonymized multi-cloud estate. Click around. Run audits. Pull a report.',
    'foot':'zop.dev/sandbox · single image · 1080×1080',
  },
  # D14 · Week-one wrap
  { 'day':14, 'phase':2, 'phaseName':'Activate', 'surface':'paper',
    'template':'bignum',
    'eyebrow':'D14 · Week-one wrap',
    'bignum':'<em>$1.2</em>M',
    'numLabel':'Annualized spend identified · week 1.',
    'sub':'250 audits run. 6,400+ findings. Avg connect-to-first-finding: 4m 18s.',
    'foot':'zop.dev/methodology · 5-tile carousel',
  },

  # D15 · McAfee case
  { 'day':15, 'phase':3, 'phaseName':'Amplify', 'surface':'paper',
    'template':'quote',
    'eyebrow':'D15 · Customer · McAfee',
    'hook':'Multi-cloud platform engineering, <em>at scale.</em>',
    'quote':'Zop has been instrumental in simplifying our multi-cloud operations.',
    'attr':'Mahesh Tyagarajan',
    'attrTitle':'VP Platform Engineering, McAfee',
    'foot':'zop.dev/customers · 6-tile carousel',
  },
  # D16 · Azure F1000
  { 'day':16, 'phase':3, 'phaseName':'Amplify', 'surface':'dark',
    'template':'stat',
    'eyebrow':'D16 · Customer · Azure F1000',
    'bignum':'$<em>14,820</em>',
    'numLabel':'Monthly recovered · net of subscription.',
    'hook':'Azure Advisor caught 14%.<br><em>We found the rest.</em>',
    'foot':'zop.dev/azure-benchmark · 5-tile carousel',
  },
  # D17 · FMCG estate
  { 'day':17, 'phase':3, 'phaseName':'Amplify', 'surface':'paper',
    'template':'stat',
    'eyebrow':'D17 · Customer · FMCG estate',
    'bignum':'$<em>9.4</em>M',
    'numLabel':'Combined annual cloud spend · 5 estates.',
    'hook':'5 of India\'s<br>top <em>20</em> FMCG enterprises.',
    'foot':'zop.dev · 4-tile carousel · NDA',
  },
  # D18 · India SaaS
  { 'day':18, 'phase':3, 'phaseName':'Amplify', 'surface':'dark',
    'template':'list',
    'eyebrow':'D18 · POV · India SaaS reality',
    'hook':'Three things US tools <em>assume.</em>',
    'items':[
      ('One cloud, usually AWS.', 'Indian SaaS runs multi-cloud.'),
      ('One billing currency, USD.', 'You bill in INR, pay in USD.'),
      ('Dedicated FinOps team.', 'Your CTO is the FinOps team.'),
    ],
    'foot':'Founder LinkedIn · text + 3-tile callout',
  },
  # D19 · Benchmark
  { 'day':19, 'phase':3, 'phaseName':'Amplify', 'surface':'paper',
    'template':'list',
    'eyebrow':'D19 · Benchmark · ZopNight vs Azure Advisor',
    'hook':'Same estate. <em>Different tools.</em>',
    'items':[
      ('Azure Advisor', '15 recommendations · 14% of opportunity.'),
      ('ZopNight', '287 recommendations · 86% of opportunity.'),
      ('Categorized', 'By lens · cost · security · performance · reliability.'),
    ],
    'foot':'zop.dev/azure-benchmark · 4-tile carousel',
  },
  # D20 · Compliance stack
  { 'day':20, 'phase':3, 'phaseName':'Amplify', 'surface':'dark',
    'template':'list',
    'eyebrow':'D20 · Compliance · audited and current',
    'hook':'What ZopDev is <em>audited</em> against.',
    'items':[
      ('SOC 2 Type II', 'Audited annually.'),
      ('ISO 27001:2022', 'Re-certified in 2026.'),
      ('IRDAI · DPDP · MeitY', 'India regulator stack.'),
    ],
    'foot':'zop.dev/trust · 6-tile carousel',
  },
  # D21 · Customer voices
  { 'day':21, 'phase':3, 'phaseName':'Amplify', 'surface':'paper',
    'template':'quote',
    'eyebrow':'D21 · Voices · customer quotes',
    'hook':'What customers <em>actually say.</em>',
    'quote':'It\'s the only tool that actually understands we don\'t have a FinOps team.',
    'attr':'CTO',
    'attrTitle':'India SaaS · anonymized',
    'foot':'zop.dev/customers · 6-tile carousel',
  },

  # D22 · ROI calculator
  { 'day':22, 'phase':4, 'phaseName':'Convert', 'surface':'dark',
    'template':'stat',
    'eyebrow':'D22 · ROI · calculator',
    'bignum':'<em>$4.2K</em> → $84K',
    'numLabel':'Estimated monthly recovery range.',
    'hook':'Drop in your spend.<br><em>See your number.</em>',
    'foot':'zop.dev/calculator · screenshot + 3-tile carousel',
  },
  # D23 · ZopNight $/mo
  { 'day':23, 'phase':4, 'phaseName':'Convert', 'surface':'paper',
    'template':'bignum',
    'eyebrow':'D23 · ZopNight · $/mo recovered',
    'bignum':'<em>$14.2</em>K',
    'numLabel':'Median monthly recovered · this quarter.',
    'sub':'Top decile: $84K+/mo. Bottom decile: $1.8K/mo. Variance is estate size.',
    'foot':'zop.dev/audit · 5-tile carousel',
  },
  # D24 · ZopDay time saved
  { 'day':24, 'phase':4, 'phaseName':'Convert', 'surface':'dark',
    'template':'stat',
    'eyebrow':'D24 · ZopDay · time saved',
    'bignum':'<em>180</em>→24',
    'numLabel':'Engineering hours/month on platform-ops.',
    'hook':'Engineering hours<br><em>back.</em>',
    'foot':'zop.dev/day · 4-tile before/after',
  },
  # D25 · Founder offer
  { 'day':25, 'phase':4, 'phaseName':'Convert', 'surface':'paper',
    'template':'cover',
    'eyebrow':'D25 · Founder offer',
    'hook':'Free audit.<br><em>First 50 teams.</em>',
    'sub':'30-minute call. No deck. No pitch. Your estate on screen, our analysis next to it.',
    'foot':'rav@zop.dev · single image',
  },
  # D26 · Book a call
  { 'day':26, 'phase':4, 'phaseName':'Convert', 'surface':'dark',
    'template':'cover',
    'eyebrow':'D26 · Sales · book a call',
    'hook':'15 minutes.<br><em>No deck.</em>',
    'sub':'You show us your AWS/GCP/Azure. We run a live audit. Top 10 findings.',
    'foot':'zop.dev/book · 3-tile carousel',
  },
  # D27 · Objections
  { 'day':27, 'phase':4, 'phaseName':'Convert', 'surface':'paper',
    'template':'list',
    'eyebrow':'D27 · Objections · 3 things we hear',
    'hook':'Three real <em>objections.</em>',
    'items':[
      ('"We already have Azure Advisor."', 'They surface 14%. We surface the rest.'),
      ('"We can\'t add another vendor."', 'Read-only. No agent. Disconnect anytime.'),
      ('"We\'re not big enough."', 'Smallest estate we run: $4K/mo.'),
    ],
    'foot':'zop.dev · 3-tile carousel',
  },
  # D28 · Last push
  { 'day':28, 'phase':4, 'phaseName':'Convert', 'surface':'dark',
    'template':'cover',
    'eyebrow':'D28 · Last push · before month ends',
    'hook':'Last day of<br><em>the month.</em>',
    'sub':'If you connected your estate this week, your first audit report is ready by Monday.',
    'foot':'zop.dev/signin · single image · 1080×1080',
  },

  # D29 · Month wrap
  { 'day':29, 'phase':5, 'phaseName':'Reflect', 'surface':'paper',
    'template':'bignum',
    'eyebrow':'D29 · Month wrap · numbers run',
    'bignum':'<em>$4.8</em>M',
    'numLabel':'Annualized spend identified · month 1.',
    'sub':'1,180 audits run. 28,400+ findings. 247 teams onboarded. 12 of India\'s top 100 SaaS.',
    'foot':'zop.dev/methodology · 5-tile carousel',
  },
  # D30 · What ships next
  { 'day':30, 'phase':5, 'phaseName':'Reflect', 'surface':'paper',
    'template':'list',
    'eyebrow':'D30 · What ships next · roadmap',
    'hook':'Landing <em>next month.</em>',
    'items':[
      ('ZopNight v1.6', 'Predictive scheduling, learns your org\'s rhythm.'),
      ('ZopDay', 'Push-to-deploy on GKE and AKS, parity with EKS.'),
      ('ZopCloud', 'OpenTofu integration alongside Terraform.'),
    ],
    'foot':'zop.dev/roadmap · 3-tile carousel',
  },
]


# ── Shared HTML head/body shell ──
SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>D{day} · {phaseName} · {eyebrow}</title>
<link rel="stylesheet" href="kit.css">
<style>
  .canvas {{ width: 1080px; height: 1350px; padding: 80px 80px; display: flex; flex-direction: column; }}
  .canvas.paper {{ background: var(--paper); color: var(--ink); }}
  .canvas.dark  {{ background: var(--ink-d); color: var(--cream); }}
  .top {{ display: flex; justify-content: space-between; align-items: center; }}
  .top .l {{ font-family: var(--mono); font-weight: 500; font-size: 12px; letter-spacing: 0.16em; text-transform: uppercase; display: inline-flex; align-items: center; gap: 12px; }}
  .top .l::before {{ content: ''; width: 10px; height: 10px; background: var(--zop-orange); }}
  .top .pg {{ font-family: var(--mono); font-weight: 500; font-size: 12px; letter-spacing: 0.16em; text-transform: uppercase; }}
  .canvas.paper .top .l, .canvas.paper .top .pg {{ color: var(--g-600); }}
  .canvas.dark  .top .l, .canvas.dark  .top .pg {{ color: var(--g-600-d); }}
  .foot {{ margin-top: auto; padding-top: 28px; border-top: 1px solid currentColor; display: flex; justify-content: space-between; align-items: flex-end; font-family: var(--mono); font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; }}
  .canvas.paper .foot {{ border-top-color: var(--line); color: var(--g-600); }}
  .canvas.dark  .foot {{ border-top-color: var(--line-d); color: var(--g-600-d); }}
  .sig {{ position: absolute; width: 10px; height: 10px; background: var(--zop-orange); bottom: 32px; right: 32px; }}
  .cross {{ position: absolute; width: 8px; height: 8px; opacity: 0.4; }}
  .canvas.paper .cross {{ color: var(--line); }}
  .canvas.dark  .cross {{ color: var(--line-d); }}
  .cross::before, .cross::after {{ content: ''; position: absolute; background: currentColor; }}
  .cross::before {{ left: 0; right: 0; top: 50%; height: 1px; }}
  .cross::after  {{ top: 0; bottom: 0; left: 50%; width: 1px; }}
  em {{ font-style: normal; color: var(--zop-orange); }}

  /* Templates */
  .body {{ flex: 1; display: flex; flex-direction: column; }}

  /* Cover: centered headline */
  .body.cover {{ justify-content: center; gap: 32px; }}
  .body.cover .hook {{ font-family: var(--font); font-weight: 700; font-size: 124px; line-height: 0.95; letter-spacing: -0.045em; max-width: 920px; }}
  .body.cover .sub {{ font-family: var(--font); font-weight: 500; font-size: 32px; line-height: 1.25; letter-spacing: -0.025em; max-width: 800px; }}
  .canvas.paper .body.cover .sub {{ color: var(--g-700); }}
  .canvas.dark  .body.cover .sub {{ color: var(--g-600-d); }}

  /* Stat: hook on top, big number on bottom */
  .body.stat {{ justify-content: space-between; padding-top: 24px; padding-bottom: 12px; }}
  .body.stat .hook {{ font-family: var(--font); font-weight: 700; font-size: 88px; line-height: 0.98; letter-spacing: -0.04em; max-width: 920px; }}
  .body.stat .num-block {{ display: flex; flex-direction: column; gap: 16px; padding-top: 28px; border-top: 1px solid currentColor; }}
  .canvas.paper .body.stat .num-block {{ border-top-color: var(--line); }}
  .canvas.dark  .body.stat .num-block {{ border-top-color: var(--line-d); }}
  .body.stat .bignum {{ font-family: var(--font); font-weight: 700; font-size: 240px; line-height: 0.88; letter-spacing: -0.06em; }}
  .body.stat .numLabel {{ font-family: var(--mono); font-size: 16px; letter-spacing: 0.14em; text-transform: uppercase; }}
  .canvas.paper .body.stat .numLabel {{ color: var(--g-600); }}
  .canvas.dark  .body.stat .numLabel {{ color: var(--g-600-d); }}

  /* List: hook + 3-row list */
  .body.list {{ justify-content: center; gap: 36px; }}
  .body.list .hook {{ font-family: var(--font); font-weight: 700; font-size: 88px; line-height: 0.98; letter-spacing: -0.04em; max-width: 920px; }}
  .body.list .items {{ display: flex; flex-direction: column; gap: 0; }}
  .body.list .item {{ display: flex; flex-direction: column; gap: 8px; padding: 22px 0; border-bottom: 1px solid currentColor; }}
  .body.list .item:last-child {{ border-bottom: 0; }}
  .canvas.paper .body.list .item {{ border-bottom-color: var(--line); }}
  .canvas.dark  .body.list .item {{ border-bottom-color: var(--line-d); }}
  .body.list .item .h {{ font-family: var(--font); font-weight: 600; font-size: 36px; letter-spacing: -0.025em; line-height: 1.05; }}
  .body.list .item .h em {{ color: var(--zop-orange); }}
  .body.list .item .d {{ font-family: var(--font-body); font-size: 18px; line-height: 1.45; }}
  .canvas.paper .body.list .item .d {{ color: var(--g-600); }}
  .canvas.dark  .body.list .item .d {{ color: var(--g-600-d); }}

  /* Quote */
  .body.quote {{ justify-content: center; gap: 32px; }}
  .body.quote .hook {{ font-family: var(--font); font-weight: 700; font-size: 64px; line-height: 1.0; letter-spacing: -0.035em; max-width: 880px; }}
  .body.quote .q {{ font-family: var(--font); font-weight: 500; font-size: 44px; line-height: 1.15; letter-spacing: -0.025em; border-left: 6px solid var(--zop-orange); padding-left: 32px; max-width: 880px; }}
  .canvas.paper .body.quote .q {{ color: var(--ink); }}
  .canvas.dark  .body.quote .q {{ color: var(--cream); }}
  .body.quote .attr {{ padding-left: 38px; display: flex; flex-direction: column; gap: 4px; }}
  .body.quote .attr .n {{ font-family: var(--font); font-weight: 600; font-size: 22px; letter-spacing: -0.02em; }}
  .body.quote .attr .t {{ font-family: var(--mono); font-size: 12px; letter-spacing: 0.16em; text-transform: uppercase; }}
  .canvas.paper .body.quote .attr .t {{ color: var(--g-600); }}
  .canvas.dark  .body.quote .attr .t {{ color: var(--g-600-d); }}

  /* Bignum: hook smaller, number huge in center */
  .body.bignum {{ justify-content: center; gap: 28px; }}
  .body.bignum .bignum {{ font-family: var(--font); font-weight: 700; font-size: 300px; line-height: 0.88; letter-spacing: -0.06em; }}
  .body.bignum .numLabel {{ font-family: var(--font); font-weight: 600; font-size: 36px; letter-spacing: -0.025em; line-height: 1.15; max-width: 800px; }}
  .body.bignum .sub {{ font-family: var(--font-body); font-size: 20px; line-height: 1.5; max-width: 820px; }}
  .canvas.paper .body.bignum .sub {{ color: var(--g-600); }}
  .canvas.dark  .body.bignum .sub {{ color: var(--g-600-d); }}
</style></head>
<body><div class="canvas {surface}">
  <span class="cross" style="top:24px; left:24px;"></span><span class="cross" style="top:24px; right:24px;"></span>
  <span class="cross" style="bottom:24px; left:24px;"></span><span class="cross" style="bottom:24px; right:24px;"></span>
  <span class="sig"></span>
  <div class="top">
    <span class="l">{eyebrow}</span>
    <span class="pg">{phaseLabel}</span>
  </div>
  <div class="body {template}">
    {bodyContent}
  </div>
  <div class="foot">
    <span>zop.dev</span>
    <span>{foot}</span>
  </div>
</div></body></html>
"""


def body_cover(p):
  return f'<h2 class="hook">{p["hook"]}</h2><p class="sub">{p["sub"]}</p>'

def body_stat(p):
  return f'<h2 class="hook">{p["hook"]}</h2><div class="num-block"><div class="bignum">{p["bignum"]}</div><div class="numLabel">{p["numLabel"]}</div></div>'

def body_list(p):
  rows = []
  for h, d in p['items']:
    detail = ('<span class="d">' + d + '</span>') if d else ''
    rows.append('<div class="item"><span class="h">' + h + '</span>' + detail + '</div>')
  items_html = ''.join(rows)
  return f'<h2 class="hook">{p["hook"]}</h2><div class="items">{items_html}</div>'

def body_quote(p):
  return (
    f'<h2 class="hook">{p["hook"]}</h2>'
    f'<div class="q">"{p["quote"]}"</div>'
    f'<div class="attr"><span class="n">— {p["attr"]}</span><span class="t">{p["attrTitle"]}</span></div>'
  )

def body_bignum(p):
  return f'<div class="bignum">{p["bignum"]}</div><div class="numLabel">{p["numLabel"]}</div><p class="sub">{p["sub"]}</p>'


BUILDERS = {
  'cover':  body_cover,
  'stat':   body_stat,
  'list':   body_list,
  'quote':  body_quote,
  'bignum': body_bignum,
}


def main():
  for p in POSTS:
    builder = BUILDERS[p['template']]
    body = builder(p)
    phase_label = f'P{p["phase"]} · {p["phaseName"]}'
    html = SHELL.format(
      day=p['day'],
      phaseName=p['phaseName'],
      eyebrow=p['eyebrow'],
      phaseLabel=phase_label,
      surface=p['surface'],
      template=p['template'],
      bodyContent=body,
      foot=p['foot'],
    )
    path = os.path.join(ROOT, f'd{p["day"]}_post.html')
    with open(path, 'w') as f:
      f.write(html)
    print(f'  → d{p["day"]}_post.html · {p["template"]}')

  print(f'\nGenerated {len(POSTS)} tile HTMLs.')


if __name__ == '__main__':
  main()

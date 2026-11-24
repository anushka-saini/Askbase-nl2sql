# small html helpers + the css for the app (cards, status badges, steps)

from html import escape

# prompt version -> fixed chart colour (same order as chartCategoricalColors in .streamlit/config.toml)
VERSION_COLORS = {"v0": "#3987e5", "v1": "#d95926", "v2": "#199e70", "v3": "#c98500", "v4": "#d55181", "v5": "#008300"}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="st-"], .stMarkdown {font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;}
#MainMenu, footer, [data-testid="stDecoration"] {visibility: hidden; height: 0;}
header[data-testid="stHeader"] {background: transparent;}
.block-container {padding-top: 1rem; padding-bottom: 1rem; max-width: 1280px;}

/* top bar */
.appbar {display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: .7rem 1.1rem; margin-bottom: .9rem;
         background: #111827; border: 1px solid #1f2937; border-radius: 12px;}
.brand {display: flex; align-items: center; gap: .7rem;}
.logo {width: 34px; height: 34px; border-radius: 9px; background: linear-gradient(135deg, #6366f1, #38bdf8); color: #fff;
       font-weight: 700; display: flex; align-items: center; justify-content: center;}
.brand .nm {font-weight: 700; font-size: 1.15rem; line-height: 1.1;}
.brand .tg {color: #9ca3af; font-size: .82rem;}
.mode {color: #9ca3af; font-size: .82rem; display: flex; align-items: center; gap: .45rem;}
.mode:before {content: ""; width: 8px; height: 8px; border-radius: 50%; background: #10b981; display: inline-block;}

/* tabs as navigation */
div[data-baseweb="tab-list"] {gap: .3rem; border-bottom: 1px solid #1f2937;}
button[data-baseweb="tab"] {padding: .55rem 1rem; font-weight: 500; color: #9ca3af; border-radius: 8px 8px 0 0;}
button[data-baseweb="tab"][aria-selected="true"] {color: #fff; font-weight: 600;}
div[data-baseweb="tab-highlight"] {background: #6366f1; height: 3px;}

/* panels, inputs, buttons */
div[data-testid="stVerticalBlockBorderWrapper"] {background: #111827; border-color: #1f2937; border-radius: 12px;}
div[data-testid="stExpander"] {border-radius: 12px; background: #111827;}
div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button {border-radius: 8px; font-weight: 500;}
div[data-testid="stButton"] button[kind="primary"] {background: #6366f1; border: none; color: #fff; font-weight: 600;}
div[data-testid="stButton"] button[kind="primary"]:hover {background: #4f52d6;}
textarea, input {border-radius: 8px !important;}
div[data-testid="stMetric"] {background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: .7rem 1rem;}
div[data-testid="stMetricLabel"] {color: #9ca3af;}
div[data-testid="stMetricValue"] {font-size: 1.5rem; font-weight: 600;}
div[data-testid="stDataFrame"] {border-radius: 10px; overflow: hidden;}
section[data-testid="stSidebar"] {background: #0e1422;}
h4 {font-size: 1.05rem; font-weight: 600; margin-top: .6rem;}

/* section headings */
.sec {font-weight: 600; font-size: 1.02rem; margin: .1rem 0 .15rem 0;}
.sub {color: #9ca3af; font-size: .86rem; margin-bottom: .5rem;}

/* result bar and steps */
.rbar {display: flex; flex-wrap: wrap; gap: .6rem 1.6rem; align-items: center; background: #111827; border: 1px solid #1f2937;
       border-radius: 12px; padding: .7rem 1.1rem; margin: .2rem 0 .8rem 0;}
.rbar .k {color: #9ca3af; font-size: .74rem; text-transform: uppercase; letter-spacing: .05em; margin-right: .5rem;}
.callout {border-left: 3px solid #4b5563; background: #111827; border-radius: 0 10px 10px 0; padding: .55rem .95rem; margin: .6rem 0;}
.callout.fail {border-left-color: #f87171;} .callout.warn {border-left-color: #f59e0b;}
.callout b {display: block; margin-bottom: .1rem;}
.step {background: #111827; border: 1px solid #1f2937; border-top: 3px solid #4b5563; border-radius: 12px; padding: .65rem .85rem; min-height: 100px;}
.step.ok {border-top-color: #10b981;} .step.warn {border-top-color: #f59e0b;} .step.fail {border-top-color: #f87171;}
.step .name {font-weight: 600; font-size: .9rem; margin-bottom: .2rem;}
.step .detail {color: #9ca3af; font-size: .8rem; margin-top: .3rem; word-break: break-word; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;}
.muted {color: #9ca3af; font-size: .86rem;}
.res {font-weight: 600;}
.res:before {content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: .4rem; background: currentColor;}
.ok {color: #34d399;} .warn {color: #fbbf24;} .fail {color: #f87171;} .info, .skip {color: #9ca3af;}
.empty {border-left: 3px solid #374151; padding: .5rem .9rem; color: #9ca3af; margin: .5rem 0 .8rem 0;}
.empty b {color: #e5e7eb; display: block; margin-bottom: .2rem;}
.side-k {color: #9ca3af; font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; margin-top: .6rem;}
.side-v {font-weight: 600; font-size: .9rem;}
.footer {text-align: center; color: #6b7280; font-size: .8rem; margin-top: 1.5rem; padding-top: .8rem; border-top: 1px solid #1f2937;}
</style>
"""

# state -> (css class, word)
STATE = {"ok": ("ok", "OK"), "warn": ("warn", "Warning"), "fail": ("fail", "Failed"),
         "skip": ("skip", "Skipped"), "info": ("info", "Info")}

# pipeline status -> state + label
STATUS = {"ok": ("ok", "Answered"), "empty": ("warn", "No rows"), "refused": ("warn", "Refused"),
          "blocked": ("fail", "Blocked"), "invalid": ("fail", "Rejected"), "error": ("fail", "SQL error"),
          "llm_error": ("fail", "No answer")}


def badge(state, text=None):
    # coloured text, no pill: green = ok, amber = warning, red = failed
    cls, default = STATE.get(state, STATE["skip"])
    return f'<span class="res {cls}">{escape(text) if text else default}</span>'


def status_badge(status):
    cls, text = STATUS.get(status, ("skip", status))
    return f'<span class="res {cls}">{escape(text)}</span>'


def step_card(step):
    st_ = step["state"]
    return (f'<div class="step {st_}"><div class="name">{escape(step["name"])}</div>{badge(st_)}'
            f'<div class="detail">{escape(str(step["detail"])[:220])}</div></div>')


def callout(kind, title, body=""):
    return f'<div class="callout {kind}"><b>{escape(title)}</b>{escape(body)}</div>'


def empty(title, body):
    return f'<div class="empty"><b>{escape(title)}</b>{escape(body)}</div>'


def side(k, v):
    return f'<div class="side-k">{escape(k)}</div><div class="side-v">{escape(str(v))}</div>'



def appbar(offline):
    mode = "Demo mode: stored evaluation runs, no live model call" if offline else "Live mode: calls the model"
    return ('<div class="appbar"><div class="brand"><div class="logo">A</div><div><div class="nm">AskBase</div>'
            '<div class="tg">Ask the Olist shop database a question in plain English. See the SQL, the answer and the safety check.</div></div></div>'
            f'<div class="mode">{escape(mode)}</div></div>')


def section(title, sub=""):
    return f'<div class="sec">{escape(title)}</div>' + (f'<div class="sub">{escape(sub)}</div>' if sub else "")


FOOTER = '<div class="footer">Team AskBase - PE-B01-16</div>'

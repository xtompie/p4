"""Draws levels.svg: one process (P-01 Place order) at the four P4 levels.

Usage: python make-diagram.py <JetBrainsMono-Regular.ttf> <JetBrainsMono-Bold.ttf>   (needs fontTools)
The font is embedded as a subset, so the image looks the same everywhere.
"""
import base64, io, os, sys
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
BG, W, L, M, D = "#0a0907", "#f3f2f9", "#d8d4ec", "#b1a9d8", "#908ab5"
TXT, DIM, LINE = "#cfc6b4", "#8a7a5c", "#3a3122"

def font(path, weight):
    opts = subset.Options(); opts.layout_features = []; opts.name_IDs = []
    f = TTFont(path); s = subset.Subsetter(opts)
    s.populate(unicodes=list(range(0x20, 0x7f)) + [0xB7, 0x2192, 0x2191, 0x2193, 0x2013]); s.subset(f)
    b = io.BytesIO(); f.save(b)
    return f"@font-face {{ font-family: JBM; font-weight: {weight}; src: url(data:font/ttf;base64,{base64.b64encode(b.getvalue()).decode()}) format('truetype'); }}"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def logo(x, y, u):
    r = lambda a, b, w, h, c: f'<rect x="{x+a*u:.1f}" y="{y+b*u:.1f}" width="{w*u:.1f}" height="{h*u:.1f}" fill="{c}"/>'
    o = r(0, 0, 7.5, 7.5, W)
    o += "".join(r(8.5 + i * 3.85, j * 3.85, 3.25, 3.25, L) for i in range(2) for j in range(2))
    o += "".join(r(i * 1.95, 8.5 + j * 1.95, 1.45, 1.45, M) for i in range(4) for j in range(4))
    st = 7.5 / 8
    o += "".join(r(8.5 + i * st, 8.5 + j * st, st * .62, st * .62, D) for i in range(8) for j in range(8))
    return o

def chamfer(x, y, w, h, c=14): return f"M{x+c} {y} H{x+w} V{y+h-c} L{x+w-c} {y+h} H{x} V{y+c} Z"

LEVELS = [
    ("P1", "PROCESSES", "Which processes are there?", W, [
        ("t", "P-01 Place order: the customer submits an order from the cart.")]),
    ("P2", "CONTRACTS", "What goes in and what comes out?", L, [
        ("t", "Input: products with quantities, delivery address, email."),
        ("t", "Output: the customer sees the order number."),
        ("t", "Effects: the order is created, a confirmation email is sent."),
        ("t", "Errors: a product ran out → no order is created.")]),
    ("P3", "IMPLEMENTATION", "What happens inside?", M, [
        ("t", "Steps: check stock → recalculate prices → reserve stock → save."),
        ("t", "Data: orders, order items, stock reservations."),
        ("t", "Place: Orders module, same approach as creating a return.")]),
    ("P4", "CODE", "What does the code look like?", D, [
        ("c", "PlaceOrderCommand { items, shipping, email, formToken }"),
        ("c", "PlaceOrderHandler::handle(PlaceOrderCommand): OrderNumber"),
        ("c", "orders(id, number, email, status, total, form_token)")]),
]

def build(css):
    Wd, x0, lab = 1280, 40, 370
    o = logo(x0, 28, 3.6) + f'<text x="{x0+80}" y="66" class="title">One process, four levels of detail.</text>'
    y = 130
    for i, (n, name, q, col, lines) in enumerate(LEVELS):
        h = max(84, 40 + len(lines) * 30)
        o += f'<path d="{chamfer(x0, y, Wd-2*x0, h)}" fill="none" stroke="{col}" stroke-width="1.6"/>'
        o += f'<text x="{x0+24}" y="{y+36}" class="num" fill="{col}">{n}</text>'
        o += f'<text x="{x0+84}" y="{y+34}" class="lvl" fill="{col}">{name}</text>'
        o += f'<text x="{x0+84}" y="{y+58}" class="q">{esc(q)}</text>'
        for k, (kind, s) in enumerate(lines):
            o += f'<text x="{x0+lab+20}" y="{y+34+k*30}" class="{"code" if kind == "c" else "body"}">{esc(s)}</text>'
        y += h + 22
        if i == 1:
            y += 30
            o += f'<line x1="{x0}" y1="{y}" x2="{Wd-x0}" y2="{y}" stroke="{M}" stroke-width="2" stroke-dasharray="10 6"/>'
            o += f'<text x="{x0}" y="{y-12}" class="edge">↑ visible from outside the system: what it does, anyone can read it</text>'
            o += f'<text x="{x0}" y="{y+28}" class="edge">↓ inside the system: where and how to build it</text>'
            y += 58
    H = y + 10
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {H}" width="{Wd}" height="{H}" role="img" '
            f'aria-label="One process, P-01 Place order, described at the four P4 levels: processes, contracts, implementation plan, pseudocode. Levels 1 and 2 are visible from outside the system, levels 3 and 4 are inside.">'
            f'<style>{css}</style><rect width="{Wd}" height="{H}" fill="{BG}"/>{o}</svg>')

css = font(sys.argv[1], 400) + font(sys.argv[2], 700) + f"""
text {{ font-family: JBM, ui-monospace, monospace; }}
.title {{ font-size: 26px; fill: #f3ead8; }}
.num {{ font-size: 24px; font-weight: 700; }}
.lvl {{ font-size: 15px; letter-spacing: 2px; font-weight: 700; }}
.q {{ font-size: 14px; fill: {DIM}; }}
.body {{ font-size: 17px; fill: {TXT}; }}
.code {{ font-size: 16px; fill: {L}; }}
.edge {{ font-size: 15px; fill: {M}; }}
"""
open(os.path.join(HERE, "levels.svg"), "w").write(build(css))
print("ok")

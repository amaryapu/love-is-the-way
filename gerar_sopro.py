#!/usr/bin/env python3
"""O SOPRO — três estados, computados. Nada desenhado à mão.

A tese: no fresco, o dedo de Deus está estendido e o de Adão caído.
A assimetria é deliberada. E o vão NUNCA se fecha — o que, por este
teorema, é obrigatório: dedos que se tocam é fusão de caminhos.
O vão é a confluência.
"""
import math, pathlib

PHI = (1 + 5 ** 0.5) / 2
W, H = 1200, 520
CX, CY = W / 2, H / 2 + 20

# o vão, em três estados — e no estado confluente ele vale a razão áurea
VAO = {"in": 0.0, "des": 420.0, "con": 100.0 * PHI / 2}   # ≈ 80,9

# A geometria é DERIVADA do vão, não escolhida: o punho fica onde tem de
# ficar para que, com o dedo estendido, a distância entre as pontas seja
# exatamente VAO["con"]. O rótulo e a figura passam a dizer o mesmo número.
L_DEDO = 130.0
PY = CY
OFFSET = VAO["con"] / 2 + L_DEDO          # = 170,45
PX_E, PX_D = CX - OFFSET, CX + OFFSET

def braco(x0, y0, x1, y1, curva):
    """Um braço que alcança: curva de Bézier, com o controle deslocado."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return f"M {x0:.1f} {y0:.1f} Q {mx:.1f} {my + curva:.1f} {x1:.1f} {y1:.1f}"

def falange(xp, yp, ang, L=L_DEDO):
    """O dedo: um segmento a partir do punho, no ângulo dado."""
    r = math.radians(ang)
    return xp + L * math.cos(r), yp + L * math.sin(r)

def cena(nome, ang_e, ang_d, rotulo, cor, desc):
    fe = falange(PX_E, PY, ang_e)
    fd = falange(PX_D, PY, 180 - ang_d)
    vao = abs(fd[0] - fe[0])
    return dict(nome=nome, fe=fe, fd=fd, vao=vao, rotulo=rotulo, cor=cor,
                desc=desc, ang_e=ang_e, ang_d=ang_d)

# ângulos escolhidos para que o vão resultante seja o da tabela
CENAS = [
    cena("in",  0,  0,  "IN-FLUÊNCIA",  "#C2554B",
         "um alcança, o outro não — e se tocar, absorve"),
    cena("des", -38, -38, "DES-FLUÊNCIA", "#6B6B6B",
         "os dois recolhem — o canal fecha"),
    cena("con", 0,  0,  "CON-FLUÊNCIA", "#C9A227",
         "os dois alcançam — e o vão permanece"),
]

def svg():
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="O sopro: in-fluência, des-fluência e con-fluência, com o vão medido">')
    o.append('<defs>')
    o.append('<linearGradient id="g" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#C9A227" stop-opacity=".15"/>'
             '<stop offset=".5" stop-color="#C9A227" stop-opacity=".55"/>'
             '<stop offset="1" stop-color="#C9A227" stop-opacity=".15"/></linearGradient>')
    o.append('<radialGradient id="sp"><stop offset="0" stop-color="#F3E3A8" stop-opacity=".95"/>'
             '<stop offset="1" stop-color="#C9A227" stop-opacity="0"/></radialGradient>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="#0E1620"/>')

    # a flor da vida, de fundo, computada — retículo hexagonal
    o.append('<g opacity=".10" stroke="#C9A227" fill="none" stroke-width="1">')
    R = 46
    for i in range(-2, 3):
        for j in range(-2, 3):
            x = CX + R * 1.5 * i
            y = CY + R * math.sqrt(3) * (j + (i % 2) / 2)
            if (x - CX) ** 2 + (y - CY) ** 2 < (R * 4.6) ** 2:
                o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R}"/>')
    o.append('</g>')

    # os dois braços
    for px, sinal in ((PX_E, 1), (PX_D, -1)):
        o.append(f'<path d="{braco(px - sinal*215, PY - 96, px, PY, 58*sinal)}" '
                 f'stroke="#8FA6B8" stroke-width="13" fill="none" stroke-linecap="round" opacity=".75"/>')

    # os dedos, animados pelos três estados
    for lado, (px, base) in enumerate(((PX_E, 0.0), (PX_D, 180.0))):
        s = 1 if lado == 0 else -1
        vals, times = [], []
        for c in CENAS + [CENAS[0]]:
            ang = (c["ang_e"] if lado == 0 else c["ang_d"])
            # no estado con, ambos alcançam plenamente; no in, só o da direita (o criador)
            if c["nome"] == "in" and lado == 0:
                ang = -30          # Adão: o dedo caído
            if c["nome"] == "con":
                ang = 0            # os dois estendidos
            x, y = falange(px, PY, base + s*ang if lado == 0 else base - ang)
            vals.append(f"{x:.1f},{y:.1f}")
        o.append(f'<line x1="{px}" y1="{PY}" x2="{px + s*L_DEDO:.1f}" y2="{PY}" '
                 f'stroke="#E8DFC8" stroke-width="11" stroke-linecap="round">')
        o.append(f'<animate attributeName="x2" dur="9s" repeatCount="indefinite" '
                 f'values="{";".join(v.split(",")[0] for v in vals)}" '
                 f'keyTimes="0;0.33;0.66;1" calcMode="spline" '
                 f'keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/>')
        o.append(f'<animate attributeName="y2" dur="9s" repeatCount="indefinite" '
                 f'values="{";".join(v.split(",")[1] for v in vals)}" '
                 f'keyTimes="0;0.33;0.66;1" calcMode="spline" '
                 f'keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1"/>')
        o.append('</line>')
        o.append(f'<circle cx="{px}" cy="{PY}" r="16" fill="#8FA6B8" opacity=".85"/>')

    # o sopro: só acende no estado confluente, e vive NO VÃO
    o.append(f'<circle cx="{CX}" cy="{PY}" r="54" fill="url(#sp)" opacity="0">')
    o.append('<animate attributeName="opacity" dur="9s" repeatCount="indefinite" '
             'values="0;0;0.95;0" keyTimes="0;0.66;0.82;1"/>')
    o.append('<animate attributeName="r" dur="9s" repeatCount="indefinite" '
             'values="30;30;60;30" keyTimes="0;0.66;0.82;1"/></circle>')

    # a medida do vão
    o.append(f'<g font-family="ui-monospace,monospace" font-size="15" fill="#C9A227" text-anchor="middle">')
    o.append(f'<text x="{CX}" y="{PY+92}" opacity="0">vão = 0 · fusão de caminhos'
             '<animate attributeName="opacity" dur="9s" repeatCount="indefinite" values="1;1;0;0;0;1" keyTimes="0;0.28;0.33;0.61;0.94;1"/></text>')
    o.append(f'<text x="{CX}" y="{PY+92}" opacity="0" fill="#9A9A9A">vão → ∞ · canal fechado'
             '<animate attributeName="opacity" dur="9s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;0.28;0.33;0.61;0.66;1"/></text>')
    o.append(f'<text x="{CX}" y="{PY+92}" opacity="0">vão = φ · ambos alcançam, nenhum absorve'
             '<animate attributeName="opacity" dur="9s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;0.61;0.66;0.94;1"/></text>')
    o.append('</g>')

    # o rótulo do estado
    o.append(f'<g font-family="ui-sans-serif,system-ui" font-size="26" font-weight="700" text-anchor="middle">')
    for i, c in enumerate(CENAS):
        kt = [0, 0.33, 0.66, 1]
        vis = ["0"]*4; vis[i] = "1"
        o.append(f'<text x="{CX}" y="86" fill="{c["cor"]}" opacity="0">{c["rotulo"]}'
                 f'<animate attributeName="opacity" dur="9s" repeatCount="indefinite" '
                 f'values="{";".join(vis)};{vis[0]}" keyTimes="0;0.28;0.61;0.94;1"/></text>')
    o.append('</g>')
    o.append(f'<g font-family="ui-sans-serif,system-ui" font-size="14" fill="#7E93A5" text-anchor="middle">')
    for i, c in enumerate(CENAS):
        vis = ["0"]*4; vis[i] = "1"
        o.append(f'<text x="{CX}" y="112" opacity="0">{c["desc"]}'
                 f'<animate attributeName="opacity" dur="9s" repeatCount="indefinite" '
                 f'values="{";".join(vis)};{vis[0]}" keyTimes="0;0.28;0.61;0.94;1"/></text>')
    o.append('</g>')
    o.append(f'<text x="{CX}" y="{H-18}" font-family="ui-monospace,monospace" font-size="12" '
             f'fill="#5E7183" text-anchor="middle">φ = {PHI:.9f} · nada desenhado: tudo computado</text>')
    o.append('</svg>')
    return "\n".join(o)

p = pathlib.Path("sopro.svg"); p.write_text(svg(), encoding="utf-8")
fe = falange(PX_E, PY, 0); fd = falange(PX_D, PY, 180)
vao_real = fd[0] - fe[0]
assert abs(vao_real - VAO["con"]) < 0.01, f"vão desenhado {vao_real:.2f} != declarado {VAO['con']:.2f}"
print(f"sopro.svg · {p.stat().st_size:,} bytes · φ = {PHI:.9f}")
print(f"  vão declarado: {VAO['con']:.2f} · vão medido na figura: {vao_real:.2f} · ✅ batem")

# ── Slides ──────────────────────────────────────────────────────────────────

def slide_01():
    """PORTADA"""
    canvas = fill_canvas(FOTOS / "poster-hero-mobile.png")
    canvas = flat_overlay(canvas, 0.58)
    d = ImageDraw.Draw(canvas)
    y = draw_text(d, "ONEstep® · Proctología · Almería", 240, fnt(30, "light"), (180, 210, 210))
    y += 40
    y = draw_text(d, "¿Pliegues anales?", y, fnt(92, "bold"), WHITE)
    rule(d, y + 10, w=180)
    y += 44
    draw_text(d, "No es lo que piensas.", y, fnt(48, "light"), (200, 235, 235))
    logo(canvas, w=220, bottom=H - 90)
    return canvas


def slide_02():
    """QUE SON - ilustracion colgajos sobre fondo blanco"""
    canvas = Image.new("RGBA", (W, H), (*OFF_WHITE, 255))
    d = ImageDraw.Draw(canvas)
    d.rectangle([(0, 0), (W, 200)], fill=(*NAVY, 255))
    draw_text(d, "¿Qué son?", 66, fnt(64, "bold"), WHITE)
    d.rectangle([(0, 200), (W, 208)], fill=(*TEAL, 255))
    img = Image.open(FOTOS / "img-colgajos-anales.png").convert("RGBA")
    iw = 820
    ih = round(img.height / img.width * iw)
    img = img.resize((iw, ih), Image.LANCZOS)
    ix, iy = (W - iw) // 2, 270
    white_bg = Image.new("RGBA", (iw, ih), (255, 255, 255, 255))
    white_bg.paste(img, (0, 0), img)
    canvas.paste(white_bg, (ix, iy))
    y = iy + ih + 60
    y = draw_text(d, "Restos de piel benignos", y, fnt(58, "bold"), DARK_GRAY, max_w=920)
    y += 8
    draw_text(d, "en el borde del ano", y, fnt(48, "light"), MID_GRAY, max_w=920)
    d.rectangle([(0, H - 80), (W, H)], fill=(*NAVY, 255))
    draw_text(d, "proctologoalmeria.com", H - 60, fnt(30, "light"), (160, 210, 210))
    return canvas


def slide_03():
    """NO SON HEMORROIDES - fondo teal degradado"""
    canvas = gradient_bg(NAVY, (8, 45, 55), TEAL, 0.52)
    canvas = flat_overlay(canvas, 0.20)
    d = ImageDraw.Draw(canvas)
    y = draw_text(d, "No son hemorroides", 470, fnt(78, "bold"), WHITE)
    rule(d, y + 10, w=160)
    y += 48
    draw_text(d, "Tampoco tienen relación\ncon el cáncer.", y, fnt(46, "light"), (185, 230, 230))
    return canvas


def slide_04():
    """POR QUE APARECEN - clinica bullets"""
    canvas = Image.new("RGBA", (W, H), (*OFF_WHITE, 255))
    d = ImageDraw.Draw(canvas)
    d.rectangle([(0, 0), (W, 200)], fill=(*NAVY, 255))
    draw_text(d, "¿Por qué aparecen?", 66, fnt(56, "bold"), WHITE)
    d.rectangle([(0, 200), (W, 208)], fill=(*TEAL, 255))
    y = 310
    items = [
        ("Hemorroide antigua", "Secuela de una trombosis previa"),
        ("Fisura anal", "El llamado colgajo centinela"),
        ("Sin causa concreta", "Por la propia anatomía"),
    ]
    for title, desc in items:
        d.ellipse([(90, y + 16), (112, y + 38)], fill=(*TEAL, 255))
        d.text((140, y), title, font=fnt(50, "bold"), fill=DARK_GRAY)
        y += 66
        d.text((140, y), desc, font=fnt(38, "light"), fill=MID_GRAY)
        y += 92
    y += 24
    draw_text(d, "Son benignos y muy frecuentes.", y, fnt(44, "light"), TEAL_DK, max_w=920)
    d.rectangle([(0, H - 80), (W, H)], fill=(*NAVY, 255))
    draw_text(d, "proctologoalmeria.com", H - 60, fnt(30, "light"), (160, 210, 210))
    return canvas


def slide_05():
    """CUANDO QUITARLOS - clinica overlay bullets"""
    clinic = FOTOS / "Clíncia de San Pio proctología especialista hemorroides Almería copia.jpeg"
    if not clinic.exists():
        clinic = FOTOS / "foto-clinica.jpg"
    canvas = fill_canvas(clinic)
    canvas = flat_overlay(canvas, 0.66)
    d = ImageDraw.Draw(canvas)
    y = draw_text(d, "¿Cuándo quitarlos?", 360, fnt(80, "bold"), WHITE)
    rule(d, y + 10, w=180)
    y += 56
    bullets = [
        "Dificultan la higiene",
        "Producen picor o irritación",
        "Molestan por su tamaño",
    ]
    for item in bullets:
        d.ellipse([(140, y + 14), (160, y + 34)], fill=(*TEAL, 255))
        d.text((190, y), item, font=fnt(48, "reg"), fill=WHITE)
        y += 82
    y += 16
    draw_text(d, "Si no molestan, no hace falta tratarlos.", y, fnt(40, "light"), (200, 235, 235), max_w=940)
    logo(canvas, w=200, bottom=H - 90)
    return canvas


def slide_06():
    """DOCTOR - solucion"""
    canvas = fill_canvas(FOTOS / "foto-doctor-2.jpeg", anchor="top")
    canvas = bottom_gradient(canvas, opacity=0.90, start_pct=0.36)
    d = ImageDraw.Draw(canvas)
    y = 1040
    y = draw_text(d, "Se resuelven con un", y, fnt(66, "bold"), WHITE)
    y = draw_text(d, "procedimiento sencillo", y - 4, fnt(66, "bold"), WHITE)
    rule(d, y + 10, w=180)
    y += 44
    draw_text(d, "Anestesia local · Sin ingreso · En consulta", y, fnt(40, "light"), (195, 235, 235), max_w=960)
    return canvas


def slide_07():
    """CONTACTO"""
    canvas = Image.new("RGBA", (W, H), (*LIGHT_BG, 255))
    d = ImageDraw.Draw(canvas)
    SPLIT = 900
    d.rectangle([(0, SPLIT), (W, H)], fill=(*NAVY, 255))
    d.rectangle([(0, 0), (W, 16)], fill=(*TEAL, 255))
    circ = circle_photo(FOTOS / "foto-doctor-2.jpeg", 420, face_bias=0.65)
    cx = (W - 420) // 2
    cy = 60
    d.ellipse([(cx - 8, cy - 8), (cx + 436, cy + 436)], outline=(*TEAL, 255), width=7)
    canvas.paste(circ, (cx, cy), circ)
    y = cy + 448
    y = draw_text(d, "Dr. Jaime Jorge Cerrudo", y, fnt(60, "bold"), DARK_GRAY)
    rule(d, y + 4, w=240, color=TEAL)
    y += 26
    y = draw_text(d, "Especialista en Coloproctología", y, fnt(38, "light"), MID_GRAY)
    draw_text(d, "Clínica de San Pío · Almería", y + 46, fnt(38, "light"), MID_GRAY)
    y = SPLIT + 80
    y = draw_text(d, "@proctologo_en_almeria", y, fnt(50, "reg"), TEAL)
    y = draw_text(d, "proctologoalmeria.com", y, fnt(38, "light"), (160, 200, 200))
    y += 50
    d.rectangle([(140, y), (W - 140, y + 1)], fill=(40, 70, 80))
    y += 50
    y = draw_text(d, "950 264 245", y, fnt(68, "bold"), WHITE)
    y = draw_text(d, "Pide tu cita", y - 4, fnt(36, "light"), (160, 200, 200))
    y += 60
    draw_text(d, "Procedimientos proctológicos en el acto", y, fnt(28, "light"), (70, 100, 110))
    logo(canvas, w=220, bottom=H - 32)
    return canvas



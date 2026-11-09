"""Chuyen box (co the bi xoay) tu CVAT for images 1.1 XML sang YOLO detection.

Mac dinh: box xoay -> box thang bao elip noi tiep cua box xoay ("ellipse").
--corners: box thang bao tron 4 goc (rong hon nhieu khi goc xoay lon).
Box khong xoay giu nguyen. Cat theo bien anh. Khong them/bot/doi lop box nao.

Dung: python tools/cvat_xml_to_yolo.py [--corners] annotations.xml OUT_DIR [IMAGES_DIR PREVIEW_DIR]
"""
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

CLASSES = {"car": 0, "truck": 1, "bus": 2, "van": 3}


METHOD = "ellipse"


def aabb(xtl, ytl, xbr, ybr, deg):
    if METHOD == "ellipse":
        cx, cy = (xtl + xbr) / 2, (ytl + ybr) / 2
        a, b = (xbr - xtl) / 2, (ybr - ytl) / 2
        t = math.radians(deg)
        ex = math.hypot(a * math.cos(t), b * math.sin(t))
        ey = math.hypot(a * math.sin(t), b * math.cos(t))
        return cx - ex, cy - ey, cx + ex, cy + ey
    cx, cy = (xtl + xbr) / 2, (ytl + ybr) / 2
    hw, hh = (xbr - xtl) / 2, (ybr - ytl) / 2
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    xs, ys = [], []
    for dx, dy in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)):
        xs.append(cx + dx * c - dy * s)
        ys.append(cy + dx * s + dy * c)
    return min(xs), min(ys), max(xs), max(ys)


def main():
    global METHOD
    if "--corners" in sys.argv:
        METHOD = "corners"
        sys.argv.remove("--corners")
    xml_path, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    img_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    prev_dir = Path(sys.argv[4]) if len(sys.argv) > 4 else None
    out_dir.mkdir(parents=True, exist_ok=True)
    if prev_dir:
        from PIL import Image, ImageDraw
        prev_dir.mkdir(parents=True, exist_ok=True)

    root = ET.parse(xml_path).getroot()
    total = rotated = 0
    for img in root.iter("image"):
        name = Path(img.get("name")).stem
        W, H = float(img.get("width")), float(img.get("height"))
        lines, draw_items, n_rot = [], [], 0
        for box in img.iter("box"):
            label = box.get("label")
            if label not in CLASSES:
                print(f"!! {name}: lop la '{label}', bo qua")
                continue
            xtl, ytl, xbr, ybr = (float(box.get(k)) for k in ("xtl", "ytl", "xbr", "ybr"))
            deg = float(box.get("rotation", 0) or 0)
            if abs(deg % 360) > 1e-6:
                n_rot += 1
                x1, y1, x2, y2 = aabb(xtl, ytl, xbr, ybr, deg)
            else:
                x1, y1, x2, y2 = xtl, ytl, xbr, ybr
            x1, x2 = max(0.0, x1), min(W, x2)
            y1, y2 = max(0.0, y1), min(H, y2)
            if x2 - x1 <= 1 or y2 - y1 <= 1:
                print(f"!! {name}: box {label} nam ngoai anh, bo qua")
                continue
            lines.append(
                f"{CLASSES[label]} {(x1 + x2) / 2 / W:.6f} {(y1 + y2) / 2 / H:.6f} "
                f"{(x2 - x1) / W:.6f} {(y2 - y1) / H:.6f}"
            )
            draw_items.append((label, (x1, y1, x2, y2)))
        (out_dir / f"{name}.txt").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        total += len(lines)
        rotated += n_rot
        if n_rot:
            print(f"{name}: {len(lines)} box, {n_rot} box xoay da chuyen")
        if prev_dir and img_dir and draw_items:
            src = next(img_dir.glob(name + ".*"), None)
            if src:
                im = Image.open(src).convert("RGB")
                d = ImageDraw.Draw(im)
                colors = {"car": "lime", "truck": "orange", "bus": "red", "van": "cyan"}
                for label, b in draw_items:
                    d.rectangle(b, outline=colors[label], width=2)
                    d.text((b[0] + 2, b[1] + 1), label, fill=colors[label])
                im.save(prev_dir / f"{name}.jpg")
    print(f"Tong: {total} box, {rotated} box xoay da chuyen, {len(list(out_dir.glob('*.txt')))} file")


if __name__ == "__main__":
    main()

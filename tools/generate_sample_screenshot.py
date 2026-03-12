from pathlib import Path
import sqlite3
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
DB = BASE / 'db' / 'project_demo.db'
OUT = BASE / 'static' / 'checkpoint-query-screenshot.png'

WIDTH = 1600
HEIGHT = 1200
BG = '#eef2ff'
CARD = '#ffffff'
TEXT = '#111827'
MUTED = '#475569'
ACCENT = '#2563eb'
ACCENT_SOFT = '#dbeafe'
LINE = '#dbe4f0'


def get_font(size, bold=False):
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf',
    ]
    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rounded_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT r.robot_name, t.team_name, tm.manager_name, sa.sa_name, sa.classification,
               p.part_name, p.part_category, cp.quantity,
               CASE
                   WHEN p.part_category = 'Structural' THEN COALESCE(st.material || ' / ' || st.structure_type, 'Structural component')
                   WHEN p.part_category = 'Electronic' THEN 'Battery / ' || b.capacity_mah || ' mAh'
                   WHEN w.part_id IS NOT NULL THEN 'Wheel / ' || w.wheel_type || ' / radius ' || w.radius
                   WHEN mtr.part_id IS NOT NULL THEN 'Motor / torque ' || mtr.torque
                   WHEN sus.part_id IS NOT NULL THEN 'Suspension / limit ' || sus.weight_limit
                   ELSE 'Component details unavailable'
               END AS part_detail
        FROM Robot r
        JOIN Team t ON t.robot_id = r.robot_id
        LEFT JOIN TeamManager tm ON tm.team_id = t.team_id
        JOIN SubAssembly sa ON sa.robot_id = r.robot_id
        JOIN ContainsPart cp ON cp.subassembly_id = sa.subassembly_id
        JOIN Part p ON p.part_id = cp.part_id
        LEFT JOIN Structural st ON st.part_id = p.part_id
        LEFT JOIN Battery b ON b.part_id = p.part_id
        LEFT JOIN Wheel w ON w.part_id = p.part_id
        LEFT JOIN Motor mtr ON mtr.part_id = p.part_id
        LEFT JOIN Suspension sus ON sus.part_id = p.part_id
        WHERE r.robot_id = 1
        ORDER BY sa.sa_name, p.part_name
        """
    ).fetchall()
    conn.close()

    img = Image.new('RGB', (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    font_title = get_font(42, True)
    font_h2 = get_font(28, True)
    font_body = get_font(18, False)
    font_small = get_font(16, False)
    font_small_bold = get_font(16, True)
    font_table_head = get_font(15, True)
    font_table = get_font(14, False)

    # hero
    rounded_rect(draw, (40, 35, 1560, 220), 22, CARD, outline='#d1d9e6')
    draw.text((70, 62), 'CMPT 354 Checkpoint Demo', fill=ACCENT, font=font_small_bold)
    draw.text((70, 92), 'Robot Parts and Team Management Platform', fill=TEXT, font=font_title)
    draw.text((70, 148), 'A minimal frontend GUI for browsing robots, their sub-assemblies, parts, and the team responsible for each robot.', fill=MUTED, font=font_body)
    rounded_rect(draw, (1240, 70, 1490, 110), 20, ACCENT_SOFT)
    rounded_rect(draw, (1240, 122, 1490, 162), 20, ACCENT_SOFT)
    draw.text((1282, 82), 'SQLite demo backend', fill=ACCENT, font=font_small_bold)
    draw.text((1260, 134), 'Python standard library server', fill=ACCENT, font=font_small_bold)

    # search card
    rounded_rect(draw, (40, 250, 1560, 420), 22, CARD, outline='#d1d9e6')
    draw.text((70, 280), 'Run a Meaningful Query', fill=TEXT, font=font_h2)
    draw.text((70, 320), 'Selected filters for screenshot', fill=MUTED, font=font_body)
    rounded_rect(draw, (70, 350, 440, 392), 12, '#f8fafc', outline=LINE)
    rounded_rect(draw, (470, 350, 790, 392), 12, '#f8fafc', outline=LINE)
    rounded_rect(draw, (820, 350, 980, 392), 12, ACCENT)
    draw.text((90, 362), 'Robot: Atlas Rover', fill=TEXT, font=font_small_bold)
    draw.text((490, 362), 'Part category: All', fill=TEXT, font=font_small_bold)
    draw.text((867, 361), 'Search', fill='white', font=font_small_bold)

    # results card
    rounded_rect(draw, (40, 450, 1560, 1160), 22, CARD, outline='#d1d9e6')
    draw.text((70, 480), 'Meaningful Query Result', fill=TEXT, font=font_h2)
    draw.text((70, 520), 'Showing the component structure for Atlas Rover.', fill=MUTED, font=font_body)

    # table
    headers = ['Robot', 'Team', 'Manager', 'Sub-Assembly', 'Class', 'Part', 'Category', 'Qty', 'Detail']
    col_widths = [120, 145, 135, 170, 80, 200, 95, 55, 380]
    start_x = 70
    start_y = 565
    row_h = 34

    x = start_x
    for h, w in zip(headers, col_widths):
        rounded_rect(draw, (x, start_y, x + w, start_y + row_h), 0, '#eff6ff', outline=LINE)
        draw.text((x + 8, start_y + 8), h, fill='#1e3a8a', font=font_table_head)
        x += w

    for idx, row in enumerate(rows[:12]):
        y = start_y + row_h + idx * row_h
        values = [
            row['robot_name'], row['team_name'], row['manager_name'], row['sa_name'], row['classification'],
            row['part_name'], row['part_category'], str(row['quantity']), row['part_detail']
        ]
        x = start_x
        for value, w in zip(values, col_widths):
            draw.rectangle((x, y, x + w, y + row_h), fill='white', outline=LINE)
            text = str(value)
            if len(text) > 34 and w < 200:
                text = text[:31] + '...'
            elif len(text) > 54 and w >= 200:
                text = text[:51] + '...'
            draw.text((x + 8, y + 9), text, fill=TEXT, font=font_table)
            x += w

    note_y = 1010
    rounded_rect(draw, (70, note_y, 1530, 1125), 14, '#f8fafc', outline=LINE)
    draw.text((92, note_y + 18), 'Query shown in this screen:', fill=TEXT, font=font_small_bold)
    draw.text((92, note_y + 48), 'retrieve all sub-assemblies and related parts for a selected robot, together with the responsible team and manager.', fill=MUTED, font=font_small)
    draw.text((92, note_y + 78), 'SELECT Robot, Team, Manager, SubAssembly, Part, Category, Quantity FROM Robot JOIN Team JOIN TeamManager JOIN SubAssembly JOIN ContainsPart JOIN Part ...', fill='#334155', font=font_small)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(f'Saved {OUT}')


if __name__ == '__main__':
    main()

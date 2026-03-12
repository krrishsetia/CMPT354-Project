from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import sqlite3
import html
import os

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'db' / 'project_demo.db'
SCHEMA_PATH = BASE_DIR / 'db' / 'schema_sqlite.sql'
SEED_PATH = BASE_DIR / 'db' / 'seed_sqlite.sql'
STYLE_PATH = BASE_DIR / 'static' / 'style.css'
HOST = '127.0.0.1'
PORT = int(os.environ.get('PORT', '8000'))


def ensure_db():
    if DB_PATH.exists():
        return
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    with open(SEED_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_robots():
    conn = get_connection()
    rows = conn.execute('SELECT robot_id, robot_name FROM Robot ORDER BY robot_name').fetchall()
    conn.close()
    return rows


def build_results(robot_id, part_category):
    conn = get_connection()
    sql = """
        SELECT
            r.robot_name,
            t.team_name,
            tm.manager_name,
            sa.sa_name,
            sa.classification,
            p.part_name,
            p.part_category,
            cp.quantity,
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
        WHERE r.robot_id = ?
    """
    params = [robot_id]
    if part_category and part_category != 'All':
        sql += ' AND p.part_category = ? '
        params.append(part_category)
    sql += ' ORDER BY sa.sa_name, p.part_name;'
    rows = conn.execute(sql, params).fetchall()
    robot_name_row = conn.execute('SELECT robot_name FROM Robot WHERE robot_id = ?', (robot_id,)).fetchone()
    conn.close()
    return rows, (robot_name_row['robot_name'] if robot_name_row else 'Unknown Robot')


def page_template(content, title='CMPT 354 Robot Parts Platform'):
    style = STYLE_PATH.read_text(encoding='utf-8') if STYLE_PATH.exists() else ''
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{html.escape(title)}</title>
  <style>{style}</style>
</head>
<body>
  <div class=\"page-shell\">{content}</div>
</body>
</html>"""


def render_home(selected_robot=None, selected_category='All', results=None, robot_name=None):
    robots = fetch_robots()
    options = ['<option value="">Select a robot</option>']
    for robot in robots:
        selected = ' selected' if selected_robot and str(robot['robot_id']) == str(selected_robot) else ''
        options.append(f'<option value="{robot["robot_id"]}"{selected}>{html.escape(robot["robot_name"])}</option>')

    categories = ['All', 'Structural', 'Electronic', 'Mechanical']
    category_options = []
    for category in categories:
        selected = ' selected' if category == selected_category else ''
        category_options.append(f'<option value="{category}"{selected}>{html.escape(category)}</option>')

    results_block = ''
    if results is not None:
        if results:
            body_rows = []
            for row in results:
                body_rows.append(
                    '<tr>'
                    f'<td>{html.escape(row["robot_name"])}</td>'
                    f'<td>{html.escape(row["team_name"] or "-")}</td>'
                    f'<td>{html.escape(row["manager_name"] or "-")}</td>'
                    f'<td>{html.escape(row["sa_name"])}</td>'
                    f'<td>{html.escape(row["classification"] or "-")}</td>'
                    f'<td>{html.escape(row["part_name"])}</td>'
                    f'<td>{html.escape(row["part_category"])}</td>'
                    f'<td>{html.escape(str(row["quantity"]))}</td>'
                    f'<td>{html.escape(row["part_detail"] or "-")}</td>'
                    '</tr>'
                )
            body_html = ''.join(body_rows)
            query_preview = html.escape(
                'SELECT Robot, Team, Manager, SubAssembly, Part, Category, Quantity '\
                'FROM Robot JOIN Team JOIN TeamManager JOIN SubAssembly JOIN ContainsPart JOIN Part ...'
            )
            results_block = f"""
            <section class=\"results-card\">
              <div class=\"section-heading\">
                <h2>Meaningful Query Result</h2>
                <p>Showing the component structure for <strong>{html.escape(robot_name or '')}</strong>.</p>
              </div>
              <div class=\"table-wrap\">
                <table>
                  <thead>
                    <tr>
                      <th>Robot</th>
                      <th>Team</th>
                      <th>Manager</th>
                      <th>Sub-Assembly</th>
                      <th>Class</th>
                      <th>Part</th>
                      <th>Category</th>
                      <th>Qty</th>
                      <th>Detail</th>
                    </tr>
                  </thead>
                  <tbody>{body_html}</tbody>
                </table>
              </div>
              <div class=\"query-note\">
                <p><strong>Query shown in this screen:</strong> retrieve all sub-assemblies and related parts for a selected robot, together with the responsible team and manager.</p>
                <pre>{query_preview}</pre>
              </div>
            </section>
            """
        else:
            results_block = """
            <section class=\"results-card\">
              <h2>Meaningful Query Result</h2>
              <p>No rows matched the current filter. Try changing the robot or part category.</p>
            </section>
            """

    content = f"""
    <header class=\"hero\">
      <div>
        <p class=\"eyebrow\">CMPT 354 Checkpoint Demo</p>
        <h1>Robot Parts and Team Management Platform</h1>
        <p class=\"lead\">A minimal frontend GUI for browsing robots, their sub-assemblies, parts, and the team responsible for each robot.</p>
      </div>
      <div class=\"hero-meta\">
        <span>SQLite demo backend</span>
        <span>Python standard library server</span>
      </div>
    </header>

    <section class=\"search-card\">
      <div class=\"section-heading\">
        <h2>Run a Meaningful Query</h2>
        <p>Select a robot and optionally filter by part category.</p>
      </div>
      <form method=\"GET\" action=\"/search\" class=\"query-form\">
        <label>
          <span>Robot</span>
          <select name=\"robot_id\" required>
            {''.join(options)}
          </select>
        </label>
        <label>
          <span>Part category</span>
          <select name=\"part_category\">{''.join(category_options)}</select>
        </label>
        <button type=\"submit\">Search</button>
      </form>
    </section>

    {results_block}
    """
    return page_template(content)


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/':
            self.respond_html(render_home())
            return
        if parsed.path == '/search':
            qs = parse_qs(parsed.query)
            robot_id = qs.get('robot_id', [''])[0]
            part_category = qs.get('part_category', ['All'])[0]
            if not robot_id.isdigit():
                self.respond_html(render_home(results=[]), status=400)
                return
            results, robot_name = build_results(int(robot_id), part_category)
            self.respond_html(render_home(selected_robot=robot_id, selected_category=part_category, results=results, robot_name=robot_name))
            return
        self.send_error(404, 'Not found')

    def log_message(self, format, *args):
        return

    def respond_html(self, body, status=200):
        encoded = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def run_server():
    ensure_db()
    server = HTTPServer((HOST, PORT), AppHandler)
    print(f'Server running at http://{HOST}:{PORT}')
    server.serve_forever()


if __name__ == '__main__':
    run_server()

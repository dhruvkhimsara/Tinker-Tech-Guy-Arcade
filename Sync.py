import os
import urllib.parse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_DIR = os.path.join(SCRIPT_DIR, 'Games')
INDEX_FILE = os.path.join(SCRIPT_DIR, 'index.html')

def clean_name(filename):
    name, _ = os.path.splitext(filename)
    name = urllib.parse.unquote(name)
    return name

def build_index():
    if not os.path.exists(GAMES_DIR):
        os.makedirs(GAMES_DIR)
        
    files = [f for f in os.listdir(GAMES_DIR) if f.lower().endswith('.html') or f.lower().endswith('.htm')]
    files.sort()

    directory_items = []
    for f in files:
        display_name = clean_name(f)
        item_html = f'                <div class="log-item">{display_name}</div>'
        directory_items.append(item_html)

    all_items_string = "\n".join(directory_items)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workspace Core</title>
    <style>
        :root {{
            --bg: #f8fafc;
            --panel: #ffffff;
            --border: #e2e8f0;
            --text: #334155;
            --text-light: #64748b;
            --accent: #0f172a;
        }}

        body, html {{
            margin: 0; padding: 0; width: 100vw; height: 100vh;
            background-color: var(--bg); color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            overflow: hidden;
        }}

        * {{ box-sizing: border-box; }}

        #dashboard-view {{
            display: flex; flex-direction: column; width: 100%; height: 100%;
            padding: 20px; overflow-y: auto;
        }}

        .launcher-panel {{
            background-color: var(--panel); border: 1px solid var(--border);
            border-radius: 8px; padding: 25px; width: 100%;
            max-width: 600px; margin: 0 auto 30px auto;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05); flex-shrink: 0;
        }}

        .launcher-panel h2 {{ margin: 0 0 5px 0; font-size: 1.1rem; color: var(--accent); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .launcher-panel p {{ color: var(--text-light); font-size: 0.85rem; margin: 0 0 15px 0; }}
        .input-group {{ display: flex; flex-direction: column; gap: 10px; width: 100%; }}

        @media (min-width: 480px) {{
            .input-group {{ flex-direction: row; }}
        }}

        input {{
            flex: 1; background: #fff; color: #000; border: 1px solid var(--border);
            padding: 10px 14px; border-radius: 6px; font-size: 0.9rem; outline: none; width: 100%;
        }}
        input:focus {{ border-color: #94a3b8; }}

        .btn {{
            background: var(--accent); color: #fff; padding: 10px 24px; border-radius: 6px;
            font-weight: 600; font-size: 0.9rem; cursor: pointer; user-select: none;
            text-align: center; white-space: nowrap; transition: background 0.1s;
        }}
        .btn:hover {{ background: #1e293b; }}

        .directory-container {{ width: 100%; max-width: 1000px; margin: 0 auto; }}
        .directory-header {{
            font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;
            color: var(--text-light); margin-bottom: 15px; border-bottom: 1px solid var(--border);
            padding-bottom: 5px; font-weight: 700;
        }}
        .directory-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 10px; }}

        .log-item {{
            background-color: var(--panel); border: 1px solid var(--border);
            padding: 12px; border-radius: 6px; color: var(--text); font-size: 0.85rem;
            user-select: text; white-space: normal; word-wrap: break-word; height: auto;
        }}

        #game-screen {{ display: none; position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #000; z-index: 9998; }}
        iframe {{ width: 100%; height: 100%; border: none; display: block; }}

        #exit-btn {{
            position: absolute; top: 0; left: 50%; transform: translateX(-50%);
            background-color: rgba(255, 255, 255, 0.1); border: none;
            color: rgba(255, 255, 255, 0.2); padding: 4px 20px;
            border-radius: 0 0 4px 4px; font-size: 0.6rem; cursor: pointer;
            z-index: 9999; transition: all 0.2s ease;
        }}
        #exit-btn:hover {{
            background-color: #ef4444; color: #fff;
        }}
    </style>
</head>
<body>

    <div id="dashboard-view">
        <div class="launcher-panel">
            <h2>Workspace Router</h2>
            <p>Enter target asset name to open the file instance:</p>
            <div class="input-group">
                <input type="text" id="game-input" placeholder="Search asset..." onkeydown="if(event.key==='Enter') launchFromInput()">
                <div class="btn" onclick="launchFromInput()">GO</div>
            </div>
        </div>

        <div class="directory-container">
            <div class="directory-header">Assets</div>
            <div class="directory-grid">
{all_items_string}
            </div>
        </div>
    </div>

    <div id="game-screen">
        <button id="exit-btn" onclick="exitGame()">-</button>
        <iframe id="game-frame" src=""></iframe>
    </div>

    <script>
        const gameFrame = document.getElementById('game-frame');
        const dashboardView = document.getElementById('dashboard-view');
        const gameScreen = document.getElementById('game-screen');
        const gameInput = document.getElementById('game-input');

        const urlParams = new URLSearchParams(window.location.search);
        const gameParam = urlParams.get('index');
        
        if (gameParam) {{
            loadGame(gameParam);
        }}

        function launchFromInput() {{
            const gameName = gameInput.value.trim();
            if (gameName) loadGame(gameName);
        }}

        function loadGame(filename) {{
            let targetFile = filename;
            if (!targetFile.toLowerCase().endswith('.html') && !targetFile.toLowerCase().endswith('.htm')) {{
                targetFile += '.html';
            }}
            gameFrame.src = "Games/" + targetFile + "?t=" + new Date().getTime();
            dashboardView.style.display = 'none';
            gameScreen.style.display = 'block';
            setTimeout(() => gameFrame.focus(), 100);
        }}

        function exitGame() {{
            gameFrame.src = "";
            gameScreen.style.display = 'none';
            dashboardView.style.display = 'flex';
            gameInput.value = "";
            if (window.location.search) {{
                window.history.replaceState({{}}, document.title, window.location.pathname);
            }}
        }}
    </script>
</body>
</html>
"""

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Clean workspace index built successfully.")

if __name__ == '__main__':
    build_index()

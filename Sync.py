import os
import urllib.parse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_DIR = os.path.join(SCRIPT_DIR, 'Games')
INDEX_FILE = os.path.join(SCRIPT_DIR, 'index.html')

def clean_name(filename):
    # Strip extension
    name, _ = os.path.splitext(filename)
    # Decode URL-encoded characters (like %20 to spaces)
    name = urllib.parse.unquote(name)
    return name

def build_index():
    # Fallback if folder doesn't exist yet
    if not os.path.exists(GAMES_DIR):
        os.makedirs(GAMES_DIR)
        
    # Gather all HTML game files
    files = [f for f in os.listdir(GAMES_DIR) if f.lower().endswith('.html') or f.lower().endswith('.htm')]
    files.sort()

    # Generate the text directory entries
    directory_items = []
    for f in files:
        display_name = clean_name(f)
        item_html = f'                <div class="directory-item">{display_name}</div>'
        directory_items.append(item_html)

    all_items_string = "\n".join(directory_items)

    # Core HTML Template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML Runner</title>
    <style>
        :root {{
            --bg-dark: #09090b;
            --panel-dark: #141416;
            --border-color: #27272a;
            --text-main: #ffffff;
            --text-muted: #a1a1aa;
            --accent-red: #ef4444;
        }}

        body, html {{
            margin: 0; padding: 0; width: 100vw; height: 100vh;
            background-color: var(--bg-dark); color: var(--text-main);
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            overflow: hidden;
        }}

        * {{ box-sizing: border-box; }}

        #dashboard-view {{
            display: flex; flex-direction: column; width: 100%; height: 100%;
            padding: clamp(15px, 4vw, 40px); overflow-y: auto;
        }}

        .launcher-panel {{
            background-color: var(--panel-dark); border: 1px solid var(--border-color);
            border-radius: 16px; padding: clamp(20px, 3vw, 35px); width: 100%;
            max-width: 600px; margin: 0 auto clamp(20px, 4vw, 40px) auto;
            text-align: center; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); flex-shrink: 0;
        }}

        .launcher-panel h2 {{ margin: 0 0 10px 0; font-size: clamp(1.4rem, 2.5vw, 2rem); letter-spacing: 1px; font-weight: 800; }}
        .launcher-panel p {{ color: var(--text-muted); font-size: clamp(0.85rem, 1.5vw, 0.95rem); margin: 0 0 20px 0; }}
        .input-group {{ display: flex; flex-direction: column; gap: 12px; width: 100%; }}

        @media (min-width: 480px) {{
            .input-group {{ flex-direction: row; gap: 10px; }}
        }}

        input {{
            flex: 1; background: #000; color: #fff; border: 1px solid var(--border-color);
            padding: 14px 18px; border-radius: 8px; font-size: 1rem; outline: none; width: 100%;
            transition: border-color 0.2s;
        }}
        input:focus {{ border-color: var(--text-muted); }}

        .btn {{
            background: #fff; color: #000; padding: 14px 30px; border-radius: 8px;
            font-weight: bold; font-size: 1rem; cursor: pointer; user-select: none;
            transition: background 0.2s; white-space: nowrap;
        }}
        .btn:hover {{ background: #e4e4e7; }}

        .directory-container {{ width: 100%; max-width: 1000px; margin: 0 auto; }}
        .directory-header {{
            font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px;
            color: var(--text-muted); margin-bottom: 15px; border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px; font-weight: 700;
        }}
        .directory-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }}

        .directory-item {{
            background-color: rgba(20, 20, 22, 0.4); border: 1px dashed var(--border-color);
            padding: 14px 16px; border-radius: 8px; color: #e4e4e7; font-size: 0.95rem;
            font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; user-select: text;
        }}

        #game-screen {{ display: none; position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #000; z-index: 9998; }}
        iframe {{ width: 100%; height: 100%; border: none; display: block; }}

        #exit-btn {{
            position: absolute; top: 0; left: 50%; transform: translateX(-50%);
            background-color: rgba(20, 20, 22, 0.75); border: 1px solid var(--border-color);
            border-top: none; color: var(--text-muted); padding: 6px 24px;
            border-radius: 0 0 12px 12px; font-weight: 800; font-size: 0.7rem;
            text-transform: uppercase; letter-spacing: 2px; cursor: pointer;
            z-index: 9999; backdrop-filter: blur(6px); opacity: 0.15; transition: all 0.2s ease;
        }}
        #exit-btn:hover {{
            opacity: 1; color: var(--accent-red); border-color: var(--accent-red);
            background-color: rgba(20, 20, 22, 0.9); box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
        }}
    </style>
</head>
<body>

    <div id="dashboard-view">
        <div class="launcher-panel">
            <h2>HTML RUNNER</h2>
            <p>Type the name of a game below to launch it instantly</p>
            <div class="input-group">
                <input type="text" id="game-input" placeholder="e.g., Slope" onkeydown="if(event.key==='Enter') launchFromInput()">
                <div class="btn" onclick="launchFromInput()">LAUNCH</div>
            </div>
        </div>

        <div class="directory-container">
            <div class="directory-header">Available Games</div>
            <div class="directory-grid">
{all_items_string}
            </div>
        </div>
    </div>

    <div id="game-screen">
        <button id="exit-btn" onclick="exitGame()">EXIT</button>
        <iframe id="game-frame" src=""></iframe>
    </div>

    <script>
        const gameFrame = document.getElementById('game-frame');
        const dashboardView = document.getElementById('dashboard-view');
        const gameScreen = document.getElementById('game-screen');
        const gameInput = document.getElementById('game-input');

        const urlParams = new URLSearchParams(window.location.search);
        const gameParam = urlParams.get('game');
        
        if (gameParam) {{
            loadGame(gameParam);
        }}

        function launchFromInput() {{
            const gameName = gameInput.value.trim();
            if (gameName) loadGame(gameName);
        }}

        function loadGame(filename) {{
            let targetFile = filename;
            if (!targetFile.toLowerCase().endsWith('.html') && !targetFile.toLowerCase().endsWith('.htm')) {{
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
    print("Successfully synced and updated index.html folder map.")

if __name__ == '__main__':
    build_index()

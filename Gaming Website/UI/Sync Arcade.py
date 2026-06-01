import os

# Define the exact absolute paths relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Games'))
INDEX_FILE = os.path.join(SCRIPT_DIR, 'index.html')

def generate_arcade():
    # 1. Scan the Games directory for all valid .html game files
    if not os.path.exists(GAMES_DIR):
        print(f"Error: Could not find Games folder at {GAMES_DIR}")
        return

    game_files = [f for f in os.listdir(GAMES_DIR) if f.endswith('.html')]
    game_files.sort() # Keeps them in clean alphabetical order

    # 2. Build the dynamic HTML string cards based on current files found
    card_elements = []
    for file_name in game_files:
        # Strip the extension out to create a clean visual title string
        display_title = os.path.splitext(file_name)[0]
        relative_path = f"../Games/{file_name}"
        
        card_html = f"""            <div class="game-card" onclick="launchGame('{relative_path}')">
                <div class="game-title">{display_title}</div>
            </div>"""
        card_elements.append(card_html)

    all_cards_string = "\n\n".join(card_elements)

    # 3. Construct the completely clean index.html file layout
    full_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gaming Website</title>
    <style>
        :root {{
            --bg-dark: #09090b;
            --panel-dark: #141416;
            --accent-green: #00ff88;
            --text-main: #ffffff;
            --text-muted: #a1a1aa;
            --border-color: #27272a;
        }}

        body {{
            margin: 0;
            padding: 0;
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }}

        header {{
            background-color: var(--panel-dark);
            border-bottom: 1px solid var(--border-color);
            padding: 0 30px;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
            z-index: 100;
        }}

        .logo {{
            font-size: 1.3rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--text-main);
            user-select: none;
            cursor: pointer;
        }}

        .logo span {{
            color: var(--accent-green);
        }}

        .nav-btn {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .nav-btn:hover {{
            color: var(--text-main);
            border-color: var(--accent-green);
            background-color: rgba(0, 255, 136, 0.05);
        }}

        #content-area {{
            flex: 1;
            display: flex;
            overflow: hidden;
            position: relative;
        }}

        #browse-view {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            padding: 40px;
            width: 100%;
            box-sizing: border-box;
            overflow-y: auto;
            align-content: start;
        }}

        .game-card {{
            background-color: var(--panel-dark);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            aspect-ratio: 16 / 10;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;    
            padding: 20px;
            box-sizing: border-box;
            background: radial-gradient(circle at 50% 50%, #18181b, #09090b);
        }}

        .game-card:hover {{
            transform: translateY(-4px);
            border-color: var(--accent-green);
            box-shadow: 0 12px 30px rgba(0, 255, 136, 0.1);
        }}

        .game-title {{
            font-size: 1.2rem;
            font-weight: 700;
            position: relative;
            z-index: 2;
            letter-spacing: 0.5px;
            text-align: center;
        }}

        #play-view {{
            display: none;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: #000000;
            box-sizing: border-box;
        }}

        #game-frame-wrapper {{
            width: 1920px;
            height: 1080px;
            min-width: 1920px;
            min-height: 1080px;
            margin: 0 auto;
            position: relative;
            background-color: #050505;
        }}

        iframe {{
            width: 100%;
            height: 100%;
            border: none;
            display: block;
        }}
    </style>
</head>
<body>

    <header>
        <div class="logo" onclick="showBrowseView()">Tinker Tech Guy's <span>Arcade</span></div>
        <button class="nav-btn" id="back-home-btn" style="display: none;" onclick="showBrowseView()">← Back to Games</button>
    </header>

    <div id="content-area">
        
        <div id="browse-view">
{all_cards_string}
        </div>

        <div id="play-view">
            <div id="game-frame-wrapper">
                <iframe id="arcade-processor" src=""></iframe>
            </div>
        </div>

    </div>

    <script>
        const browseView = document.getElementById('browse-view');
        const playView = document.getElementById('play-view');
        const backBtn = document.getElementById('back-home-btn');
        const iframe = document.getElementById('arcade-processor');

        function launchGame(gameFilePath) {{
            iframe.src = gameFilePath;
            browseView.style.display = 'none';
            playView.style.display = 'block';
            backBtn.style.display = 'block';
        }}

        function showBrowseView() {{
            iframe.src = "";
            playView.style.display = 'none';
            backBtn.style.display = 'none';
            browseView.style.display = 'grid';
        }}
    </script>

</body>
</html>
"""

    # 4. Write out the final built HTML string
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html_content)
    
    print(f"Arcade sync successful! Found {len(game_files)} games inside 'Gaming Website/Games'. index.html updated.")

if __name__ == '__main__':
    generate_arcade()
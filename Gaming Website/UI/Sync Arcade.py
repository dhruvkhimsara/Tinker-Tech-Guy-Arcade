import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAMES_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'Games'))
INDEX_FILE = os.path.join(SCRIPT_DIR, 'index.html')

def generate_arcade():
    if not os.path.exists(GAMES_DIR):
        print(f"Error: Could not find Games folder at {GAMES_DIR}")
        return

    game_files = [f for f in os.listdir(GAMES_DIR) if f.endswith('.html')]
    game_files.sort()

    card_elements = []
    for file_name in game_files:
        display_title = os.path.splitext(file_name)[0]
        relative_path = f"Games/{file_name}"
        
        card_html = f"""            <div class="game-card" onclick="launchGame('{relative_path}')">
                <div class="game-title">{display_title}</div>
                <button class="btn-launch">Launch Engine</button>
            </div>"""
        card_elements.append(card_html)

    all_cards_string = "\n\n".join(card_elements)

    full_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    
    <title>Tinker Tech Guy's Arcade</title>
    <style>
        :root {{
            --bg-dark: #050505;
            --panel-dark: #141416;
            --accent-green: #00ff88;
            --text-main: #ffffff;
            --text-muted: #a1a1aa;
            --border-color: #27272a;
        }}

        * {{
            box-sizing: border-box;
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
            user-select: none;
        }}

        /* --- DASHBOARD WRAPPER --- */
        #dashboard-container {{
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
            background: radial-gradient(circle at center, #111114 0%, var(--bg-dark) 100%);
        }}

        header {{
            background-color: var(--panel-dark);
            border-bottom: 1px solid var(--border-color);
            padding: 0 30px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;        
            flex-shrink: 0;
            z-index: 100;
        }}

        .logo {{
            font-size: 1.6rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: var(--text-main);
        }}

        .logo span {{
            color: var(--accent-green);
        }}

        #browse-view {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px;
            padding: 50px;
            width: 100%;
            max-width: 1600px;
            margin: 0 auto;
            overflow-y: auto;
            align-content: start;
        }}

        .game-card {{
            background-color: var(--panel-dark);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            aspect-ratio: 16 / 10;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;    
            padding: 30px;
            gap: 15px;
        }}

        .game-card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-green);
            background-color: rgba(0, 255, 136, 0.02);
            box-shadow: 0 12px 30px rgba(0, 255, 136, 0.1);
        }}

        .game-title {{
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: 1px;
            text-align: center;
        }}

        .btn-launch {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--accent-green);
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .game-card:hover .btn-launch {{
            background-color: rgba(0, 255, 136, 0.1);
            border-color: var(--accent-green);
        }}

        /* --- FULL VIEWPORT GAME VIEW --- */
        #play-view {{
            display: none;
            position: fixed;
            top: 0; 
            left: 0; 
            width: 100vw; 
            height: 100vh;
            background-color: #000000;
            z-index: 500;
        }}

        iframe {{
            width: 100%;
            height: 100%;
            border: none;
            margin: 0;
            padding: 0;
            display: block;
        }}

        /* Top-Center Stealth Dropdown Menu Button */
        #floating-escape-btn {{
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            background-color: rgba(20, 20, 22, 0.75);
            border: 1px solid var(--border-color);
            border-top: none;
            color: var(--text-muted);
            padding: 6px 24px;
            border-radius: 0 0 12px 12px;
            font-weight: 800;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            z-index: 600;
            backdrop-filter: blur(6px);
            transition: all 0.2s ease;
            opacity: 0.15; /* Highly transparent during active gameplay */
        }}

        #floating-escape-btn:hover {{
            opacity: 1;
            color: var(--accent-green);
            border-color: var(--accent-green);
            background-color: var(--panel-dark);
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.15);
            padding-bottom: 10px; /* Slight expansion animation on hover */
        }}

        /* --- ESCAPE MENU MODAL OVERLAY --- */
        #pause-overlay {{
            display: none; 
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(5, 5, 5, 0.95);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(8px);
        }}

        .pause-box {{
            background-color: var(--panel-dark);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 45px;
            text-align: center;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.8);
        }}

        .pause-box h1 {{
            margin: 0 0 10px 0;
            color: #ffffff;
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: 2px;
        }}

        .pause-box p {{
            color: var(--text-muted);
            margin: 0 0 30px 0;
            font-weight: 600;
            font-size: 1rem;
        }}

        .pause-btns {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .btn-menu {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 14px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .btn-menu:hover {{
            border-color: var(--accent-green);
            background-color: rgba(0, 255, 136, 0.05);
            color: var(--accent-green);
        }}

        .btn-quit {{
            border-color: rgba(239, 68, 68, 0.3);
            color: #ef4444;
        }}

        .btn-quit:hover {{
            border-color: #ef4444;
            background-color: rgba(239, 68, 68, 0.1);
            color: #ef4444;
        }}
    </style>
</head>
<body>

    <div id="dashboard-container">
        <header>
            <div class="logo">Tinker Tech Guy's <span>Arcade</span></div>
        </header>

        <div id="browse-view">
{all_cards_string}
        </div>
    </div>

    <div id="play-view">
        <button id="floating-escape-btn" onclick="openPauseMenu()">Hub Menu</button>
        <iframe id="arcade-processor" src="" allowfullscreen="true" scrolling="no"></iframe>
    </div>

    <div id="pause-overlay">
        <div class="pause-box">
            <h1>SYSTEM PAUSED</h1>
            <p>Return to the main dashboard?</p>
            <div class="pause-btns">
                <button class="btn-menu" onclick="resumeGame()">Resume Game</button>
                <button class="btn-menu btn-quit" onclick="exitToHub()">Exit to Hub</button>
            </div>
        </div>
    </div>

    <script>
        const dashboardContainer = document.getElementById('dashboard-container');
        const playView = document.getElementById('play-view');
        const iframe = document.getElementById('arcade-processor');
        const pauseOverlay = document.getElementById('pause-overlay');

        let isGameRunning = false;

        function launchGame(gameFilePath) {{
            dashboardContainer.style.display = 'none';
            playView.style.display = 'block';
            
            iframe.src = gameFilePath + '?t=' + new Date().getTime();
            isGameRunning = true;
            
            setTimeout(() => {{
                iframe.focus();
            }}, 100);
        }}

        function openPauseMenu() {{
            if (isGameRunning) {{
                pauseOverlay.style.display = 'flex';
            }}
        }}

        function resumeGame() {{
            pauseOverlay.style.display = 'none';
            iframe.focus();
        }}

        function exitToHub() {{
            iframe.src = ""; 
            pauseOverlay.style.display = 'none';
            playView.style.display = 'none';
            dashboardContainer.style.display = 'flex';
            isGameRunning = false;
        }}

        window.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape' && isGameRunning) {{
                if (pauseOverlay.style.display === 'flex') {{
                    resumeGame();
                }} else {{
                    openPauseMenu();
                }}
            }}
        }});
    </script>

</body>
</html>
"""

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html_content)
    
    print(f"Arcade sync successful! Updated fullscreen view layout in index.html.")

if __name__ == '__main__':
    generate_arcade()
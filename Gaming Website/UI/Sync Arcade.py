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
        # Simply grab the exact filename without the .html extension
        display_title = os.path.splitext(file_name)[0]
        relative_path = f"Games/{file_name}"
        
        # Data-title is still stored in lowercase for the search engine to work smoothly
        card_html = f"""            <div class="game-card" data-title="{display_title.lower()}" onclick="launchGame('{relative_path}')">
                <div class="game-title">{display_title}</div>
                <button class="btn-launch">PLAY</button>
            </div>"""
        card_elements.append(card_html)

    all_cards_string = "\n\n".join(card_elements)

    full_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
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
            -webkit-tap-highlight-color: transparent;
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
            width: 100vw;
            overflow: hidden;
            user-select: none;
        }}

        /* --- DASHBOARD WRAPPER --- */
        #dashboard-container {{
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
            background: radial-gradient(circle at top, #111116 0%, var(--bg-dark) 100%);
            overflow-y: auto;
        }}

        /* Integrated Cool Cinematic Branding Section */
        .arcade-hero {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 60px 20px 20px 20px;
            text-align: center;
            flex-shrink: 0;
        }}

        .logo {{
            font-size: 2.8rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 6px;
            color: var(--text-main);
            margin: 0 0 25px 0;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
        }}

        .logo span {{
            color: var(--accent-green);
        }}

        /* Centered High-Tech Search Interface */
        .search-wrapper {{
            position: relative;
            width: 100%;
            max-width: 480px;
            margin: 0 auto;
        }}

        .search-bar {{
            width: 100%;
            background-color: var(--panel-dark);
            border: 1px solid var(--border-color);
            border-radius: 30px;
            padding: 14px 25px;
            color: var(--text-main);
            font-size: 1rem;
            font-weight: 600;
            outline: none;
            text-align: center;
            letter-spacing: 0.5px;
            transition: all 0.25s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}

        .search-bar:focus {{
            border-color: var(--accent-green);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.15), 0 4px 25px rgba(0, 0, 0, 0.5);
            background-color: #17171a;
        }}

        .search-bar::placeholder {{
            color: var(--text-muted);
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-size: 0.8rem;
            opacity: 0.7;
        }}

        /* Dynamic Fluid Matrix Layout */
        #browse-view {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 25px;
            padding: 30px 20px 60px 20px;
            width: 100%;
            max-width: 1550px; 
            margin: 0 auto;
            align-content: start;
        }}

        .game-card {{
            background-color: var(--panel-dark);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            cursor: pointer;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.2s, background-color 0.2s, opacity 0.25s ease, visibility 0.25s;
            width: calc(20% - 20px); 
            min-width: 260px;       
            max-width: 290px;
            min-height: 180px; /* Swapped aspect-ratio for min-height to allow text wrapping safely */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;    
            padding: 24px;
            gap: 18px;
            opacity: 1;
            visibility: visible;
        }}

        /* Instant Hide Utility for Dynamic Filter Engine */
        .game-card.hidden {{
            display: none;
            opacity: 0;
            visibility: hidden;
        }}

        .game-card:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-green);
            background-color: rgba(0, 255, 136, 0.02);
            box-shadow: 0 12px 30px rgba(0, 255, 136, 0.1);
        }}

        .game-title {{
            font-size: 1.3rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-align: center;
            width: 100%;
            white-space: normal; /* Allows text to wrap */
            overflow-wrap: break-word; /* Breaks exceptionally long words if needed */
            line-height: 1.3;
        }}

        .btn-launch {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--accent-green);
            padding: 10px 28px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.2s ease;
            cursor: pointer;
            margin-top: auto; /* Pushes the button to the bottom evenly */
        }}

        .game-card:hover .btn-launch {{
            background-color: var(--accent-green);
            border-color: var(--accent-green);
            color: #000000;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
        }}

        /* --- LIQUID RESPONSIVE VIEWER --- */
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
            opacity: 0.15;
        }}

        #floating-escape-btn:hover {{
            opacity: 1;
            color: var(--accent-green);
            border-color: var(--accent-green);
            background-color: var(--panel-dark);
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.15);
            padding-bottom: 10px;
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
        <div class="arcade-hero">
            <div class="logo">Tinker Tech Guy's <span>Arcade</span></div>
            <div class="search-wrapper">
                <input type="text" id="game-search" class="search-bar" placeholder="Search Catalog..." autocomplete="off">
            </div>
        </div>

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
        const searchBar = document.getElementById('game-search');
        const gameCards = document.querySelectorAll('.game-card');

        let isGameRunning = false;

        // --- Client-Side Search Processing Engine ---
        searchBar.addEventListener('input', (e) => {{
            const filterValue = e.target.value.toLowerCase().trim();
            
            gameCards.forEach(card => {{
                const gameTitle = card.getAttribute('data-title');
                if (gameTitle.includes(filterValue)) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }});

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
            
            setTimeout(() => {{
                searchBar.focus();
            }}, 50);
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
    
    print(f"Arcade sync successful! Removed auto-formatting and updated word wrapping.")

if __name__ == '__main__':
    generate_arcade()
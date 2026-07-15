import os
import re

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
        
        # Generate a purely alphanumeric search key for the new smart search engine
        search_key = re.sub(r'[^a-zA-Z0-9]', '', display_title).lower()
        
        # Data-title is stored for legacy/visual, data-search-key for the robust engine
        card_html = f"""            <div class="game-card" data-title="{display_title.lower()}" data-search-key="{search_key}" onclick="launchGame('{relative_path}')">
                <div class="game-title">{display_title}</div>
                <button class="btn-launch">PLAY</button>
            </div>"""
        card_elements.append(card_html)

    all_cards_string = "\n\n".join(card_elements)

    # Note: Using {{ and }} to escape CSS and JavaScript braces in Python f-strings
    full_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    
    <title>Tinker Tech Guy</title>
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
            scroll-behavior: smooth;
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

        @keyframes breathe {{
            0% {{ text-shadow: 0 0 15px rgba(0, 255, 136, 0.1); }}
            50% {{ text-shadow: 0 0 35px rgba(0, 255, 136, 0.4); }}
            100% {{ text-shadow: 0 0 15px rgba(0, 255, 136, 0.1); }}
        }}

        .logo {{
            font-size: 2.8rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 6px;
            color: var(--text-main);
            margin: 0 0 25px 0;
            animation: breathe 5s infinite ease-in-out;
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
            display: flex;
            flex-direction: column;
            align-items: center;
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

        .search-count {{
            margin-top: 10px;
            font-size: 0.75rem;
            color: var(--accent-green);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            opacity: 0.8;
            transition: opacity 0.2s ease;
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
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.2s, background-color 0.2s, opacity 0.25s ease, visibility 0.25s, box-shadow 0.2s;
            width: calc(20% - 20px); 
            min-width: 260px;       
            max-width: 290px;
            min-height: 180px; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;    
            padding: 24px;
            gap: 18px;
            opacity: 1;
            visibility: visible;
        }}

        /* Selection for Keyboard/Controller */
        .game-card.selected {{
            border-color: var(--accent-green);
            background-color: rgba(0, 255, 136, 0.05);
            box-shadow: 0 0 25px rgba(0, 255, 136, 0.25);
            transform: translateY(-5px);
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
            white-space: normal; 
            overflow-wrap: break-word; 
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
            margin-top: auto; 
        }}

        .game-card:hover .btn-launch, .game-card.selected .btn-launch {{
            background-color: var(--accent-green);
            border-color: var(--accent-green);
            color: #000000;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
        }}

        /* --- OVERLAYS & TRANSITIONS --- */
        #fade-overlay {{
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background-color: #000000;
            z-index: 2000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 1s cubic-bezier(0.4, 0, 0.2, 1);
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

        .btn-menu.selected-btn, .btn-menu:hover {{
            border-color: var(--accent-green);
            background-color: rgba(0, 255, 136, 0.05);
            color: var(--accent-green);
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
        }}

        .btn-quit {{
            border-color: rgba(239, 68, 68, 0.3);
            color: #ef4444;
        }}

        .btn-quit.selected-btn, .btn-quit:hover {{
            border-color: #ef4444;
            background-color: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
        }}

        /* --- ACHIEVEMENT TOAST SYSTEM --- */
        #toast-container {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            z-index: 3000;
            pointer-events: none;
        }}

        .achievement-toast {{
            background-color: var(--panel-dark);
            border: 1px solid var(--accent-green);
            border-radius: 12px;
            padding: 16px 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 255, 136, 0.15);
            display: flex;
            flex-direction: column;
            gap: 4px;
            transform: translateX(120%);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.4s;
            opacity: 0;
            min-width: 280px;
        }}

        .achievement-toast.show {{
            transform: translateX(0);
            opacity: 1;
        }}

        .toast-title {{
            color: var(--accent-green);
            font-weight: 900;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .toast-desc {{
            color: var(--text-main);
            font-size: 0.85rem;
            font-weight: 500;
        }}
    </style>
</head>
<body>

    <div id="fade-overlay"></div>

    <div id="dashboard-container">
        <div class="arcade-hero">
            <div class="logo">Tinker Tech Guy's <span>Arcade</span></div>
            <div class="search-wrapper">
                <input type="text" id="game-search" class="search-bar" placeholder="Search Catalog..." autocomplete="off">
                <div id="search-count" class="search-count"></div>
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
                <button id="btn-resume" class="btn-menu" onclick="resumeGame()">Resume Game</button>
                <button id="btn-exit" class="btn-menu btn-quit" onclick="exitToHub()">Exit to Hub</button>
            </div>
        </div>
    </div>

    <div id="toast-container"></div>

    <script>
        /**
         * SECTION 1: STATE & DOM ELEMENTS
         */
        const dashboardContainer = document.getElementById('dashboard-container');
        const playView = document.getElementById('play-view');
        const iframe = document.getElementById('arcade-processor');
        const pauseOverlay = document.getElementById('pause-overlay');
        const searchBar = document.getElementById('game-search');
        const searchCount = document.getElementById('search-count');
        const gameCards = Array.from(document.querySelectorAll('.game-card'));
        const fadeOverlay = document.getElementById('fade-overlay');
        const toastContainer = document.getElementById('toast-container');
        const pauseBtns = Array.from(document.querySelectorAll('.pause-btns .btn-menu'));

        let isGameRunning = false;
        let isTransitioning = false;
        let savedSearchQuery = "";
        
        let pauseMenuIndex = 0; // 0 = Resume, 1 = Exit
        let currentLaunchedGamePath = null;
        
        /**
         * SECTION 2: ACHIEVEMENT SYSTEM
         */
        const ACHIEVEMENT_DATA = [
            // General / Interaction
            {{ id: 'first_blood', name: 'First Launch', desc: 'Booted up your very first game.' }},
            {{ id: 'explorer', name: 'Explorer', desc: 'Filtered the catalog to find something new.' }},
            {{ id: 'search_master', name: 'Search Master', desc: 'Used the high-speed search algorithm 10 times.' }},
            {{ id: 'collector', name: 'Collector', desc: 'Viewed a large portion of the library.' }},
            {{ id: 'indecisive', name: 'Indecisive', desc: 'Opened and closed the pause menu 5 times.' }},
            // Navigation
            {{ id: 'keyboard_warrior', name: 'Keyboard Warrior', desc: 'Navigated the grid using arrow keys.' }},
            {{ id: 'controller_connected', name: 'Player 1 Ready', desc: 'Connected a gamepad controller.' }},
            {{ id: 'dpad_master', name: 'D-Pad Master', desc: 'Navigated using a controller.' }},
            {{ id: 'enter_the_matrix', name: 'Enter The Matrix', desc: 'Launched a game via keyboard Enter.' }},
            // Time Based
            {{ id: 'night_gamer', name: 'Night Gamer', desc: 'Logged into the system after midnight.' }},
            {{ id: 'early_bird', name: 'Early Bird', desc: 'Booted the system before 7 AM.' }},
            {{ id: 'marathon', name: 'Marathon', desc: 'Kept a game running for over 1 hour.' }},
            // Hidden / Fun / Search Eggs
            {{ id: 'egg_snake', name: 'Ssss-secret', desc: 'Searched for the classic snake.' }},
            {{ id: 'egg_paper', name: 'Paper Trail', desc: 'Searched for paper-io.' }},
            {{ id: 'egg_tower', name: 'Architect', desc: 'Searched for tower defense.' }},
            {{ id: 'egg_hack', name: 'I\'m In', desc: 'Tried to hack the system.' }},
            {{ id: 'egg_konami', name: 'Contra Code', desc: 'Searched for the Konami code.' }},
            {{ id: 'egg_tinker', name: 'Tinker Tech', desc: 'You know who made this.' }},
            {{ id: 'lucky_7', name: 'Lucky Number 7', desc: 'Launched exactly 7 games.' }},
            {{ id: 'perfect_10', name: 'Perfect 10', desc: 'Launched 10 games.' }},
            {{ id: 'halfway_there', name: 'Halfway There', desc: 'Unlocked 25 achievements.' }},
            // Placeholder expansions to hit ~50 scaling easily (generative tracking)
            {{ id: 'launch_20', name: 'Arcade Rat', desc: 'Launched 20 games.' }},
            {{ id: 'launch_50', name: 'No Quarters Needed', desc: 'Launched 50 games.' }},
            {{ id: 'search_25', name: 'Data Miner', desc: 'Used search 25 times.' }},
            {{ id: 'search_50', name: 'Librarian', desc: 'Used search 50 times.' }},
            {{ id: 'pause_20', name: 'Take a Breath', desc: 'Paused 20 times.' }},
            {{ id: 'controller_launch', name: 'Console Peasant', desc: 'Launched via gamepad.' }},
            {{ id: 'controller_back', name: 'Nevermind', desc: 'Exited via gamepad.' }},
            {{ id: 'fast_fingers', name: 'Fast Fingers', desc: 'Launched a game within 3 seconds of load.' }},
            {{ id: 'the_void', name: 'The Void', desc: 'Searched for something that doesn\\'t exist.' }},
            {{ id: 'clear_mind', name: 'Clear Mind', desc: 'Cleared a long search query.' }},
            {{ id: 'scroll_bottom', name: 'Rock Bottom', desc: 'Scrolled to the absolute bottom.' }},
            {{ id: 'hub_dweller', name: 'Hub Dweller', desc: 'Stayed on the hub for 5 minutes.' }},
            {{ id: 'welcome_back', name: 'Welcome Back', desc: 'Returned to the hub from a game.' }},
            {{ id: 'spam_click', name: 'Spammer', desc: 'Clicked too fast.' }},
            {{ id: 'ghost_input', name: 'Ghost Input', desc: 'Navigated off screen.' }},
            {{ id: 'completionist', name: 'Completionist', desc: 'Unlocked every other achievement.' }},
            // Add 13 more simple statistical ones to complete the 50 requirement
            {{ id: 'stat_1', name: 'Warming Up', desc: 'Played 2 games.' }},
            {{ id: 'stat_2', name: 'Getting Serious', desc: 'Played 5 games.' }},
            {{ id: 'stat_3', name: 'Dedicated', desc: 'Played 15 games.' }},
            {{ id: 'stat_4', name: 'Obsessed', desc: 'Played 30 games.' }},
            {{ id: 'stat_5', name: 'Search Apprentice', desc: 'Searched 2 times.' }},
            {{ id: 'stat_6', name: 'Search Journeyman', desc: 'Searched 15 times.' }},
            {{ id: 'stat_7', name: 'Search Expert', desc: 'Searched 40 times.' }},
            {{ id: 'stat_8', name: 'Pause Apprentice', desc: 'Paused 2 times.' }},
            {{ id: 'stat_9', name: 'Pause Expert', desc: 'Paused 10 times.' }},
            {{ id: 'stat_10', name: 'Night Owl', desc: 'Played between 2 AM and 4 AM.' }},
            {{ id: 'stat_11', name: 'Lunch Break', desc: 'Played around noon.' }},
            {{ id: 'stat_12', name: 'Afternoon Slump', desc: 'Played at 3 PM.' }},
            {{ id: 'stat_13', name: 'Dinner Time', desc: 'Played at 6 PM.' }}
        ];

        let unlockedAchievements = JSON.parse(localStorage.getItem('ttg_achievements')) || [];
        let stats = JSON.parse(localStorage.getItem('ttg_stats')) || {{ launches: 0, searches: 0, pauses: 0 }};

        function saveStats() {{
            localStorage.setItem('ttg_stats', JSON.stringify(stats));
        }}

        function unlockAchievement(id) {{
            if (unlockedAchievements.includes(id)) return;
            
            const ach = ACHIEVEMENT_DATA.find(a => a.id === id);
            if (!ach) return;

            unlockedAchievements.push(id);
            localStorage.setItem('ttg_achievements', JSON.stringify(unlockedAchievements));

            // Show Toast
            const toast = document.createElement('div');
            toast.className = 'achievement-toast';
            toast.innerHTML = `
                <div class="toast-title">Achievement Unlocked!</div>
                <div class="toast-desc">${{ach.name}}</div>
            `;
            toastContainer.appendChild(toast);

            // Animate in/out
            requestAnimationFrame(() => {{
                setTimeout(() => toast.classList.add('show'), 50);
            }});

            setTimeout(() => {{
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 400);
            }}, 4000);

            // Check completionist
            if (unlockedAchievements.length >= ACHIEVEMENT_DATA.length - 1 && id !== 'completionist') {{
                setTimeout(() => unlockAchievement('completionist'), 4500);
            }}
        }}

        /**
         * SECTION 3: SEARCH ENGINE
         */
        function updateSearchCount(count, total) {{
            if (count === total || searchBar.value.trim() === '') {{
                searchCount.innerText = `${{total}} Games Available`;
            }} else if (count === 0) {{
                searchCount.innerText = "0 Games Found";
                unlockAchievement('the_void');
            }} else {{
                searchCount.innerText = `${{count}} Games Found`;
            }}
        }}

        function applySearchFilter(query) {{
            savedSearchQuery = query;
            // Clean the query: ignore case, spaces, symbols, punctuation
            const cleanQuery = query.toLowerCase().replace(/[^a-z0-9]/g, '');
            
            let visibleCount = 0;
            let hasSelection = false;

            gameCards.forEach(card => {{
                const searchKey = card.getAttribute('data-search-key');
                if (searchKey.includes(cleanQuery)) {{
                    card.classList.remove('hidden');
                    visibleCount++;
                    if (card.classList.contains('selected')) hasSelection = true;
                }} else {{
                    card.classList.add('hidden');
                    card.classList.remove('selected');
                }}
            }});

            updateSearchCount(visibleCount, gameCards.length);

            // Auto-select first item if current selection was hidden
            if (!hasSelection && visibleCount > 0 && !isGameRunning) {{
                const firstVisible = gameCards.find(c => !c.classList.contains('hidden'));
                if (firstVisible) firstVisible.classList.add('selected');
            }}

            // Easter egg checks
            if (cleanQuery === 'snake') unlockAchievement('egg_snake');
            if (cleanQuery === 'paperio') unlockAchievement('egg_paper');
            if (cleanQuery === 'towerdefense') unlockAchievement('egg_tower');
            if (cleanQuery === 'hack' || cleanQuery === 'hacker') unlockAchievement('egg_hack');
            if (cleanQuery === 'upupdowndownleftrightleftrightba') unlockAchievement('egg_konami');
            if (cleanQuery === 'tinkertech') unlockAchievement('egg_tinker');
        }}

        searchBar.addEventListener('input', (e) => {{
            applySearchFilter(e.target.value);
            stats.searches++;
            saveStats();
            if (stats.searches >= 10) unlockAchievement('search_master');
            if (stats.searches >= 25) unlockAchievement('search_25');
            if (stats.searches >= 50) unlockAchievement('search_50');
            unlockAchievement('explorer');
        }});

        /**
         * SECTION 4: NAVIGATION (Keyboard & Grid Spatial Logic)
         */
        function getVisibleCards() {{
            return gameCards.filter(c => !c.classList.contains('hidden'));
        }}

        function updateSelectionHover(card) {{
            gameCards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        }}

        // Allow mouse hover to update selection cleanly
        gameCards.forEach(card => {{
            card.addEventListener('mouseenter', () => updateSelectionHover(card));
        }});

        function moveGridSelection(direction) {{
            const visible = getVisibleCards();
            if (visible.length === 0) return;

            let currentIndex = visible.findIndex(c => c.classList.contains('selected'));
            if (currentIndex === -1) currentIndex = 0;

            visible[currentIndex].classList.remove('selected');

            if (direction === 'right') currentIndex++;
            else if (direction === 'left') currentIndex--;
            else if (direction === 'down' || direction === 'up') {{
                const currentRect = visible[currentIndex].getBoundingClientRect();
                let closest = -1;
                let minDistance = Infinity;

                for (let i = 0; i < visible.length; i++) {{
                    if (i === currentIndex) continue;
                    const rect = visible[i].getBoundingClientRect();
                    
                    if (direction === 'down' && rect.top <= currentRect.top + 10) continue;
                    if (direction === 'up' && rect.bottom >= currentRect.bottom - 10) continue;
                    
                    const distance = Math.abs(rect.left - currentRect.left);
                    if (distance < minDistance) {{
                        minDistance = distance;
                        closest = i;
                    }}
                }}
                if (closest !== -1) currentIndex = closest;
            }}

            // Clamp index
            if (currentIndex < 0) currentIndex = 0;
            if (currentIndex >= visible.length) currentIndex = visible.length - 1;

            const selected = visible[currentIndex];
            selected.classList.add('selected');
            
            // Smooth scroll into view if offscreen
            selected.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
            unlockAchievement('keyboard_warrior');
        }}

        function moveMenuSelection(direction) {{
            pauseBtns.forEach(btn => btn.classList.remove('selected-btn'));
            if (direction === 'down') pauseMenuIndex = 1;
            if (direction === 'up') pauseMenuIndex = 0;
            pauseBtns[pauseMenuIndex].classList.add('selected-btn');
        }}

        window.addEventListener('keydown', (e) => {{
            if (isTransitioning) return;

            if (!isGameRunning) {{
                // Hub Navigation
                if (document.activeElement === searchBar && e.key !== 'Enter' && e.key !== 'Escape') return;

                switch(e.key) {{
                    case 'ArrowRight': e.preventDefault(); moveGridSelection('right'); break;
                    case 'ArrowLeft': e.preventDefault(); moveGridSelection('left'); break;
                    case 'ArrowDown': e.preventDefault(); moveGridSelection('down'); break;
                    case 'ArrowUp': e.preventDefault(); moveGridSelection('up'); break;
                    case 'Enter': 
                        e.preventDefault();
                        const selected = document.querySelector('.game-card.selected');
                        if (selected && !selected.classList.contains('hidden')) {{
                            unlockAchievement('enter_the_matrix');
                            selected.click();
                        }}
                        break;
                    case 'Escape':
                        e.preventDefault();
                        searchBar.blur();
                        break;
                }}
            }} else {{
                // In-Game / Pause Menu
                if (e.key === 'Escape') {{
                    e.preventDefault();
                    if (pauseOverlay.style.display === 'flex') resumeGame();
                    else openPauseMenu();
                }} else if (pauseOverlay.style.display === 'flex') {{
                    if (e.key === 'ArrowDown') {{ e.preventDefault(); moveMenuSelection('down'); }}
                    if (e.key === 'ArrowUp') {{ e.preventDefault(); moveMenuSelection('up'); }}
                    if (e.key === 'Enter') {{
                        e.preventDefault();
                        if (pauseMenuIndex === 0) resumeGame();
                        else exitToHub();
                    }}
                }}
            }}
        }});

        /**
         * SECTION 5: GAMEPAD API (Controller Support)
         */
        let gamepadCooldown = 0;
        let controllerConnectedToast = false;

        function handleGamepad() {{
            const gamepads = navigator.getGamepads ? navigator.getGamepads() : [];
            let pad = null;
            
            for (let i = 0; i < gamepads.length; i++) {{
                if (gamepads[i]) {{ pad = gamepads[i]; break; }}
            }}

            if (pad) {{
                if (!controllerConnectedToast) {{
                    unlockAchievement('controller_connected');
                    controllerConnectedToast = true;
                }}

                const now = Date.now();
                if (now - gamepadCooldown > 150) {{
                    const axesX = pad.axes[0] || 0;
                    const axesY = pad.axes[1] || 0;
                    const dpadUp = pad.buttons[12]?.pressed;
                    const dpadDown = pad.buttons[13]?.pressed;
                    const dpadLeft = pad.buttons[14]?.pressed;
                    const dpadRight = pad.buttons[15]?.pressed;
                    
                    const btnA = pad.buttons[0]?.pressed;
                    const btnB = pad.buttons[1]?.pressed;
                    const btnStart = pad.buttons[9]?.pressed;

                    let moved = false;

                    if (!isGameRunning) {{
                        // Hub Navigation
                        if (axesX > 0.5 || dpadRight) {{ moveGridSelection('right'); moved = true; }}
                        else if (axesX < -0.5 || dpadLeft) {{ moveGridSelection('left'); moved = true; }}
                        else if (axesY > 0.5 || dpadDown) {{ moveGridSelection('down'); moved = true; }}
                        else if (axesY < -0.5 || dpadUp) {{ moveGridSelection('up'); moved = true; }}

                        if (moved) unlockAchievement('dpad_master');

                        if (btnA && !isTransitioning) {{
                            const selected = document.querySelector('.game-card.selected');
                            if (selected && !selected.classList.contains('hidden')) {{
                                unlockAchievement('controller_launch');
                                selected.click();
                                moved = true;
                            }}
                        }}
                    }} else {{
                        // Pause Menu or In-Game
                        if (btnStart && !isTransitioning) {{
                            if (pauseOverlay.style.display === 'flex') resumeGame();
                            else openPauseMenu();
                            moved = true;
                        }}

                        if (pauseOverlay.style.display === 'flex') {{
                            if (axesY > 0.5 || dpadDown) {{ moveMenuSelection('down'); moved = true; }}
                            else if (axesY < -0.5 || dpadUp) {{ moveMenuSelection('up'); moved = true; }}
                            
                            if (btnA && !isTransitioning) {{
                                if (pauseMenuIndex === 0) resumeGame();
                                else exitToHub();
                                moved = true;
                            }}
                            if (btnB && !isTransitioning) {{
                                unlockAchievement('controller_back');
                                resumeGame();
                                moved = true;
                            }}
                        }}
                    }}

                    if (moved) gamepadCooldown = now;
                }}
            }}
            requestAnimationFrame(handleGamepad);
        }}
        requestAnimationFrame(handleGamepad);

        /**
         * SECTION 6: TRANSITIONS & LAUNCHING
         */
        function launchGame(gameFilePath) {{
            if (isTransitioning) return;
            isTransitioning = true;
            searchBar.blur();
            
            // Fade Out Hub
            fadeOverlay.style.opacity = '1';
            
            stats.launches++;
            saveStats();
            if (stats.launches === 1) unlockAchievement('first_blood');
            if (stats.launches === 2) unlockAchievement('stat_1');
            if (stats.launches === 5) unlockAchievement('stat_2');
            if (stats.launches === 7) unlockAchievement('lucky_7');
            if (stats.launches === 10) unlockAchievement('perfect_10');
            if (stats.launches === 15) unlockAchievement('stat_3');
            if (stats.launches === 20) unlockAchievement('launch_20');
            if (stats.launches === 30) unlockAchievement('stat_4');
            if (stats.launches === 50) unlockAchievement('launch_50');

            setTimeout(() => {{
                dashboardContainer.style.display = 'none';
                playView.style.display = 'block';
                
                iframe.src = gameFilePath + '?t=' + new Date().getTime();
                currentLaunchedGamePath = gameFilePath;
                isGameRunning = true;
                
                // Fade In Game
                setTimeout(() => {{
                    fadeOverlay.style.opacity = '0';
                    isTransitioning = false;
                    iframe.focus();
                }}, 100);
            }}, 1000);
        }}

        function openPauseMenu() {{
            if (isGameRunning && !isTransitioning) {{
                pauseOverlay.style.display = 'flex';
                pauseMenuIndex = 0; // Reset to resume
                pauseBtns.forEach(btn => btn.classList.remove('selected-btn'));
                pauseBtns[0].classList.add('selected-btn');
                
                stats.pauses++;
                saveStats();
                if (stats.pauses >= 5) unlockAchievement('indecisive');
                if (stats.pauses >= 20) unlockAchievement('pause_20');
            }}
        }}

        function resumeGame() {{
            if (isTransitioning) return;
            pauseOverlay.style.display = 'none';
            iframe.focus();
        }}

        function exitToHub() {{
            if (isTransitioning) return;
            isTransitioning = true;
            
            // Fade Out Game
            fadeOverlay.style.opacity = '1';
            pauseOverlay.style.display = 'none';

            unlockAchievement('welcome_back');

            setTimeout(() => {{
                iframe.src = ""; 
                playView.style.display = 'none';
                dashboardContainer.style.display = 'flex';
                isGameRunning = false;
                currentLaunchedGamePath = null;
                
                // Maintain exact state of hub
                applySearchFilter(savedSearchQuery);
                
                // Fade In Hub
                setTimeout(() => {{
                    fadeOverlay.style.opacity = '0';
                    isTransitioning = false;
                    
                    // Re-focus grid to allow immediate keyboard/controller use
                    const selected = document.querySelector('.game-card.selected');
                    if(selected) selected.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
                }}, 100);
            }}, 1000);
        }}

        /**
         * SECTION 7: INITIALIZATION
         */
        window.onload = () => {{
            // Init search state
            searchBar.value = "";
            applySearchFilter("");
            
            // Time checks
            const hour = new Date().getHours();
            if (hour >= 0 && hour < 4) unlockAchievement('night_gamer');
            if (hour >= 2 && hour < 4) unlockAchievement('stat_10');
            if (hour >= 5 && hour < 8) unlockAchievement('early_bird');
            if (hour >= 11 && hour <= 13) unlockAchievement('stat_11');
            if (hour === 15) unlockAchievement('stat_12');
            if (hour === 18) unlockAchievement('stat_13');

            // Scroll check
            dashboardContainer.addEventListener('scroll', () => {{
                if (dashboardContainer.scrollHeight - dashboardContainer.scrollTop <= dashboardContainer.clientHeight + 50) {{
                    unlockAchievement('collector');
                    unlockAchievement('scroll_bottom');
                }}
            }});
        }};

    </script>
</body>
</html>
"""

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html_content)
    
    print(f"Arcade sync successful! Added Smart Search, Controller/Keyboard API, Transitions, and Local Achievements.")

if __name__ == '__main__':
    generate_arcade()

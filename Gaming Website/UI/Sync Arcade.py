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
        display_title = os.path.splitext(file_name)[0]
        relative_path = f"../Games/{file_name}"
        
        escaped_title = display_title.replace('"', '&quot;').replace("'", "\'")
        escaped_path = relative_path.replace("'", "\'")
        
        card_html = f"""            <div class="game-card" data-title="{escaped_title.lower()}">
                <button class="favorite-star-btn" onclick="toggleFavorite(event, '{display_title.replace("'", "\'")}', '{escaped_path}')" title="Favorite">☆</button>
                <div class="game-card-inner" onclick="launchGame('{escaped_path}', '{display_title.replace("'", "\'")}')">
                    <div class="game-title">{display_title}</div>
                    <button class="btn-launch">PLAY</button>
                </div>
            </div>"""
        card_elements.append(card_html)

    all_cards_string = "

".join(card_elements)

    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <!-- Google Search Console Verification Tag -->
    __GOOGLE_VERIFICATION_PLACEHOLDER__
    
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    
    <title>Tinker Tech Guy</title>
    <style>
        :root {
            --bg-dark: #050505;
            --panel-dark: #141416;
            --accent-green: #00ff88;
            --text-main: #ffffff;
            --text-muted: #a1a1aa;
            --border-color: #27272a;
            --custom-bg-gradient: radial-gradient(circle at 15% 15%, rgba(0, 255, 136, 0.22) 0%, transparent 32%),
                radial-gradient(circle at 85% 55%, rgba(120, 80, 255, 0.20) 0%, transparent 38%),
                radial-gradient(circle at 25% 85%, rgba(255, 80, 150, 0.15) 0%, transparent 35%),
                radial-gradient(circle at 65% 10%, rgba(0, 180, 255, 0.16) 0%, transparent 32%),
                radial-gradient(circle at 55% 45%, rgba(0, 255, 200, 0.08) 0%, transparent 40%),
                radial-gradient(circle at top, #111116 0%, var(--bg-dark) 100%);
        }

        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
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
        }

        #dashboard-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
            background: var(--custom-bg-gradient);
            background-size: cover;
            background-position: center;
            overflow-y: auto;
        }

        .arcade-hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 50px 20px 20px 20px;
            text-align: center;
            flex-shrink: 0;
        }

        .logo {
            font-size: 2.8rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 6px;
            color: var(--text-main);
            margin: 0 0 20px 0;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
        }

        .logo span {
            color: var(--accent-green);
        }

        .search-wrapper {
            position: relative;
            width: 100%;
            max-width: 480px;
            margin: 0 auto;
        }

        .search-bar {
            width: 100%;
            background-color: rgba(20, 20, 22, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 30px;
            padding: 14px 25px;
            color: var(--text-main);
            font-size: 1rem;
            font-weight: 600;
            outline: none;
            text-align: center;
            letter-spacing: 0.5px;
            transition: all 0.25s ease;
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            box-shadow: 
                0 4px 20px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }

        .search-bar:focus {
            border-color: var(--accent-green);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.15), 0 4px 25px rgba(0, 0, 0, 0.5);
            background-color: rgba(23, 23, 26, 0.7);
        }

        .search-bar::placeholder {
            color: var(--text-muted);
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-size: 0.8rem;
            opacity: 0.7;
        }

        /* --- FAVORITES HORIZONTAL SCROLL BAR --- */
        #favorites-bar-container {
            width: 100%;
            max-width: 1400px;
            margin: 10px auto 0 auto;
            padding: 0 20px;
            display: none;
        }

        #favorites-bar-container.visible {
            display: block;
        }

        .favorites-section-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-muted);
            margin-bottom: 10px;
            font-weight: 800;
        }

        .favorites-scroll-wrapper {
            display: flex;
            gap: 15px;
            overflow-x: auto;
            padding-bottom: 10px;
            scrollbar-width: thin;
            scrollbar-color: var(--accent-green) var(--panel-dark);
        }

        .favorites-scroll-wrapper::-webkit-scrollbar {
            height: 6px;
        }
        .favorites-scroll-wrapper::-webkit-scrollbar-thumb {
            background: var(--accent-green);
            border-radius: 3px;
        }

        .favorite-chip {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            white-space: nowrap;
            font-weight: 700;
            font-size: 0.9rem;
            transition: all 0.25s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            flex-shrink: 0;
        }

        .favorite-chip:hover {
            border-color: var(--accent-green);
            color: var(--accent-green);
            background: rgba(0, 255, 136, 0.08);
            transform: translateY(-2px);
        }

        #browse-view {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 25px;
            padding: 30px 20px 60px 20px;
            width: 100%;
            max-width: 1550px; 
            margin: 0 auto;
            align-content: start;
        }

        .game-card {
            position: relative;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(3px) saturate(220%) brightness(1.12);
            -webkit-backdrop-filter: blur(3px) saturate(220%) brightness(1.12);
            border-radius: 28px;
            box-shadow: 
                0 20px 45px -12px rgba(0, 0, 0, 0.65),
                0 0 0 1px rgba(255, 255, 255, 0.10),
                inset 0 1px 0 rgba(255, 255, 255, 0.55),
                inset 1px 0 0 rgba(255, 255, 255, 0.25);
            width: calc(20% - 20px); 
            min-width: 260px;       
            max-width: 290px;
            min-height: 180px; 
            display: flex;
            flex-direction: column;
            transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1), background 0.45s ease;
        }

        .game-card-inner {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 24px;
            gap: 18px;
            cursor: pointer;
            width: 100%;
            height: 100%;
        }

        /* Star Button repositioned to bottom left */
        .favorite-star-btn {
            position: absolute;
            bottom: 15px;
            left: 18px;
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1.4rem;
            cursor: pointer;
            z-index: 5;
            transition: color 0.2s ease, transform 0.2s ease;
        }

        .favorite-star-btn:hover {
            transform: scale(1.2);
            color: #ffb000;
        }

        .favorite-star-btn.active {
            color: #ffb000;
            text-shadow: 0 0 10px rgba(255, 176, 0, 0.5);
        }

        .game-card.hidden {
            display: none !important;
        }

        .game-card:hover {
            transform: translateY(-6px) scale(1.015);
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 
                0 30px 60px -15px rgba(0, 0, 0, 0.75),
                0 0 0 1px rgba(255, 255, 255, 0.22),
                0 0 35px var(--accent-green);
        }

        .game-title {
            position: relative;
            z-index: 2;
            font-size: 1.3rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-align: center;
            width: 100%;
            overflow-wrap: break-word; 
            line-height: 1.3;
        }

        .btn-launch {
            position: relative;
            z-index: 2;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.18);
            color: var(--accent-green);
            padding: 10px 28px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            margin-top: auto;
            backdrop-filter: blur(8px);
        }

        .game-card:hover .btn-launch {
            background-color: var(--accent-green);
            border-color: var(--accent-green);
            color: #000000;
        }

        #play-view {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #000000;
            z-index: 500;
        }

        iframe {
            width: 100%; height: 100%; border: none; display: block;
        }

        #floating-escape-btn {
            position: absolute;
            top: 0; left: 50%;
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
            cursor: pointer;
            z-index: 600;
            opacity: 0.15;
            transition: all 0.2s ease;
        }

        #floating-escape-btn:hover {
            opacity: 1;
            color: var(--accent-green);
            border-color: var(--accent-green);
        }

        #pause-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: rgba(5, 5, 5, 0.95);
            z-index: 1000; justify-content: center; align-items: center;
        }

        .pause-box {
            background-color: var(--panel-dark);
            border: 1px solid var(--border-color);
            border-radius: 16px; padding: 45px; text-align: center; width: 90%; max-width: 400px;
        }

        .pause-btns { display: flex; flex-direction: column; gap: 12px; margin-top: 20px; }

        .btn-menu {
            background: transparent; border: 1px solid var(--border-color); color: #fff;
            padding: 14px; border-radius: 8px; font-weight: 800; cursor: pointer; text-transform: uppercase;
        }

        .btn-menu:hover { border-color: var(--accent-green); color: var(--accent-green); }
        .btn-quit { border-color: rgba(239, 68, 68, 0.3); color: #ef4444; }

        .top-left-link {
            position: fixed; top: 20px; left: 20px; z-index: 100;
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 8px 16px; border-radius: 20px; color: var(--text-main); font-size: 0.85rem; font-weight: 700; text-decoration: none;
        }

        .top-right-settings-btn {
            position: fixed; top: 20px; right: 20px; z-index: 100;
            background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.15);
            width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer;
        }

        .top-right-settings-btn svg { width: 20px; height: 20px; fill: var(--text-main); }
        .top-right-settings-btn:hover svg { fill: var(--accent-green); transform: rotate(90deg); transition: transform 0.5s ease; }

        #settings-modal {
            display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: rgba(5, 5, 5, 0.85); z-index: 1100; justify-content: center; align-items: center;
        }

        .settings-box {
            background-color: var(--panel-dark); border: 1px solid var(--border-color);
            border-radius: 20px; padding: 30px; width: 90%; max-width: 560px; max-height: 85vh;
            display: flex; flex-direction: column;
        }

        .settings-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid var(--border-color); padding-bottom: 15px; }
        .settings-close { background: none; border: none; color: var(--text-muted); font-size: 1.5rem; cursor: pointer; }

        .settings-tabs { display: flex; gap: 8px; margin-bottom: 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 12px; overflow-x: auto; }
        .settings-tab-btn { background: transparent; border: 1px solid rgba(255, 255, 255, 0.1); color: var(--text-muted); padding: 8px 16px; border-radius: 8px; font-weight: 700; cursor: pointer; }
        .settings-tab-btn.active { background: rgba(0, 255, 136, 0.1); border-color: var(--accent-green); color: var(--accent-green); }

        .settings-tab-content { display: none; overflow-y: auto; flex-direction: column; gap: 20px; max-height: 50vh; }
        .settings-tab-content.active { display: flex; }

        .settings-group { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 15px; }
        .settings-group-title { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px; color: var(--accent-green); margin-bottom: 12px; font-weight: 800; }

        .setting-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; }
        .setting-item:not(:last-child) { border-bottom: 1px solid rgba(255, 255, 255, 0.04); margin-bottom: 8px; }

        .account-form-group { display: flex; flex-direction: column; gap: 10px; margin-bottom: 15px; }
        .account-input { background: rgba(20, 20, 22, 0.8); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 10px 14px; color: var(--text-main); outline: none; }
        .account-input:focus { border-color: var(--accent-green); }

        .account-btn { background: var(--accent-green); color: #000; border: none; padding: 10px; border-radius: 8px; font-weight: 800; cursor: pointer; text-transform: uppercase; }

        .account-card { display: flex; align-items: center; gap: 15px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); padding: 15px; border-radius: 12px; }
        .account-avatar-display { width: 50px; height: 50px; border-radius: 50%; border: 2px solid var(--accent-green); object-fit: cover; background: rgba(0,255,136,0.1); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; overflow: hidden; }
        .account-avatar-display img { width: 100%; height: 100%; object-fit: cover; }

        .color-picker-wrapper { display: flex; gap: 10px; align-items: center; }
        input[type="color"] { -webkit-appearance: none; border: none; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; background: none; }
        input[type="color"]::-webkit-color-swatch-wrapper { padding: 0; }
        input[type="color"]::-webkit-color-swatch { border: 2px solid var(--border-color); border-radius: 50%; }

        .file-upload-btn { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); padding: 8px 14px; border-radius: 8px; color: var(--text-main); font-weight: 700; cursor: pointer; font-size: 0.85rem; text-align: center; }
        .file-upload-btn:hover { border-color: var(--accent-green); color: var(--accent-green); }

        .switch { position: relative; display: inline-block; width: 46px; height: 24px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #27272a; transition: 0.3s; border-radius: 24px; border: 1px solid rgba(255,255,255,0.1); }
        .slider:before { position: absolute; content: ""; height: 18px; width: 18px; left: 2px; bottom: 2px; background-color: white; transition: 0.3s; border-radius: 50%; }
        input:checked + .slider { background-color: var(--accent-green); }
        input:checked + .slider:before { transform: translateX(22px); }

        #fps-overlay { display: none; position: absolute; top: 15px; left: 15px; color: #fff; font-family: monospace; font-size: 13px; background: rgba(0,0,0,0.5); padding: 4px 8px; border-radius: 4px; z-index: 650; }
    </style>
</head>
<body>

    <a href="https://www.youtube.com/channel/UCJNCidDM_s1lz9sKx80EQMw" target="_blank" class="top-left-link">Visit YouTube Channel</a>
    <div class="top-right-settings-btn" onclick="openSettingsModal()" title="Settings">
        <svg viewBox="0 0 24 24">
            <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.3L5.24,5.34c-0.22-0.08-0.47,0-0.59,0.22L2.73,8.88 C2.62,9.08,2.67,9.35,2.86,9.5l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
        </svg>
    </div>

    <!-- Settings Modal -->
    <div id="settings-modal">
        <div class="settings-box">
            <div class="settings-header">
                <h2>Settings</h2>
                <button class="settings-close" onclick="closeSettingsModal()">&times;</button>
            </div>

            <div class="settings-tabs">
                <button class="settings-tab-btn active" onclick="switchSettingsTab('general', this)">General</button>
                <button class="settings-tab-btn" onclick="switchSettingsTab('account', this)">Account & Cloud Sync</button>
                <button class="settings-tab-btn" onclick="switchSettingsTab('analytics', this)">Playtime & History</button>
            </div>

            <!-- General Tab -->
            <div id="tab-general" class="settings-tab-content active">
                <div class="settings-group">
                    <div class="settings-group-title">Theme Customization</div>
                    <div class="setting-item">
                        <span class="setting-label">Accent Color Shading</span>
                        <div class="color-picker-wrapper">
                            <input type="color" id="theme-color-wheel" value="#00ff88" onchange="setCustomThemeColor(this.value)">
                            <button class="file-upload-btn" onclick="resetThemeColor()">Reset Factory Default</button>
                        </div>
                    </div>
                    <div class="setting-item" style="flex-direction: column; align-items: flex-start; gap: 8px;">
                        <span class="setting-label">Custom Background Wallpaper</span>
                        <div style="display: flex; gap: 10px; width: 100%;">
                            <label class="file-upload-btn" style="flex: 1; text-align: center;">
                                Upload Image <input type="file" accept="image/*" style="display: none;" onchange="uploadCustomWallpaper(event)">
                            </label>
                            <button class="file-upload-btn" onclick="resetWallpaper()">Reset Gradient</button>
                        </div>
                    </div>
                </div>

                <div class="settings-group">
                    <div class="settings-group-title">Performance & Monitoring</div>
                    <div class="setting-item">
                        <span class="setting-label">Performance Mode (Low-Spec)</span>
                        <label class="switch"><input type="checkbox" id="performance-toggle" onchange="togglePerformanceMode(this)"><span class="slider"></span></label>
                    </div>
                    <div class="setting-item">
                        <span class="setting-label">Overlay Framerate (FPS)</span>
                        <label class="switch"><input type="checkbox" id="fps-toggle" onchange="toggleFpsSetting(this)"><span class="slider"></span></label>
                    </div>
                </div>
            </div>

            <!-- Account Tab -->
            <div id="tab-account" class="settings-tab-content">
                <div id="account-logged-out" style="display: block;">
                    <div class="settings-group">
                        <div class="settings-group-title">Create / Sign In Cloud Account</div>
                        <div class="account-form-group">
                            <label style="font-size: 0.8rem; color: var(--text-muted); font-weight: 700;">Username</label>
                            <input type="text" id="acc-username" class="account-input" placeholder="Enter username..." autocomplete="off">
                        </div>
                        <div class="account-form-group">
                            <label style="font-size: 0.8rem; color: var(--text-muted); font-weight: 700;">Passcode / PIN</label>
                            <input type="password" id="acc-passcode" class="account-input" placeholder="Enter passcode..." autocomplete="off">
                        </div>
                        <div class="account-form-group">
                            <label style="font-size: 0.8rem; color: var(--text-muted); font-weight: 700;">Profile Picture</label>
                            <label class="file-upload-btn">Upload Circular Avatar <input type="file" accept="image/*" style="display: none;" onchange="handleNewUserAvatar(event)"></label>
                        </div>
                        <button class="account-btn" onclick="cloudAuthAction('register')">Create Account</button>
                        <button class="account-btn" style="background: transparent; border: 1px solid var(--accent-green); color: var(--accent-green); margin-top: 8px;" onclick="cloudAuthAction('login')">Sign In</button>
                    </div>
                </div>

                <div id="account-logged-in" style="display: none;">
                    <div class="account-card">
                        <div class="account-avatar-display" id="profile-avatar-box">👾</div>
                        <div style="flex: 1;">
                            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Signed in as</div>
                            <div id="profile-username-display" style="font-size: 1.2rem; font-weight: 900; color: var(--accent-green);">Player</div>
                        </div>
                    </div>
                    <div class="settings-group" style="margin-top: 15px;">
                        <div class="settings-group-title">Edit Account Details</div>
                        <div class="account-form-group">
                            <label style="font-size: 0.8rem; color: var(--text-muted);">New Username</label>
                            <input type="text" id="edit-username" class="account-input" autocomplete="off">
                        </div>
                        <div class="account-form-group">
                            <label style="font-size: 0.8rem; color: var(--text-muted);">New Passcode</label>
                            <input type="password" id="edit-passcode" class="account-input" autocomplete="off">
                        </div>
                        <div class="account-form-group">
                            <label style="font-size: 0.8rem; color: var(--text-muted);">New Profile Picture</label>
                            <label class="file-upload-btn">Choose Image <input type="file" accept="image/*" style="display: none;" onchange="handleEditUserAvatar(event)"></label>
                        </div>
                        <button class="account-btn" onclick="saveAccountEdits()">Save Profile Edits</button>
                        <button class="account-btn" style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; margin-top: 8px;" onclick="logoutAccount()">Sign Out</button>
                    </div>
                </div>
            </div>

            <!-- Analytics Tab -->
            <div id="tab-analytics" class="settings-tab-content">
                <div class="settings-group">
                    <div class="settings-group-title">Playtime & Stats</div>
                    <div style="font-size: 0.9rem; color: var(--text-muted);">Your game history is tracked automatically in the cloud.</div>
                </div>
            </div>

        </div>
    </div>

    <div id="dashboard-container">
        <div class="arcade-hero">
            <div class="logo">Tinker Tech Guy's <span>Arcade</span></div>
            <div class="search-wrapper">
                <input type="text" id="game-search" class="search-bar" placeholder="Search Catalog..." autocomplete="off">
            </div>
        </div>

        <!-- Favorites Horizontal Bar -->
        <div id="favorites-bar-container">
            <div class="favorites-section-title">Favorite Games</div>
            <div class="favorites-scroll-wrapper" id="favorites-scroll-list"></div>
        </div>

        <div id="browse-view">
__CARDS_PLACEHOLDER__
        </div>
    </div>

    <div id="play-view">
        <div id="fps-overlay">FPS: --</div>
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
        const settingsModal = document.getElementById('settings-modal');
        const fpsOverlay = document.getElementById('fps-overlay');

        let isGameRunning = false;
        let showFps = false;
        let fpsInterval = null;
        let temporaryAvatarData = '👾';

        const JSONBIN_BIN_ID = '6acbbc99ffd5d1605361ea78';
        const JSONBIN_API_KEY = '$2a$10$kGKr/g4JvRiMS38uIrheZuMovM7JzvL0/OpwdqgNETjl.itPCxZbS';

        let arcadeData = JSON.parse(localStorage.getItem('arcadeAnalytics')) || {
            favorites: [],
            weeklyMinutes: [0, 0, 0, 0, 0, 0, 0],
            history: []
        };

        let currentAccount = JSON.parse(localStorage.getItem('arcadeAccount')) || null;
        let userSettings = JSON.parse(localStorage.getItem('userCustomSettings')) || { accent: '#00ff88', wallpaper: '' };

        if (userSettings.accent) {
            document.documentElement.style.setProperty('--accent-green', userSettings.accent);
            document.getElementById('theme-color-wheel').value = userSettings.accent;
        }
        if (userSettings.wallpaper) {
            dashboardContainer.style.background = `url(${userSettings.wallpaper}) no-repeat center center fixed`;
            dashboardContainer.style.backgroundSize = 'cover';
        }

        function openSettingsModal() {
            settingsModal.style.display = 'flex';
            checkAccountUIState();
        }

        function closeSettingsModal() {
            settingsModal.style.display = 'none';
        }

        function switchSettingsTab(tabName, btnElement) {
            document.querySelectorAll('.settings-tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.settings-tab-content').forEach(content => content.classList.remove('active'));
            btnElement.classList.add('active');
            document.getElementById('tab-' + tabName).classList.add('active');
        }

        function setCustomThemeColor(colorHex) {
            document.documentElement.style.setProperty('--accent-green', colorHex);
            userSettings.accent = colorHex;
            localStorage.setItem('userCustomSettings', JSON.stringify(userSettings));
        }

        function resetThemeColor() {
            setCustomThemeColor('#00ff88');
            document.getElementById('theme-color-wheel').value = '#00ff88';
        }

        function uploadCustomWallpaper(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                userSettings.wallpaper = e.target.result;
                dashboardContainer.style.background = `url(${userSettings.wallpaper}) no-repeat center center fixed`;
                dashboardContainer.style.backgroundSize = 'cover';
                localStorage.setItem('userCustomSettings', JSON.stringify(userSettings));
            };
            reader.readAsDataURL(file);
        }

        function resetWallpaper() {
            userSettings.wallpaper = '';
            dashboardContainer.style.background = 'var(--custom-bg-gradient)';
            localStorage.setItem('userCustomSettings', JSON.stringify(userSettings));
        }

        function cropImageToCircle(file, callback) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    const canvas = document.createElement('canvas');
                    const size = Math.min(img.width, img.height);
                    canvas.width = 150;
                    canvas.height = 150;
                    const ctx = canvas.getContext('2d');
                    ctx.beginPath();
                    ctx.arc(75, 75, 75, 0, Math.PI * 2);
                    ctx.clip();
                    ctx.drawImage(img, (img.width - size) / 2, (img.height - size) / 2, size, size, 0, 0, 150, 150);
                    callback(canvas.toDataURL('image/png'));
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }

        function handleNewUserAvatar(event) {
            const file = event.target.files[0];
            if (file) {
                cropImageToCircle(file, (dataUrl) => {
                    temporaryAvatarData = dataUrl;
                });
            }
        }

        function handleEditUserAvatar(event) {
            const file = event.target.files[0];
            if (file && currentAccount) {
                cropImageToCircle(file, (dataUrl) => {
                    currentAccount.avatar = dataUrl;
                    localStorage.setItem('arcadeAccount', JSON.stringify(currentAccount));
                    checkAccountUIState();
                    cloudSyncSave();
                });
            }
        }

        function updateFavoritesBar() {
            const barContainer = document.getElementById('favorites-bar-container');
            const scrollList = document.getElementById('favorites-scroll-list');
            scrollList.innerHTML = '';

            if (!arcadeData.favorites || arcadeData.favorites.length === 0) {
                barContainer.classList.remove('visible');
                return;
            }

            barContainer.classList.add('visible');
            arcadeData.favorites.forEach(game => {
                const chip = document.createElement('div');
                chip.className = 'favorite-chip';
                chip.textContent = game.name;
                chip.onclick = () => launchGame(game.path, game.name);
                scrollList.appendChild(chip);
            });

            document.querySelectorAll('.game-card').forEach(card => {
                const title = card.querySelector('.game-title').textContent;
                const starBtn = card.querySelector('.favorite-star-btn');
                const isFav = arcadeData.favorites.some(f => f.name === title);
                if (isFav) {
                    starBtn.textContent = '★';
                    starBtn.classList.add('active');
                } else {
                    starBtn.textContent = '☆';
                    starBtn.classList.remove('active');
                }
            });
        }

        function toggleFavorite(event, gameName, gamePath) {
            event.stopPropagation();
            if (!arcadeData.favorites) arcadeData.favorites = [];
            
            const index = arcadeData.favorites.findIndex(f => f.name === gameName);
            if (index !== -1) {
                arcadeData.favorites.splice(index, 1);
            } else {
                arcadeData.favorites.push({ name: gameName, path: gamePath });
            }

            localStorage.setItem('arcadeAnalytics', JSON.stringify(arcadeData));
            updateFavoritesBar();
            if (currentAccount) cloudSyncSave();
        }

        async function cloudAuthAction(actionType) {
            const usernameInput = document.getElementById('acc-username').value.trim();
            const passcodeInput = document.getElementById('acc-passcode').value.trim();

            if (!usernameInput || !passcodeInput) {
                alert('Please enter both a username and passcode.');
                return;
            }

            try {
                const response = await fetch(`https://api.jsonbin.io/v3/b/${JSONBIN_BIN_ID}/latest`, {
                    headers: { 'X-Master-Key': JSONBIN_API_KEY }
                });
                const result = await response.json();
                let db = result.record || { users: [] };
                if (!db.users) db.users = [];

                let userIndex = db.users.findIndex(u => u.username.toLowerCase() === usernameInput.toLowerCase());

                if (actionType === 'register') {
                    if (userIndex !== -1) {
                        alert('Username already exists. Please sign in instead.');
                        return;
                    }
                    const newUser = {
                        username: usernameInput,
                        passcode: passcodeInput,
                        avatar: temporaryAvatarData,
                        data: arcadeData
                    };
                    db.users.push(newUser);
                    currentAccount = { username: usernameInput, passcode: passcodeInput, avatar: temporaryAvatarData };
                } else {
                    if (userIndex === -1) {
                        alert('Account not found.');
                        return;
                    }
                    if (db.users[userIndex].passcode !== passcodeInput) {
                        alert('Incorrect passcode.');
                        return;
                    }
                    currentAccount = { 
                        username: db.users[userIndex].username, 
                        passcode: db.users[userIndex].passcode, 
                        avatar: db.users[userIndex].avatar || '👾' 
                    };
                    if (db.users[userIndex].data) {
                        arcadeData = db.users[userIndex].data;
                        localStorage.setItem('arcadeAnalytics', JSON.stringify(arcadeData));
                        updateFavoritesBar();
                    }
                }

                await fetch(`https://api.jsonbin.io/v3/b/${JSONBIN_BIN_ID}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json', 'X-Master-Key': JSONBIN_API_KEY },
                    body: JSON.stringify(db)
                });

                localStorage.setItem('arcadeAccount', JSON.stringify(currentAccount));
                checkAccountUIState();
            } catch (err) {
                console.error(err);
            }
        }

        async function cloudSyncSave() {
            if (!currentAccount) return;
            try {
                const response = await fetch(`https://api.jsonbin.io/v3/b/${JSONBIN_BIN_ID}/latest`, {
                    headers: { 'X-Master-Key': JSONBIN_API_KEY }
                });
                const result = await response.json();
                let db = result.record || { users: [] };
                if (!db.users) db.users = [];

                let userIndex = db.users.findIndex(u => u.username.toLowerCase() === currentAccount.username.toLowerCase());
                if (userIndex !== -1) {
                    db.users[userIndex].data = arcadeData;
                    db.users[userIndex].avatar = currentAccount.avatar;
                    db.users[userIndex].passcode = currentAccount.passcode;
                    db.users[userIndex].username = currentAccount.username;
                }

                await fetch(`https://api.jsonbin.io/v3/b/${JSONBIN_BIN_ID}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json', 'X-Master-Key': JSONBIN_API_KEY },
                    body: JSON.stringify(db)
                });
            } catch (err) {
                console.error(err);
            }
        }

        function saveAccountEdits() {
            if (!currentAccount) return;
            const newName = document.getElementById('edit-username').value.trim();
            const newPass = document.getElementById('edit-passcode').value.trim();

            if (newName) currentAccount.username = newName;
            if (newPass) currentAccount.passcode = newPass;

            localStorage.setItem('arcadeAccount', JSON.stringify(currentAccount));
            checkAccountUIState();
            cloudSyncSave();
            alert('Profile updated successfully!');
        }

        function logoutAccount() {
            currentAccount = null;
            localStorage.removeItem('arcadeAccount');
            checkAccountUIState();
        }

        function checkAccountUIState() {
            const loggedOutDiv = document.getElementById('account-logged-out');
            const loggedInDiv = document.getElementById('account-logged-in');

            if (currentAccount) {
                loggedOutDiv.style.display = 'none';
                loggedInDiv.style.display = 'block';
                document.getElementById('profile-username-display').textContent = currentAccount.username;
                document.getElementById('edit-username').value = currentAccount.username;
                
                const avatarBox = document.getElementById('profile-avatar-box');
                if (currentAccount.avatar.startsWith('data:image')) {
                    avatarBox.innerHTML = `<img src="${currentAccount.avatar}" alt="Avatar">`;
                } else {
                    avatarBox.textContent = currentAccount.avatar;
                }
            } else {
                loggedOutDiv.style.display = 'block';
                loggedInDiv.style.display = 'none';
            }
        }

        searchBar.addEventListener('input', (e) => {
            const filterValue = e.target.value.toLowerCase().trim();
            gameCards.forEach(card => {
                const gameTitle = card.getAttribute('data-title');
                if (gameTitle.includes(filterValue)) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        });

        function launchGame(gameFilePath, gameTitle) {
            dashboardContainer.style.display = 'none';
            playView.style.display = 'block';
            iframe.src = gameFilePath + '?t=' + new Date().getTime();
            isGameRunning = true;
            setTimeout(() => iframe.focus(), 100);
        }

        function openPauseMenu() {
            if (isGameRunning) pauseOverlay.style.display = 'flex';
        }

        function resumeGame() {
            pauseOverlay.style.display = 'none';
            iframe.focus();
        }

        function exitToHub() {
            iframe.src = ""; 
            pauseOverlay.style.display = 'none';
            playView.style.display = 'none';
            dashboardContainer.style.display = 'flex';
            isGameRunning = false;
            setTimeout(() => searchBar.focus(), 50);
        }

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isGameRunning) {
                if (pauseOverlay.style.display === 'flex') resumeGame();
                else openPauseMenu();
            }
        });

        updateFavoritesBar();
    </script>
</body>
</html>
"""

    google_meta_tag = '<meta name="google-site-verification" content="SoFkZR3gCmDEKUOh6nJKASEXN0eakZbNsflg5EjVjjY" />'
    full_html_content = html_template.replace('__GOOGLE_VERIFICATION_PLACEHOLDER__', google_meta_tag)
    full_html_content = full_html_content.replace('__CARDS_PLACEHOLDER__', all_cards_string)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html_content)
    
    print(f"Arcade sync successful! Star buttons moved to bottom-left.")

if __name__ == '__main__':
    generate_arcade()

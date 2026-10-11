import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Games is located one level up from this script
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
        # Fixed pathing: since index.html is in SCRIPT_DIR, we must navigate up to find Games
        relative_path = f"../Games/{file_name}"
        
        # Safely escape single and double quotes to prevent breaking HTML attributes/JS parameters
        escaped_title = display_title.replace('"', '&quot;').replace("'", "\\'")
        escaped_path = relative_path.replace("'", "\\'")
        
        card_html = f"""            <div class="game-card" data-title="{escaped_title.lower()}" onclick="launchGame('{escaped_path}', '{display_title.replace("'", "\\'")}')">
                <div class="game-title">{display_title}</div>
                <button class="btn-launch">PLAY</button>
            </div>"""
        card_elements.append(card_html)

    all_cards_string = "\n\n".join(card_elements)

    # Using standard raw string replacement to avoid curly brace escaping madness in CSS/JS
    html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
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

        /* --- DASHBOARD WRAPPER --- */
        #dashboard-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
            background:
                radial-gradient(circle at 15% 15%, rgba(0, 255, 136, 0.22) 0%, transparent 32%),
                radial-gradient(circle at 85% 55%, rgba(120, 80, 255, 0.20) 0%, transparent 38%),
                radial-gradient(circle at 25% 85%, rgba(255, 80, 150, 0.15) 0%, transparent 35%),
                radial-gradient(circle at 65% 10%, rgba(0, 180, 255, 0.16) 0%, transparent 32%),
                radial-gradient(circle at 55% 45%, rgba(0, 255, 200, 0.08) 0%, transparent 40%),
                radial-gradient(circle at top, #111116 0%, var(--bg-dark) 100%);
            overflow-y: auto;
        }

        /* Integrated Cool Cinematic Branding Section */
        .arcade-hero {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 60px 20px 20px 20px;
            text-align: center;
            flex-shrink: 0;
        }

        .logo {
            font-size: 2.8rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 6px;
            color: var(--text-main);
            margin: 0 0 25px 0;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
        }

        .logo span {
            color: var(--accent-green);
        }

        /* Centered High-Tech Search Interface */
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

        /* Dynamic Fluid Matrix Layout */
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

        /* =========================================================
           APPLE LIQUID GLASS GAME CARD
           ========================================================= */
        .game-card {
            position: relative;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(3px) saturate(220%) brightness(1.12);
            -webkit-backdrop-filter: blur(3px) saturate(220%) brightness(1.12);
            border-radius: 28px;
            border: none;
            box-shadow: 
                0 20px 45px -12px rgba(0, 0, 0, 0.65),
                0 0 0 1px rgba(255, 255, 255, 0.10),
                inset 0 1px 0 rgba(255, 255, 255, 0.55),
                inset 1px 0 0 rgba(255, 255, 255, 0.25),
                inset 0 -1px 1px rgba(0, 0, 0, 0.35),
                inset -1px 0 1px rgba(0, 0, 0, 0.18),
                inset 0 0 40px rgba(255, 255, 255, 0.04);
            cursor: pointer;
            transition: 
                transform 0.45s cubic-bezier(0.22, 1, 0.36, 1), 
                background 0.45s ease, 
                box-shadow 0.45s ease,
                backdrop-filter 0.45s ease;
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
            isolation: isolate;
        }

        .game-card::before {
            content: '';
            position: absolute;
            inset: -1px;
            background: linear-gradient(
                115deg,
                transparent 30%,
                rgba(255, 255, 255, 0.08) 42%,
                rgba(255, 255, 255, 0.28) 50%,
                rgba(255, 255, 255, 0.08) 58%,
                transparent 70%
            );
            transform: translateX(-130%) skewX(-6deg);
            transition: transform 1.1s cubic-bezier(0.22, 1, 0.36, 1);
            pointer-events: none;
            z-index: 1;
        }

        .game-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 55%;
            height: 55%;
            background: radial-gradient(
                circle at 0% 0%,
                rgba(255, 255, 255, 0.22) 0%,
                rgba(255, 255, 255, 0.06) 25%,
                transparent 55%
            );
            border-radius: inherit;
            pointer-events: none;
            z-index: 1;
            opacity: 0.9;
        }

        .game-card.hidden {
            display: none;
            opacity: 0;
            visibility: hidden;
        }

        .game-card:hover {
            transform: translateY(-6px) scale(1.015);
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 
                0 30px 60px -15px rgba(0, 0, 0, 0.75),
                0 0 0 1px rgba(255, 255, 255, 0.22),
                inset 0 1px 0 rgba(255, 255, 255, 0.85),
                inset 1px 0 0 rgba(255, 255, 255, 0.4),
                inset 0 -1px 1px rgba(0, 0, 0, 0.45),
                inset -1px 0 1px rgba(0, 0, 0, 0.25),
                inset 0 0 50px rgba(255, 255, 255, 0.07),
                0 0 35px rgba(0, 255, 136, 0.15);
        }

        .game-card:hover::before {
            transform: translateX(130%) skewX(-6deg);
        }

        .game-card:hover::after {
            opacity: 1;
            background: radial-gradient(
                circle at 0% 0%,
                rgba(255, 255, 255, 0.4) 0%,
                rgba(255, 255, 255, 0.1) 25%,
                transparent 55%
            );
        }

        .game-title {
            position: relative;
            z-index: 2;
            font-size: 1.3rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-align: center;
            width: 100%;
            white-space: normal; 
            overflow-wrap: break-word; 
            line-height: 1.3;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.55), 0 0 12px rgba(0, 0, 0, 0.35);
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
            transition: all 0.25s ease;
            cursor: pointer;
            margin-top: auto;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }

        .game-card:hover .btn-launch {
            background-color: var(--accent-green);
            border-color: var(--accent-green);
            color: #000000;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.5);
        }

        /* --- LIQUID RESPONSIVE VIEWER --- */
        #play-view {
            display: none;
            position: fixed;
            top: 0; 
            left: 0; 
            width: 100vw; 
            height: 100vh;
            background-color: #000000;
            z-index: 500;
        }

        iframe {
            width: 100%;
            height: 100%;
            border: none;
            margin: 0;
            padding: 0;
            display: block;
        }

        #floating-escape-btn {
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
        }

        #floating-escape-btn:hover {
            opacity: 1;
            color: var(--accent-green);
            border-color: var(--accent-green);
            background-color: var(--panel-dark);
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.15);
            padding-bottom: 10px;
        }

        /* --- ESCAPE MENU MODAL OVERLAY --- */
        #pause-overlay {
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
        }

        .pause-box {
            background-color: var(--panel-dark);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 45px;
            text-align: center;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 0 40px rgba(0, 0, 0, 0.8);
        }

        .pause-box h1 {
            margin: 0 0 10px 0;
            color: #ffffff;
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: 2px;
        }

        .pause-box p {
            color: var(--text-muted);
            margin: 0 0 30px 0;
            font-weight: 600;
            font-size: 1rem;
        }

        .pause-btns {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .btn-menu {
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
        }

        .btn-menu:hover {
            border-color: var(--accent-green);
            background-color: rgba(0, 255, 136, 0.05);
            color: var(--accent-green);
        }

        .btn-quit {
            border-color: rgba(239, 68, 68, 0.3);
            color: #ef4444;
        }

        .btn-quit:hover {
            border-color: #ef4444;
            background-color: rgba(239, 68, 68, 0.1);
            color: #ef4444;
        }

        /* --- NEW UI ELEMENTS STYLING --- */
        .top-left-link {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 100;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 8px 16px;
            border-radius: 20px;
            color: var(--text-main);
            font-size: 0.85rem;
            font-weight: 700;
            text-decoration: none;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: all 0.25s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .top-left-link:hover {
            border-color: var(--accent-green);
            color: var(--accent-green);
            background: rgba(0, 255, 136, 0.08);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
        }

        .top-right-settings-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 100;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            width: 42px;
            height: 42px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            transition: all 0.25s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .top-right-settings-btn:hover {
            border-color: var(--accent-green);
            background: rgba(0, 255, 136, 0.08);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
        }

        .top-right-settings-btn svg {
            width: 20px;
            height: 20px;
            fill: var(--text-main);
            transition: fill 0.25s ease, transform 0.5s ease;
        }

        .top-right-settings-btn:hover svg {
            fill: var(--accent-green);
            transform: rotate(90deg);
        }

        /* Settings Modal & Sub-Directories / Tabs */
        #settings-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(5, 5, 5, 0.85);
            z-index: 1100;
            justify-content: center;
            align-items: center;
            backdrop-filter: blur(8px);
        }

        .settings-box {
            background-color: var(--panel-dark);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 30px;
            width: 90%;
            max-width: 560px;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
        }

        .settings-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 15px;
        }

        .settings-header h2 {
            margin: 0;
            font-size: 1.5rem;
            font-weight: 800;
            letter-spacing: 1px;
        }

        .settings-close {
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
            transition: color 0.2s ease;
        }

        .settings-close:hover {
            color: var(--text-main);
        }

        /* Settings Tabs Navigation */
        .settings-tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 12px;
        }

        .settings-tab-btn {
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .settings-tab-btn.active {
            background: rgba(0, 255, 136, 0.1);
            border-color: var(--accent-green);
            color: var(--accent-green);
        }

        .settings-tab-content {
            display: none;
            overflow-y: auto;
            flex-direction: column;
            gap: 20px;
            padding-right: 5px;
            max-height: 50vh;
        }

        .settings-tab-content.active {
            display: flex;
        }

        .settings-group {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 15px;
        }

        .settings-group-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--accent-green);
            margin-bottom: 12px;
            font-weight: 800;
        }

        .setting-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
        }

        .setting-item:not(:last-child) {
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            margin-bottom: 8px;
        }

        .setting-label {
            font-weight: 600;
            font-size: 0.9rem;
        }

        /* Analytics Tab Styles */
        .analytics-summary {
            display: flex;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 15px;
        }

        .analytics-metric {
            text-align: center;
            flex: 1;
        }

        .analytics-metric-value {
            font-size: 1.4rem;
            font-weight: 900;
            color: var(--accent-green);
            margin-top: 4px;
        }

        .analytics-metric-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Weekly Chart */
        .chart-container {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 15px;
        }

        .chart-title {
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 12px;
            color: var(--text-main);
        }

        .chart-bars {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            height: 120px;
            padding-top: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .chart-bar-col {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            height: 100%;
            justify-content: flex-end;
        }

        .chart-bar {
            width: 22px;
            background: var(--accent-green);
            border-radius: 4px 4px 0 0;
            transition: height 0.4s ease;
            min-height: 4px;
        }

        .chart-day-label {
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-top: 8px;
            font-weight: 600;
        }

        /* Play History List */
        .history-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .history-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 0.85rem;
        }

        .history-game-name {
            font-weight: 700;
        }

        .history-game-time {
            color: var(--text-muted);
            font-size: 0.8rem;
        }

        /* Accent Color Swatches */
        .color-swatches {
            display: flex;
            gap: 8px;
        }

        .swatch {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .swatch:hover {
            transform: scale(1.15);
        }

        .swatch.active {
            border-color: #ffffff;
            transform: scale(1.1);
        }

        /* iOS-style Switch Toggle */
        .switch {
            position: relative;
            display: inline-block;
            width: 46px;
            height: 24px;
        }

        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: #27272a;
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 18px;
            width: 18px;
            left: 2px;
            bottom: 2px;
            background-color: white;
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 50%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        input:checked + .slider {
            background-color: var(--accent-green);
        }

        input:checked + .slider:before {
            transform: translateX(22px);
        }

        /* High Contrast Mode Overrides */
        body.high-contrast {
            --bg-dark: #000000;
            --panel-dark: #111111;
            --text-main: #ffffff;
            --text-muted: #ffff00;
            --border-color: #ffffff;
        }
        body.high-contrast .game-card {
            background: #000000;
            border: 2px solid #ffffff;
            backdrop-filter: none;
            -webkit-backdrop-filter: none;
        }
        body.high-contrast .game-card:hover {
            border-color: var(--accent-green);
        }
        body.high-contrast .search-bar {
            background-color: #000000;
            border: 2px solid #ffffff;
            color: #ffffff;
        }

        /* Performance / Low-Spec Mode Overrides */
        body.performance-mode #dashboard-container {
            background: #050505 !important;
        }
        body.performance-mode .game-card {
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            background: #141416 !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
        }
        body.performance-mode .game-card::before,
        body.performance-mode .game-card::after {
            display: none !important;
        }
        body.performance-mode .search-bar {
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            background-color: #141416 !important;
        }
        body.performance-mode #pause-overlay,
        body.performance-mode #settings-modal {
            backdrop-filter: none !important;
            background-color: rgba(5, 5, 5, 0.98) !important;
        }

        /* FPS Overlay Style */
        #fps-overlay {
            display: none;
            position: absolute;
            top: 15px;
            left: 15px;
            color: #ffffff;
            font-family: monospace;
            font-size: 13px;
            font-weight: 700;
            background: rgba(0, 0, 0, 0.5);
            padding: 4px 8px;
            border-radius: 4px;
            pointer-events: none;
            z-index: 650;
            letter-spacing: 0.5px;
        }

        /* Global Mute Mask Style */
        .site-muted iframe {
            filter: grayscale(10%);
        }
    </style>
</head>
<body>

    <a href="https://www.youtube.com/channel/UCJNCidDM_s1lz9sKx80EQMw" target="_blank" class="top-left-link">Click Here To Visit My YouTube Channel</a>
    <div class="top-right-settings-btn" onclick="openSettingsModal()" title="Settings">
        <svg viewBox="0 0 24 24">
            <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.3L5.24,5.34c-0.22-0.08-0.47,0-0.59,0.22L2.73,8.88 C2.62,9.08,2.67,9.35,2.86,9.5l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
        </svg>
    </div>

    <!-- Settings Modal with Sub-Directories / Tabs -->
    <div id="settings-modal">
        <div class="settings-box">
            <div class="settings-header">
                <h2>Settings</h2>
                <button class="settings-close" onclick="closeSettingsModal()">&times;</button>
            </div>

            <!-- Tabs Header -->
            <div class="settings-tabs">
                <button class="settings-tab-btn active" onclick="switchSettingsTab('general', this)">General</button>
                <button class="settings-tab-btn" onclick="switchSettingsTab('analytics', this)">Playtime & History</button>
            </div>

            <!-- Tab 1: General Preferences -->
            <div id="tab-general" class="settings-tab-content active">
                <div class="settings-group">
                    <div class="settings-group-title">Appearance & Theme</div>
                    <div class="setting-item">
                        <span class="setting-label">Accent Color</span>
                        <div class="color-swatches">
                            <div class="swatch active" style="background-color: #00ff88;" onclick="setAccentColor('#00ff88', this)"></div>
                            <div class="swatch" style="background-color: #00b4ff;" onclick="setAccentColor('#00b4ff', this)"></div>
                            <div class="swatch" style="background-color: #7850ff;" onclick="setAccentColor('#7850ff', this)"></div>
                            <div class="swatch" style="background-color: #ff5096;" onclick="setAccentColor('#ff5096', this)"></div>
                            <div class="swatch" style="background-color: #ffb000;" onclick="setAccentColor('#ffb000', this)"></div>
                        </div>
                    </div>
                    <div class="setting-item">
                        <span class="setting-label">High Contrast Mode</span>
                        <label class="switch">
                            <input type="checkbox" id="high-contrast-toggle" onchange="toggleHighContrast(this)">
                            <span class="slider"></span>
                        </label>
                    </div>
                </div>

                <div class="settings-group">
                    <div class="settings-group-title">Performance & Monitoring</div>
                    <div class="setting-item">
                        <span class="setting-label">Performance Mode (Low-Spec)</span>
                        <label class="switch">
                            <input type="checkbox" id="performance-toggle" onchange="togglePerformanceMode(this)">
                            <span class="slider"></span>
                        </label>
                    </div>
                    <div class="setting-item">
                        <span class="setting-label">Overlay Framerate (FPS)</span>
                        <label class="switch">
                            <input type="checkbox" id="fps-toggle" onchange="toggleFpsSetting(this)">
                            <span class="slider"></span>
                        </label>
                    </div>
                </div>

                <div class="settings-group">
                    <div class="settings-group-title">Audio Controls</div>
                    <div class="setting-item">
                        <span class="setting-label">Global Mute Site-Wide</span>
                        <label class="switch">
                            <input type="checkbox" id="mute-toggle" onchange="toggleGlobalMute(this)">
                            <span class="slider"></span>
                        </label>
                    </div>
                </div>
            </div>

            <!-- Tab 2: Playtime & Analytics -->
            <div id="tab-analytics" class="settings-tab-content">
                <div class="analytics-summary">
                    <div class="analytics-metric">
                        <div class="analytics-metric-label">Total Time (7 Days)</div>
                        <div id="analytics-total-time" class="analytics-metric-value">0m</div>
                    </div>
                    <div class="analytics-metric">
                        <div class="analytics-metric-label">Games Played</div>
                        <div id="analytics-total-games" class="analytics-metric-value">0</div>
                    </div>
                </div>

                <div class="chart-container">
                    <div class="chart-title">Past Week Activity</div>
                    <div class="chart-bars" id="chart-bars-container">
                        <!-- Populated dynamically -->
                    </div>
                </div>

                <div class="settings-group">
                    <div class="settings-group-title">Recent Game History</div>
                    <div class="history-list" id="history-list-container">
                        <div style="color: var(--text-muted); font-size: 0.85rem; text-align: center; padding: 10px;">No games played yet this week.</div>
                    </div>
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
        const fpsToggle = document.getElementById('fps-toggle');
        const fpsOverlay = document.getElementById('fps-overlay');

        let isGameRunning = false;
        let showFps = false;
        let fpsInterval = null;

        // Analytics State Variables
        let currentGameName = '';
        let gameStartTime = 0;
        let sessionTimerInterval = null;

        // Load analytics data from localStorage or initialize
        let arcadeData = JSON.parse(localStorage.getItem('arcadeAnalytics')) || {
            weeklyMinutes: [0, 0, 0, 0, 0, 0, 0], // Sun - Sat
            history: [] // Array of { name, duration, date }
        };

        function openSettingsModal() {
            settingsModal.style.display = 'flex';
            updateAnalyticsUI();
        }

        function closeSettingsModal() {
            settingsModal.style.display = 'none';
        }

        function switchSettingsTab(tabName, btnElement) {
            document.querySelectorAll('.settings-tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.settings-tab-content').forEach(content => content.classList.remove('active'));

            btnElement.classList.add('active');
            document.getElementById('tab-' + tabName).classList.add('active');

            if (tabName === 'analytics') {
                updateAnalyticsUI();
            }
        }

        // --- Analytics & History Functions ---
        function recordPlayTime(gameName, secondsElapsed) {
            if (secondsElapsed <= 0) return;
            const minutesToAdd = secondsElapsed / 60;
            const todayIndex = new Date().getDay(); // 0 (Sun) to 6 (Sat)

            arcadeData.weeklyMinutes[todayIndex] += minutesToAdd;

            // Update or add to history
            const existingEntry = arcadeData.history.find(h => h.name === gameName);
            if (existingEntry) {
                existingEntry.duration += secondsElapsed;
                existingEntry.timestamp = Date.now();
            } else {
                arcadeData.history.unshift({
                    name: gameName,
                    duration: secondsElapsed,
                    timestamp: Date.now()
                });
            }

            // Keep history limited to last 10 entries
            if (arcadeData.history.length > 10) {
                arcadeData.history.pop();
            }

            localStorage.setItem('arcadeAnalytics', JSON.stringify(arcadeData));
        }

        function formatDuration(totalSeconds) {
            if (totalSeconds < 60) return `${Math.round(totalSeconds)}s`;
            const mins = Math.floor(totalSeconds / 60);
            if (mins < 60) return `${mins}m`;
            const hrs = (mins / 60).toFixed(1);
            return `${hrs}h`;
        }

        function updateAnalyticsUI() {
            // Total time calculation
            const totalMinutes = arcadeData.weeklyMinutes.reduce((a, b) => a + b, 0);
            document.getElementById('analytics-total-time').textContent = formatDuration(totalMinutes * 60);
            document.getElementById('analytics-total-games').textContent = arcadeData.history.length;

            // Render Weekly Bar Chart
            const chartContainer = document.getElementById('chart-bars-container');
            chartContainer.innerHTML = '';
            const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            const maxMins = Math.max(...arcadeData.weeklyMinutes, 1);

            arcadeData.weeklyMinutes.forEach((mins, idx) => {
                const heightPercent = Math.min(Math.max((mins / maxMins) * 100, 4), 100);
                
                const col = document.createElement('div');
                col.className = 'chart-bar-col';
                col.innerHTML = `
                    <div style="font-size: 0.65rem; color: var(--text-muted); margin-bottom: 4px;">${formatDuration(mins * 60)}</div>
                    <div class="chart-bar" style="height: ${heightPercent}%;"></div>
                    <div class="chart-day-label">${days[idx]}</div>
                `;
                chartContainer.appendChild(col);
            });

            // Render History List
            const historyContainer = document.getElementById('history-list-container');
            historyContainer.innerHTML = '';

            if (arcadeData.history.length === 0) {
                historyContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 0.85rem; text-align: center; padding: 10px;">No games played yet this week.</div>';
            } else {
                arcadeData.history.forEach(item => {
                    const row = document.createElement('div');
                    row.className = 'history-item';
                    row.innerHTML = `
                        <span class="history-game-name">${item.name}</span>
                        <span class="history-game-time">${formatDuration(item.duration)}</span>
                    `;
                    historyContainer.appendChild(row);
                });
            }
        }

        // --- Settings Implementation Functions ---
        function setAccentColor(colorHex, element) {
            document.documentElement.style.setProperty('--accent-green', colorHex);
            document.querySelectorAll('.swatch').forEach(sw => sw.classList.remove('active'));
            element.classList.add('active');
        }

        function toggleHighContrast(checkbox) {
            if (checkbox.checked) {
                document.body.classList.add('high-contrast');
            } else {
                document.body.classList.remove('high-contrast');
            }
        }

        function togglePerformanceMode(checkbox) {
            if (checkbox.checked) {
                document.body.classList.add('performance-mode');
            } else {
                document.body.classList.remove('performance-mode');
            }
        }

        function toggleGlobalMute(checkbox) {
            if (checkbox.checked) {
                document.body.classList.add('site-muted');
                muteAllAudioElements(true);
            } else {
                document.body.classList.remove('site-muted');
                muteAllAudioElements(false);
            }
        }

        function muteAllAudioElements(mute) {
            const mediaEls = document.querySelectorAll('audio, video');
            mediaEls.forEach(el => el.muted = mute);

            try {
                if (iframe && iframe.contentWindow) {
                    const iframeMedia = iframe.contentWindow.document.querySelectorAll('audio, video');
                    iframeMedia.forEach(el => el.muted = mute);
                }
            } catch (e) {}
        }

        function toggleFpsSetting(checkbox) {
            showFps = checkbox.checked;
            if (isGameRunning) {
                updateFpsVisibility();
            }
        }

        function updateFpsVisibility() {
            if (isGameRunning && showFps) {
                fpsOverlay.style.display = 'block';
                startFpsCounter();
            } else {
                fpsOverlay.style.display = 'none';
                stopFpsCounter();
            }
        }

        function startFpsCounter() {
            stopFpsCounter();
            let frameCount = 0;
            let lastTime = performance.now();

            function measureFps(currentTime) {
                frameCount++;
                if (currentTime - lastTime >= 1000) {
                    let fps = Math.round((frameCount * 1000) / (currentTime - lastTime));
                    fpsOverlay.textContent = `FPS: ${fps}`;
                    frameCount = 0;
                    lastTime = currentTime;
                }
                if (isGameRunning && showFps) {
                    fpsInterval = requestAnimationFrame(measureFps);
                }
            }
            fpsInterval = requestAnimationFrame(measureFps);
        }

        function stopFpsCounter() {
            if (fpsInterval) {
                cancelAnimationFrame(fpsInterval);
                fpsInterval = null;
            }
        }

        // --- Client-Side Search Processing Engine ---
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
            updateFpsVisibility();

            // Track playtime start
            currentGameName = gameTitle;
            gameStartTime = Date.now();
            if (sessionTimerInterval) clearInterval(sessionTimerInterval);
            sessionTimerInterval = setInterval(() => {
                // Periodic background record every 30 seconds of active play
                const elapsedSec = (Date.now() - gameStartTime) / 1000;
                if (elapsedSec >= 30) {
                    recordPlayTime(currentGameName, 30);
                    gameStartTime = Date.now();
                }
            }, 30000);

            if (document.getElementById('mute-toggle').checked) {
                setTimeout(() => muteAllAudioElements(true), 500);
            }
            
            setTimeout(() => {
                iframe.focus();
            }, 100);
        }

        function openPauseMenu() {
            if (isGameRunning) {
                pauseOverlay.style.display = 'flex';
            }
        }

        function resumeGame() {
            pauseOverlay.style.display = 'none';
            iframe.focus();
        }

        function exitToHub() {
            // Save remaining playtime before closing session
            if (isGameRunning && gameStartTime) {
                const elapsedSec = (Date.now() - gameStartTime) / 1000;
                recordPlayTime(currentGameName, elapsedSec);
                if (sessionTimerInterval) clearInterval(sessionTimerInterval);
            }

            iframe.src = ""; 
            pauseOverlay.style.display = 'none';
            playView.style.display = 'none';
            dashboardContainer.style.display = 'flex';
            isGameRunning = false;
            updateFpsVisibility();
            
            setTimeout(() => {
                searchBar.focus();
            }, 50);
        }

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isGameRunning) {
                if (pauseOverlay.style.display === 'flex') {
                    resumeGame();
                } else {
                    openPauseMenu();
                }
            }
        });
    </script>

</body>
</html>
"""

    # Inject the generated game cards securely
    full_html_content = html_template.replace('__CARDS_PLACEHOLDER__', all_cards_string)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html_content)
    
    print(f"Arcade sync successful! Added Playtime Analytics & History tab with weekly charts.")

if __name__ == '__main__':
    generate_arcade()
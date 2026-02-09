# Simplified Web Interface for PicoTamachibi
# Memory-efficient version with minimal HTML

import socket

class WebInterface:
    def __init__(self, oled, gamestate):
        self.oled = oled
        self.gamestate = gamestate
        self.server_socket = None
        self.running = False
        
    def start(self, port=8082):
        """Start the web server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', port))
            self.server_socket.listen(1)
            self.server_socket.settimeout(0.1)
            self.running = True
            print(f"Web server started on port {port}")
            return True
        except Exception as e:
            print(f"Failed to start web server: {e}")
            return False
    
    def stop(self):
        """Stop the web server"""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None
        print("Web server stopped")
    
    def handle_request(self):
        """Handle incoming HTTP requests (non-blocking)"""
        if not self.running or not self.server_socket:
            return
        
        try:
            conn, addr = self.server_socket.accept()
            conn.settimeout(1.0)
            
            # Read request
            request = conn.recv(512).decode('utf-8')
            
            # Parse request line
            lines = request.split('\r\n')
            if len(lines) > 0:
                parts = lines[0].split(' ')
                
                if len(parts) >= 2:
                    method = parts[0]
                    path = parts[1]
                    
                    # Route the request
                    if method == 'GET':
                        if path == '/' or path == '/index.html':
                            self.serve_html(conn)
                        elif path == '/status':
                            self.serve_status(conn)
                        else:
                            self.serve_404(conn)
                    elif method == 'POST':
                        if path.startswith('/action/'):
                            action = path.split('/')[-1]
                            self.handle_action(conn, action)
                        elif path.startswith('/button/'):
                            button = path.split('/')[-1]
                            self.handle_button(conn, button)
            
            conn.close()
            
        except OSError:
            pass
        except Exception as e:
            print(f"Error handling request: {e}")
    
    def serve_html(self, conn):
        """Serve minimal HTML interface"""
        html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>PicoTamachibi</title><style>
body{font-family:Arial;background:#1a1a1a;color:#fff;text-align:center;padding:20px;margin:0}
.stat{background:#2a2a2a;padding:15px;border-radius:8px;margin:10px;display:inline-block;min-width:80px}
.stat-value{font-size:1.8em;font-weight:bold;color:#4CAF50}
button{background:#4CAF50;color:white;border:none;padding:15px 30px;font-size:1.1em;
border-radius:8px;cursor:pointer;margin:5px;min-width:100px}
button:active{transform:scale(0.95)}
.btn-feed{background:#FF9800}.btn-sleep{background:#2196F3}.btn-clean{background:#9C27B0}
.alert{background:#f44336;padding:10px;border-radius:8px;margin:10px;font-weight:bold}
</style></head><body>
<h1>🐾 PicoTamachibi 🐾</h1>
<div id="stats"></div>
<div id="alert"></div>
<div><button class="btn-feed" onclick="sendAction('feed')">🍖 Feed</button>
<button class="btn-sleep" onclick="sendAction('sleep')" id="sleepBtn">💤 Sleep</button>
<button class="btn-clean" onclick="sendAction('clean')">🧹 Clean</button></div>
<div id="status" style="margin-top:20px">Loading...</div>
<script>
function update(){fetch('/status').then(r=>r.text()).then(d=>{
var stats=d;
document.getElementById('stats').innerHTML=stats;
document.getElementById('status').textContent='Connected';
var sleepBtn=document.getElementById('sleepBtn');
if(stats.includes('Sleeping')){sleepBtn.textContent='☀️ Wake';}
else{sleepBtn.textContent='💤 Sleep';}
}).catch(()=>document.getElementById('status').textContent='Disconnected');}
function sendAction(a){fetch('/action/'+a,{method:'POST'}).then(()=>setTimeout(update,500));}
update();setInterval(update,2000);
</script></body></html>"""
        
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html
        conn.send(response.encode('utf-8'))
    
    def serve_status(self, conn):
        """Serve pet status as HTML"""
        from time import time
        
        # Calculate age
        current_time = time()
        age_seconds = current_time - self.gamestate.states.get("pet_birth_time", current_time)
        age_days = age_seconds / (24 * 60 * 60)
        age_days_rounded = round(age_days * 2) / 2
        
        # Get pet name and type
        pet_name = self.gamestate.states.get('pet_name', 'Unknown')
        pet_type = self.gamestate.states.get('pet_type', 'Fox')
        
        # Determine current activity/state
        activity = "🦊 Idle"
        if self.gamestate.states.get('sleeping', False):
            activity = "� Sleeping"
        elif self.gamestate.states.get('feeding_time', False):
            activity = "🍖 Eating"
        elif self.gamestate.states.get('hide_seek_active', False):
            activity = "🎮 Playing Hide & Seek"
        elif self.gamestate.states.get('walking_active', False):
            direction = "→" if self.gamestate.states.get('walking_direction', 0) == 1 else "←"
            activity = f"🚶 Walking {direction}"
        elif self.gamestate.states.get('butterfly_active', False):
            activity = "🦋 Chasing Butterfly"
        elif self.gamestate.states.get('bunny_active', False):
            activity = "🐰 Watching Bunny"
        elif self.gamestate.states.get('birds_active', False):
            activity = "🐦 Watching Birds"
        elif self.gamestate.states.get('quick_nap_active', False):
            activity = "😴 Quick Nap"
        elif self.gamestate.states.get('rain_active', False):
            activity = "🌧️ In the Rain"
        
        # Check if there's poop (health dropping indicates poop present)
        if self.gamestate.states.get('unwell', False):
            activity += " • 💩 Needs cleaning!"
        
        # Add position info
        position = self.gamestate.states.get('fox_position', 1)
        position_text = ["Left", "Center", "Right"][position]
        
        # Check if sleeping
        is_sleeping = self.gamestate.states.get('sleeping', False)
        sleep_status = "💤" if is_sleeping else ""
        
        # Get alert/message if any
        alert_html = ""
        if self.gamestate.states.get('alert', False):
            alert_reason = self.gamestate.states.get('alert_reason', 'Alert!')
            alert_html = f'<div class="alert">⚠️ {alert_reason}</div>'
        
        # Show last random message if no alert
        last_msg = self.gamestate.states.get('last_random_message', '')
        if last_msg and not alert_html:
            alert_html = f'<div style="background:#2a2a2a;padding:10px;border-radius:8px;margin:10px;font-size:0.9em">💭 {last_msg}</div>'
        
        # Build HTML stats
        html = f"""<div style="margin-bottom:10px;font-size:1.2em">{pet_name} the {pet_type} {sleep_status}</div>
<div style="background:#1a3a1a;padding:8px;border-radius:8px;margin:10px;font-size:1em">{activity} • {position_text}</div>
{alert_html}
<div class="stat"><div>Health</div><div class="stat-value">{int(self.gamestate.states.get('health', 0))}/10</div></div>
<div class="stat"><div>Happiness</div><div class="stat-value">{int(self.gamestate.states.get('happiness', 0))}/10</div></div>
<div class="stat"><div>Sleepiness</div><div class="stat-value">{int(self.gamestate.states.get('sleepiness', 0))}/10</div></div>
<div class="stat"><div>Age</div><div class="stat-value">{age_days_rounded:.1f}d</div></div>"""
        
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html
        conn.send(response.encode('utf-8'))
    
    def handle_action(self, conn, action):
        """Handle action from web interface (feed, sleep, clean)"""
        action_lower = action.lower()
        
        if action_lower == 'feed':
            # Trigger feeding
            self.gamestate.states['web_action_feed'] = True
            print(f"Web action: Feed")
            response_data = 'OK - Feeding'
        elif action_lower == 'sleep':
            # Trigger sleep
            self.gamestate.states['web_action_sleep'] = True
            print(f"Web action: Sleep")
            response_data = 'OK - Sleeping'
        elif action_lower == 'clean':
            # Trigger cleaning
            self.gamestate.states['web_action_clean'] = True
            print(f"Web action: Clean")
            response_data = 'OK - Cleaning'
        else:
            response_data = 'ERROR - Unknown action'
        
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n' + response_data
        conn.send(response.encode('utf-8'))
    
    def handle_button(self, conn, button):
        """Handle button press from web interface"""
        button_upper = button.upper()
        if button_upper in ['A', 'B', 'X']:
            self.gamestate.states[f'web_button_{button_upper}'] = True
            print(f"Web button pressed: {button_upper}")
            response_data = 'OK'
        else:
            response_data = 'ERROR'
        
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n' + response_data
        conn.send(response.encode('utf-8'))
    
    def serve_404(self, conn):
        """Serve 404 error"""
        html = '<html><body><h1>404 Not Found</h1></body></html>'
        response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n' + html
        conn.send(response.encode('utf-8'))

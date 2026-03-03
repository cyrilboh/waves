from http.server import HTTPServer, BaseHTTPRequestHandler

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Drink Up! 🍺</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Segoe UI', sans-serif;
    background: #1a1a2e;
    color: #eee;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .screen { display: none; width: 100%; max-width: 600px; padding: 20px; }
  .screen.active { display: block; }

  h1 { font-size: 2.8rem; text-align: center; margin-bottom: 8px; }
  h2 { font-size: 1.6rem; text-align: center; margin-bottom: 20px; color: #f5a623; }
  .subtitle { text-align: center; color: #aaa; margin-bottom: 30px; font-size: 1rem; }

  .card {
    background: #16213e;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
    border: 1px solid #0f3460;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
  }

  input[type="text"] {
    width: 100%;
    padding: 12px 16px;
    border-radius: 10px;
    border: 2px solid #0f3460;
    background: #0f3460;
    color: #fff;
    font-size: 1rem;
    margin-bottom: 12px;
    outline: none;
    transition: border-color 0.2s;
  }
  input[type="text"]:focus { border-color: #f5a623; }
  input[type="text"]::placeholder { color: #666; }

  .btn {
    display: block;
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: none;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: transform 0.1s, opacity 0.2s;
    margin-bottom: 12px;
    letter-spacing: 0.5px;
  }
  .btn:active { transform: scale(0.97); }
  .btn-primary   { background: linear-gradient(135deg, #f5a623, #e07b00); color: #1a1a2e; }
  .btn-secondary { background: linear-gradient(135deg, #533483, #7b2ff7); color: #fff; }
  .btn-danger    { background: linear-gradient(135deg, #e04040, #a01010); color: #fff; }
  .btn-green     { background: linear-gradient(135deg, #20bf55, #01baef); color: #1a1a2e; }
  .btn-small {
    display: inline-block;
    width: auto;
    padding: 6px 14px;
    font-size: 0.85rem;
    margin: 0 4px;
    border-radius: 8px;
  }

  /* Mode grid */
  .mode-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .mode-btn {
    background: #0f3460;
    border: 2px solid transparent;
    border-radius: 14px;
    padding: 20px 10px;
    cursor: pointer;
    text-align: center;
    transition: border-color 0.2s, background 0.2s;
    color: #eee;
  }
  .mode-btn:hover { border-color: #f5a623; background: #1a4080; }
  .mode-btn .icon { font-size: 2.2rem; margin-bottom: 8px; }
  .mode-btn .label { font-size: 0.95rem; font-weight: 600; }

  /* Players bar */
  .players-bar {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    justify-content: center;
  }
  .player-chip {
    flex: 1;
    text-align: center;
    background: #0f3460;
    border-radius: 12px;
    padding: 10px 6px;
    border: 2px solid transparent;
    transition: border-color 0.2s;
    min-width: 0;
  }
  .player-chip.active-player { border-color: #f5a623; background: #1a4080; }
  .player-chip .pname { font-size: 0.85rem; font-weight: 700; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .player-chip .drinks { font-size: 1.5rem; }
  .player-chip .drink-label { font-size: 0.7rem; color: #aaa; }

  /* Challenge card */
  .challenge-box {
    background: #0f3460;
    border-radius: 14px;
    padding: 28px 20px;
    text-align: center;
    margin-bottom: 20px;
    min-height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  }
  .challenge-tag {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #f5a623;
    margin-bottom: 10px;
  }
  .challenge-text {
    font-size: 1.25rem;
    line-height: 1.5;
    font-weight: 500;
  }
  .turn-label {
    text-align: center;
    margin-bottom: 12px;
    font-size: 1rem;
    color: #aaa;
  }
  .turn-label span { color: #f5a623; font-weight: 700; }

  /* Score table */
  .score-table { width: 100%; border-collapse: collapse; }
  .score-table th, .score-table td {
    padding: 12px 16px;
    text-align: center;
    border-bottom: 1px solid #0f3460;
  }
  .score-table th { color: #f5a623; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; }
  .score-table .winner { color: #20bf55; font-weight: 700; }

  .badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; margin-left: 6px; background: #f5a623; color: #1a1a2e; }

  .flex-row { display: flex; gap: 10px; }
  .flex-row .btn { flex: 1; }
</style>
</head>
<body>

<!-- SCREEN 1: WELCOME -->
<div id="screen-welcome" class="screen active">
  <div class="card">
    <h1>🍺 Drink Up!</h1>
    <p class="subtitle">A drinking game for 3 brave friends</p>
    <label style="color:#aaa;font-size:0.9rem;display:block;margin-bottom:6px;">Player 1</label>
    <input type="text" id="p1" placeholder="Enter name..." maxlength="14">
    <label style="color:#aaa;font-size:0.9rem;display:block;margin-bottom:6px;">Player 2</label>
    <input type="text" id="p2" placeholder="Enter name..." maxlength="14">
    <label style="color:#aaa;font-size:0.9rem;display:block;margin-bottom:6px;">Player 3</label>
    <input type="text" id="p3" placeholder="Enter name..." maxlength="14">
    <button class="btn btn-primary" onclick="startGame()" style="margin-top:10px;">Let's Play! 🎉</button>
  </div>
</div>

<!-- SCREEN 2: MODE SELECT -->
<div id="screen-mode" class="screen">
  <h2>Pick a Game Mode</h2>
  <div id="players-bar-mode" class="players-bar"></div>
  <div class="mode-grid">
    <div class="mode-btn" onclick="playMode('truth')">
      <div class="icon">🤫</div>
      <div class="label">Truth or Dare</div>
    </div>
    <div class="mode-btn" onclick="playMode('never')">
      <div class="icon">🙅</div>
      <div class="label">Never Have I Ever</div>
    </div>
    <div class="mode-btn" onclick="playMode('would')">
      <div class="icon">🤔</div>
      <div class="label">Would You Rather</div>
    </div>
    <div class="mode-btn" onclick="playMode('hot')">
      <div class="icon">🔥</div>
      <div class="label">Hot Seat</div>
    </div>
  </div>
  <button class="btn btn-danger" onclick="showScores()" style="margin-top:16px;">📊 Scoreboard</button>
</div>

<!-- SCREEN 3: PLAY -->
<div id="screen-play" class="screen">
  <div id="players-bar-play" class="players-bar"></div>
  <div class="turn-label">It's <span id="current-player-name"></span>'s turn!</div>
  <div class="challenge-box">
    <div class="challenge-tag" id="challenge-tag"></div>
    <div class="challenge-text" id="challenge-text">Press "Draw Card" to begin!</div>
  </div>
  <div class="flex-row">
    <button class="btn btn-primary" onclick="drawCard()">🃏 Draw Card</button>
    <button class="btn btn-danger" onclick="drinkUp()">🍺 Drink!</button>
  </div>
  <div class="flex-row" style="margin-top:0;">
    <button class="btn btn-secondary btn-small" onclick="goMode()">← Modes</button>
    <button class="btn btn-secondary btn-small" onclick="nextTurn()">Skip →</button>
  </div>
</div>

<!-- SCREEN 4: SCOREBOARD -->
<div id="screen-scores" class="screen">
  <h2>📊 Scoreboard</h2>
  <div class="card">
    <table class="score-table" id="score-table"></table>
  </div>
  <button class="btn btn-green" onclick="goMode()">Back to Game</button>
  <button class="btn btn-danger" onclick="resetGame()">🔄 New Game</button>
</div>

<script>
const MODES = {
  truth: {
    label: 'TRUTH OR DARE',
    cards: [
      "TRUTH: What's the most embarrassing thing that happened to you this year?",
      "DARE: Do your best impression of someone in this room.",
      "TRUTH: What's a secret you've never told anyone here?",
      "DARE: Let the group go through your camera roll for 30 seconds.",
      "TRUTH: Who in this room would you call first in a crisis?",
      "DARE: Text someone random from your contacts 'I think about you sometimes' — no context.",
      "TRUTH: What's the weirdest dream you've had recently?",
      "DARE: Speak only in questions for the next 2 rounds.",
      "TRUTH: What's something you've lied about to impress someone?",
      "DARE: Let the person to your left write something on your forehead with a marker.",
      "TRUTH: What's your most unpopular opinion?",
      "DARE: Do 10 push-ups or drink twice.",
      "TRUTH: What's the pettiest thing you've ever done?",
      "DARE: Show the group your most recent search history.",
      "TRUTH: Have you ever talked about someone in this room behind their back?",
      "DARE: Call someone and sing them Happy Birthday — wrong person is fine.",
    ]
  },
  never: {
    label: 'NEVER HAVE I EVER',
    cards: [
      "Never have I ever sent a text to the wrong person.",
      "Never have I ever pretended to be sick to skip something.",
      "Never have I ever cried at a commercial.",
      "Never have I ever fallen asleep in a public place.",
      "Never have I ever eaten food I dropped on the floor.",
      "Never have I ever stalked an ex on social media.",
      "Never have I ever lied about watching a show just to fit in.",
      "Never have I ever taken a selfie and then deleted it immediately.",
      "Never have I ever googled my own name.",
      "Never have I ever ordered food for delivery just because I didn't want to cook.",
      "Never have I ever pretended to understand a joke when I didn't.",
      "Never have I ever sent a risky message by accident.",
      "Never have I ever screenshot a conversation to show someone else.",
      "Never have I ever stayed up past 3am doing absolutely nothing useful.",
      "Never have I ever forgotten someone's name right after being introduced.",
    ]
  },
  would: {
    label: 'WOULD YOU RATHER',
    cards: [
      "Would you rather always speak in rhyme OR always sing instead of talking?",
      "Would you rather know how you'll die OR when you'll die?",
      "Would you rather lose all your photos OR all your contacts?",
      "Would you rather always be 10 minutes late OR always be 20 minutes early?",
      "Would you rather eat pizza for every meal OR never eat pizza again?",
      "Would you rather have a pause button or a rewind button for your life?",
      "Would you rather be famous but hated OR unknown but loved?",
      "Would you rather never use social media again OR never watch TV/Netflix again?",
      "Would you rather always know when someone is lying OR be able to get away with any lie?",
      "Would you rather fight 100 duck-sized horses OR 1 horse-sized duck?",
      "Would you rather be the funniest person in the room OR the smartest?",
      "Would you rather have no internet for a week OR no phone for a week?",
      "Would you rather live in the past OR in the future?",
      "Would you rather only whisper for a year OR only shout for a year?",
    ]
  },
  hot: {
    label: '🔥 HOT SEAT',
    cards: [
      "Everyone points to the player most likely to cry at a movie. That person drinks.",
      "Vote: who is most likely to end up on a reality TV show? They drink.",
      "The group picks the most dramatic person here. Drink up!",
      "Who would survive longest in a zombie apocalypse? Everyone else drinks.",
      "Most likely to accidentally reply-all to a company email? Drink.",
      "Who is the worst at keeping secrets? They take 2 sips.",
      "Who would be the last one to bed at a sleepover? They drink.",
      "Who is most likely to become a millionaire? Everyone else drinks (jealousy sips).",
      "Most likely to get lost in their own neighborhood? Drink.",
      "Who would be voted off the island first? They drink.",
      "Who gives the best advice? Everyone else drinks (you're not as wise).",
      "Who's most likely to start a fight over something trivial? They drink.",
      "Who is most likely to forget a birthday? 2 drinks.",
      "Who has the worst sense of direction? They drink.",
    ]
  }
};

const RULES = {
  truth:  'If you refuse a Truth, drink 2. If you refuse a Dare, drink 3.',
  never:  'If you HAVE done it, drink. Honesty required!',
  would:  'Pick one! Whoever picks the same as most loses and drinks.',
  hot:    'Group votes decide who drinks. Majority rules!',
};

let players = [];
let drinks  = [0, 0, 0];
let currentMode = 'truth';
let currentPlayer = 0;
let usedCards = {};

function show(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

function buildPlayersBar(containerId) {
  const bar = document.getElementById(containerId);
  bar.innerHTML = players.map((p, i) => `
    <div class="player-chip ${i === currentPlayer ? 'active-player' : ''}" id="chip-${containerId}-${i}">
      <div class="drinks">${'🍺'.repeat(Math.min(drinks[i], 5))}${drinks[i] > 5 ? '+' : ''}</div>
      <div class="pname">${p}</div>
      <div class="drink-label">${drinks[i]} drink${drinks[i] !== 1 ? 's' : ''}</div>
    </div>
  `).join('');
}

function refreshBars() {
  ['players-bar-mode','players-bar-play'].forEach(id => {
    if (document.getElementById(id)) buildPlayersBar(id);
  });
  document.getElementById('current-player-name').textContent = players[currentPlayer];
}

function startGame() {
  const vals = ['p1','p2','p3'].map(id => document.getElementById(id).value.trim());
  if (vals.some(v => !v)) { alert('Please enter all 3 player names!'); return; }
  players = vals;
  drinks  = [0, 0, 0];
  usedCards = {};
  currentPlayer = 0;
  MODES.truth.cards.forEach((_,i) => {/* reset usage */});
  buildPlayersBar('players-bar-mode');
  show('screen-mode');
}

function playMode(mode) {
  currentMode = mode;
  if (!usedCards[mode]) usedCards[mode] = new Set();
  refreshBars();
  document.getElementById('challenge-tag').textContent = '';
  document.getElementById('challenge-text').textContent = 'Press "Draw Card" to begin!';
  show('screen-play');
}

function drawCard() {
  const cards = MODES[currentMode].cards;
  const used  = usedCards[currentMode];
  let available = cards.map((_, i) => i).filter(i => !used.has(i));
  if (available.length === 0) {
    used.clear();
    available = cards.map((_, i) => i);
  }
  const idx = available[Math.floor(Math.random() * available.length)];
  used.add(idx);
  document.getElementById('challenge-tag').textContent = MODES[currentMode].label;
  document.getElementById('challenge-text').textContent = cards[idx];
}

function drinkUp() {
  drinks[currentPlayer]++;
  nextTurn();
}

function nextTurn() {
  currentPlayer = (currentPlayer + 1) % 3;
  refreshBars();
  document.getElementById('challenge-tag').textContent = '';
  document.getElementById('challenge-text').textContent = 'Press "Draw Card" to begin!';
}

function goMode() {
  buildPlayersBar('players-bar-mode');
  show('screen-mode');
}

function showScores() {
  const sorted = players.map((p, i) => ({ name: p, d: drinks[i] }))
                        .sort((a, b) => b.d - a.d);
  const maxD = sorted[0].d;
  const rows = sorted.map((p, rank) => `
    <tr>
      <td>${rank + 1}</td>
      <td class="${p.d === maxD && maxD > 0 ? 'winner' : ''}">${p.name}${p.d === maxD && maxD > 0 ? '<span class="badge">champ</span>' : ''}</td>
      <td>${p.d} 🍺</td>
    </tr>
  `).join('');
  document.getElementById('score-table').innerHTML = `
    <thead><tr><th>#</th><th>Player</th><th>Drinks</th></tr></thead>
    <tbody>${rows}</tbody>
  `;
  show('screen-scores');
}

function resetGame() {
  drinks = [0, 0, 0];
  usedCards = {};
  currentPlayer = 0;
  ['p1','p2','p3'].forEach(id => document.getElementById(id).value = '');
  show('screen-welcome');
}
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def log_message(self, format, *args):
        pass  # silence access logs


if __name__ == "__main__":
    print("Starting waves on port 8254")
    HTTPServer(("127.0.0.1", 8254), Handler).serve_forever()

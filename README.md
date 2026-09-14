# The Gift Economy

A simultaneous bidding card game for 3–6 players, about ten minutes.

Every round you bid for a prize by playing a number card. The catch is that the card
you play is not discarded — it goes to the player on your left and joins their hand.
Winning costs you your best card and hands it straight to a rival.

This repo holds a playable digital build and a printable paper prototype.

## Rules

Each player takes a set of cards numbered 1–7. That is their hand for the whole game.
Nine Prize cards, worth 1 through 9 points, are shuffled face down in the middle.

Each round:

1. **Bid.** Flip the top Prize. Everyone secretly plays one card face down, then all reveal at once.
2. **Cancel.** Any number played by more than one player is crossed out. The highest number still standing takes the Prize.
3. **Give.** Everyone passes the card they just played to the player on their left.

After all nine Prizes are gone, the most points wins.

### Why it works

High cards are better to hold and worse to spend. Playing a 1 loses the round on
purpose but clogs your neighbour's hand with junk, so dumping is a real move. And
because matching numbers cancel, the obvious bid is often the losing one — if two
people both slam their 7, a 5 takes the prize outright.

## What's here

| Path | What it is |
|---|---|
| `index.html` | Playable build. Single file, no dependencies, works offline. |
| `print/gift-economy-cards.pdf` | Four pages: rules sheet plus cards to cut out. |
| `print/make_cards.py` | Generates the PDF. Requires `reportlab`. |

### Playing the digital build

Open `index.html` in any browser, or serve it with GitHub Pages.

It has two modes:

- **Play** — set up a table of 3–6 seats, name the people and leave the rest as bots.
  Because bidding is secret, multiple people share one device through a pass-the-device
  handoff: the table blanks, one person reveals their own hand, bids, and the screen
  blanks again for the next. Every bid stays face down until the last person commits.
- **Balance** — runs up to 4000 full games between bots and reports what the rules
  actually produced. Sliders for hand size, round count and player count.

### Printing the paper version

Pages 1–3 cover a four-player game. Page 4 holds the Prize cards and a fifth hand.
Cut along the card borders and deal one colour per player.

## Design notes

Findings from the simulator at the default settings (7 cards, 9 rounds, 4 players,
1000 games). These are bot games, not human ones — treat them as directions of
change rather than truth.

- **Cancelling flips the winner in ~23% of rounds.** The rule earns the sentence it costs to teach.
- **~29% of bids are deliberate junk dumps.** The gift mechanic is a live decision, not just a tax on winners.
- **~16% of rounds end with every bid cancelled** and the prize binned. Even player counts are the
  worst case, because bids split into matching pairs easily. Three or five players run cleaner.
- **Last place averages 2.3 points against the winner's 18.4.** The widest open problem: someone
  can spend the whole game taking nothing home.

Known open questions, in priority order:

1. Give last place something to play for. Penalty cards, where the *lowest* unique number is
   stuck with a negative, are the obvious candidate — at the cost of a second resolution rule.
2. Decide whether dead prizes should carry over and stack into a bigger pot instead of being discarded.
3. Cards only ever flow one direction, so you can only ever punish your left-hand neighbour. At five
   or six players that is a kingmaking risk worth testing.

## Lineage

The cancel-on-tie auction comes from Alex Randolph's *Raj* (*Hol's der Geier*, 1988).
Passing your spent card to the player on your left is this game's own addition.

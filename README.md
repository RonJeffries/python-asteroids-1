# Asteroids Game

This is an asteroids game, written in Python using the pygame library. It is documented in a nearly infinite series of articles on [ronjeffries.com](https://ronjeffries.com/categories/asteroids/), along with a previous series of articles implementing the game in Codea Lua.

At this writing, the code is being extended to also host the game Space Invaders, in the same code base, to demonstrate the power and use of this particular implementation.

The game, as it stands now, implements Asteroids (and, depending on when you read this, Space Invaders) using an unusual design. Rather than the game being embedded in one or more "god objects", which understand the game's overall scheme and manage things like collisions, all the logic of the game is in the individual objects. We'll discuss that further.

All live game objects are kept in a general collection object, named Fleets. I often refer to that object as "the mix", and you could make a case that I should rename it. The Game has one instance of Fleets, and all the choreography is done by that instance.

## The Game Cycle

The Fleets instance runs the game cycle, which consists of sending a series of messages, once per game frame (1/60th of a second) to each game object in Fleets. For each message in the series, that message is sent to all the live objects before the next message is sent. The sequence is:

* `update` - this message is intended to allow the receiver to update its position or any other aspects that need to be updated on each frame.

* `begin_interactions` - informs each object that the interaction cycle is about to begin.

* `interact_with` - for each pair (a, b) of objects in the mix, send `a.interact_with(b)` and `b.interact_with(a)`. An object of class SomeClass is expected to implement `self.interact_with(other)` as `other.interact_with_someclass(self)`. This exchange is the essential "trick" to how the program works. Further details will be found below.

* `end_interactions` - sent after all the interactions are complete. The receiver can take any action desired at this point, based on what has happened during interactions.

* `tick` - a general purpose message, used variously, typically to increment timers and take timed actions.

* `draw` - an opportunity for a visible object to draw itself.

## The Game Objects

In the mix (the Fleets instance), there are visible game objects, like Asteroid, Ship, Missile. And there are invisible objects as well, such as ShipMaker and SaucerMaker. It is through the interaction of these objects that the playable behavior of the game emerges. Let's sketch how that happens.

## The Game Cycle

Suppose there are some Asteroid instances and a Ship instance in the mix. Asteroids just have a position on the screen, and a velocity, a constant vector in the direction they are moving. (Asteroids only move in straight lines). The Ship has access to the game's controls, implemented with keys on the keyboard. A game cycle might go like this:

### Update

The asteroids just update their position according to their velocity. The ship accesses its controls, and may adjust its angle of rotation, apply acceleration, or fire a Missile, which it does by giving the Missile a velocity and position near the Ship, and placing it in the mix. Missiles, if any exist, adjust their position according to their velocity. 

At this point, all objects have moved to their correct location for this frame (1/60th of a second).

### Begin Interactions

The Ship initializes a couple of counters, `asteroid_tally` and `missile_tally`, to zero. The asteroids and missiles ignore this message.

### Interact_with

Recall that for each pair of objects, first and second, of class, say, FirstClass and SecondClass, the game will send `interact_with` to each pair, passing the other as parameter, and the rule is that they will reflect that message, including their class name, so the result is that for each pair, two messages are sent:

~~~python
first.interact_with_secondclass(second)
second.interact_with_firstclass(first)
~~~

For example, each asteroid will receive `interact_with_ship(ship)`. It is the responsibility of the asteroid to determine whether it is colliding with the ship. If it isn't, nothing happens. If it is colliding, the asteroid either splits itself into two smaller asteroids, or, if it is already of the smallest size, just removes itself from the Fleets mix.

> This interaction implements the game behavior for the ship crashing into an asteroid. It's all right here. No larger object that decides what will happen. This is the essential character of this design.

Similarly, each asteroid will receive `interact_with_asteroid` for every other asteroid. Since asteroids do not mutually interact, this method just returns.

Finally, each asteroid will receive `interact_with_missile` for each missile currently in operation. The asteroid checks to see if the missile is colliding with it, and if it is, splits or dies as before.

Meanwhile, the ship will receive `interact_with_asteroid`, for each asteroid. It will check to see if it is colliding with the asteroid, and if so, will put an Explosion into the mix, and remove itself. The Explosion object just displays the cute ship explosion fragments.

### End Interactions

When all the pairwise interactions are complete, everyone who's still in the mix is sent `end_interactions`. At present, no object uses `end_interactions`, but it is used at least once in tests. 

### Tick

Then each object still in the mix is sent `tick`, which includes the time since last tick (about a sixtieth of a second). Asteroids ignore `tick`. Missiles tick their timer and remove themselves after the three second missile flight time. The Ship does two somewhat arcane things. It counts down its `hyperspace_timer`, because after going to hyperspace, you can't go again for a while. And the Ship also adjusts a `drop_in` value. When a ship is first created, there is a visual effect of dropping onto the screen, done by scaling it larger than usual and having it quickly get smaller, so that it appears to be dropping down.

### Draw

The asteroids, ship, and missiles draw themselves on the screen in their current positions.

If I've been clear enough, you should be able to see that this cycle of interaction allows the ship to maneuver, allows missiles to split or kill asteroids, and allows the ship to destroy itself by hitting an asteroid. So, you see, there is no single place in the game where the behavior is coded. Instead, each individual object manages its own behavior and the sum of those individual behaviors creates the game's overall behavior.

## Special, Invisible Objects

But what about scoring and free ships and new waves of asteroids and all the other rigmarole? This is also handled by individual objects in the fleets mix. Details can be found in the code, but here are some brief descriptions:

### ShipMaker

ShipMaker sits silently in the mix. On `begin_interactions`, it sets a flag saying that it has not seen the ship. on `interact_with_ship`, it sets the flag to say that it has seen the ship. And, in `tick`, it checks to see whether it has seen a ship. If not, it ticks its ship restoration timer and when that has expired, if another ship is available, it creates a new Ship and adds it to the fleets mix. The ship drops in and you get another go.

If there is no ship available, ShipMaker adds a GameOver instance to the mix and removes itself. GameOver displays the start/end screen. Meanwhile, asteroids continue to fly around, which makes up the "attract" screen.

> A fairly common behavior for objects in the mix is to use the `interact_with_` messages to make note that some other kind of object exists, and occasionally even to hold on to it. For example, ShipMaker is detected by ScoreKeeper, as we'll mention below.

### ScoreKeeper

ScoreKeeper sits silently in the mix. It only interacts with instances of Score, ShipMaker, and Signal.

When an asteroid is split by a ship missile, the active player receives a score. This is done by the Asteroid, which determines what the score should be and puts a Score instance, bearing that value, into the mix. When that object is seen by the ScoreKeeper, the ScoreKeeper adds that amount to the current player's score. Meanwhile, when the Score sees `interact_with_scorekeeper`, it knows that it has been seen and removes itself. 

The Signal is used to tell a ScoreKeeper which player is active. In a two player game, there are two ScoreKeepers in the mix, one for each player, and ShipMaker drops a Signal into the mix when it creates a ship, signalling which player is active.

ScoreKeeper also notices ShipMaker, and keeps a pointer to it, which it uses when drawing the score, to display the free ships remaining, because ShipMaker holds the free ship countdown. This is a an important aspect / pattern of interaction between different objects in the mix: notice a particular object and send it messages as needed.

## Cooperation creates the game

We see here some fairly simple, low-level cooperation between Asteroid, Ship, ShipMaker, Score, Signal, and ScoreKeeper that, among them, creates complex game behavior. 

> Asteroids emit Score objects. The active ScoreKeeper accumulates those scores. The ShipMaker uses Signal to say which ScoreKeeper should be active. Score and Signal just carry information and immediately destroy themselves.

But the Asteroid doesn't know about ScoreKeeper. It just knows that it is supposed to create a Score. Score doesn't really care about ScoreKeeper, it just removes itself on interacting with one. It could just as well ignore that and remove itself on `end_interactions` but it seems safer to be sure we have at least been near a ScoreKeeper. ScoreKeeper doesn't know about asteroids, it just accumulates Scores.

Everything in the game works like that. Individual objects know as little about others as possible. Even in the very rare case where an object does hold on to another for a while, it isn't created knowing that object, it finds out about it during interactions. 

### A curious result

I have found a curious result from this design. I find it quite easy to figure out a few little objects to make something happen. I'm currently in the process of creating Space Invaders by creating a few new objects, and I expect to have no difficulty and to need no changes to the other classes in the game.

But while it is easy to create an important interaction, it is not easy to see the game of Asteroids anywhere in the program, because it is not in the program code in one or a few places, as one might expect. Instead, the Asteroids game is an "emergent property" of the interaction of more than 15 classes.

## Exploration Advice

Should you choose to try to understand this code or to take a copy, here are some hints. If you do study the code, and certainly if you adopt it, please get in touch with me and tell me about your experience. No obligation but I'll appreciate it: I'm quite interested in people's reaction to this strange design.

### Classes to Consider

Game
: You'll find that there isn't much to Game. It basically creates some stuff and then does `coin.slug(fleets)`. Coin is somewhat interesting.

Coin
: At this writing, there are currently these "coins": `quarter`, `slug`, `two_player`, `no_asteroids`, and `invaders`. These are top-level functions. Each receives an instance of Fleets as its only parameter, and each appends a few object instances to the fleets.

: Since the game behavior is just the result of the objects in the fleets mix, each coin creates a different kind of game:

: The `slug` starts with a WaveMaker (which creates waves of asteroids) and a GameOver, plus the common elements SaucerMaker, ScoreKeepr, and Thumper. The result is a screen with the GameOver / startup info displayed, and asteroids sailing. Once in a while, the saucer appears.  We get the attract screen.

: The `quarter` starts with a WaveMaker and ShipMaker and the common elements. The game is not over, and the ShipMaker will, after a short delay, create a Ship. The game begins and plays as described above.

: `two_player` adds a second ScoreKeeper and a ShipMaker primed for a two-player game, plus the common elements. We get a two player game, with two scores displayed.

: `no_asteroids` starts a game without the asteroids, which I use for testing saucer behavior. It also makes the game a lot easier, but it's difficult to score well with no asteroids. 

: `invaders`, incomplete at this writing, is the "coin" that starts a game of Space Invaders, by creating an entirely different mix.

Fleets
: A quick look at Fleets will show you that it allows for adding and removing objects from the mix, and will lead you to Interactor, which manages the interaction loop. Fleets contains the game cycle (`update`, `begin`, and so on).

Individual Flyers
: There are at least 15 subclasses of the Flyer interface, the interface for all objects that go into the mix. We've talked about many of them above. In each one you can see all the things with which it interacts and what it does about those interactions.

## Summary

You may be wondering about this design. I built it this way because I had an intuition that it would be interesting. I've built Asteroids in many different ways, and this one just seemed interesting. It's clearly not as efficient as it might be, if only because every asteroid interacts with every other asteroid and does nothing. But what fascinates me is that the game emerges from the collaboration of the individual little objects, which discover the situation as the game goes on.

I don't know that there is a "best design" for Asteroids. It would depend on your machine, your language, and many other variables. There may be no combination of those things where this would be the "best" design, but it is the most interesting version of Asteroids I've ever seen.
# Resources and development

Use this reference when a stock, flow, exchange or acquired capability changes
an actor's plans. Work with the game's native sheet, rules, configuration or
save; the representations below are examples, not a required data format.

## Contents

- [Build the enabling chain](#build-the-enabling-chain)
- [Choose a change by its consequence](#choose-a-change-by-its-consequence)
- [Worked economy: the ferry workshop](#worked-economy-the-ferry-workshop)
- [Separate a random wait from a promise](#separate-a-random-wait-from-a-promise)
- [Follow storage and intermediation](#follow-storage-and-intermediation)
- [Make an acquisition change play](#make-an-acquisition-change-play)
- [Revise with an appropriate observation](#revise-with-an-appropriate-observation)
- [Source anchors](#source-anchors)

## Build the enabling chain

Start from the desired action and work backward to its prerequisites. Obtain
initial stocks, units, holders, source frequency, capacity, loss conditions,
action prices, dependencies, time of choosing the result, and the rule version.
For probability, obtain dependence between attempts, guarantees, resets and
whether the opportunity itself can be lost. For an existing system, inspect
the actual parameter consumed by the relevant operation.

| Operation | Required distinction | Question that changes a plan |
| --- | --- | --- |
| Create | A source adds a unit inside the accounting boundary | Can someone start without already owning the source? |
| Destroy | A unit leaves that boundary without a new holder inside it | Is this irreversible cost or an unrecorded recipient? |
| Convert | One unit type is consumed and another produced | What prerequisites, capacity or binding does the result acquire? |
| Transfer | The unit changes holder | Who can now authorize its use, and when? |
| Reserve | The unit exists but cannot be spent elsewhere | Who releases it after cancellation, failure or absence? |

For one unit type, write `next stock = stock + creation - destruction +
transfers in - transfers out`. Transfers cancel in the total only if both
holders are inside the boundary. Record wood-to-building conversion with two
units; adding wood and buildings into “wealth” needs a justified valuation.

A vote, trust, knowledge, access right and inventory item may need different
operations. Do not turn every relationship into interchangeable currency.
Dormans's resource-flow distinctions provide a useful formal vocabulary;
his SimWar discussion also limits what that economic abstraction establishes
about an implemented game's tactics and level design. [D11]

## Choose a change by its consequence

Offer a new rule with the choice it creates or removes. These are local design
options; none is a universal balance repair.

| Change | Construct | Follow the trade-off |
| --- | --- | --- |
| Endowment | A first-episode purchase set | Is a viable plan available before the first reward? |
| New source | An action, condition and payout | Time spent obtaining it, new loops and lost alternatives |
| Storage cap or decay | Capacity and overflow/decay disposition | Stockpiling versus forced use; who loses overflow |
| Diminishing production | A marginal output schedule | Whether another investment becomes viable |
| Upkeep | A recurring bill and nonpayment consequence | Whether past success becomes an obligation |
| Guarantee or exchange | A maximum failure run or substitute acquisition | Changed expected output and retained uncertainty |
| Shared control | A usable authorization rule | Flexibility, individual refusal and coordination work |

For compounding `next = (1 + r) * stock`, two positive stocks at the same
rate retain their ratio while their absolute gap grows. Inspect a threshold
that changes future production or blocks an opponent before concluding that
the formula creates an unavoidable winner. Accumulation can be the game's subject.

## Worked economy: the ferry workshop

This original paper model uses whole scrap units. Ava owns 4, Bo owns 3 and the
crew locker owns 5. Locker scrap may fund a crew repair after the treasurer
approves the named expense. There is no income during these three independent
comparisons; reset to the initial state each time.

| Operation | Ava | Bo | Locker | Total | Consequence |
| --- | ---: | ---: | ---: | ---: | --- |
| Ava contributes 2 to locker | 2 | 3 | 7 | 12 | Crew repair budget grows; nothing was destroyed |
| Ava burns 2 in a flare | 2 | 3 | 5 | 10 | Illumination costs scrap permanently |
| Ava reserves 2 for departure | 4, including 2 reserved | 3 | 5 | 12 | Ava can spend only 2 elsewhere until release |

Repair costs 6. A table of total wealth reports 12 and may suggest repair is
available. It is unavailable from the locker alone. The contribution makes it
affordable; authorization still determines whether it occurs. This is an
ownership and authority effect, not inflation.

Reset the locker to 4. A public salvage excursion yields 2 at its end, needs
no upfront scrap and takes one episode. Repair costs 6; a portable winch costs
4. After one excursion, the crew may repair and retain 0, buy the winch and
retain 2, or defer spending. Buying the winch immediately leaves three
excursions to reach repair from 0. A revised winch that yields one extra scrap
per excursion changes that route to two excursions: specify the production
effect explicitly.

Reproduce the arithmetic with Python 3's standard library. No package install
is needed; the output describes this model, not measured player behavior.

```python
from math import ceil

initial = {"ava": 4, "bo": 3, "locker": 5}
after_transfer = dict(initial)
after_transfer["ava"] -= 2
after_transfer["locker"] += 2
after_burn = dict(initial)
after_burn["ava"] -= 2
print(sum(initial.values()), sum(after_transfer.values()), sum(after_burn.values()))
print(ceil((6 - 4) / 2), ceil(6 / 2), ceil(6 / 3))
```

Output: `12 12 10`, then `1 3 2`. A neutral exchange is a legitimate control:
moving 3 scrap for 3 scrap creates no growth. A cycle that turns 2 scrap into
an item and sells it for 3 adds one scrap per completed cycle if the paying
source is unbounded. A merchant with a finite purse of 3 does not support
indefinitely repeated growth from those same transactions.

## Separate a random wait from a promise

Suppose an optional blueprint drops with independent probability 0.1 on each
completed excursion and no partial credit. Its first success time `T` has
`E[T] = 10`, but `P(T > n) = 0.9 ** n`. After ten excursions, about 34.87%
remain without it in the model; after thirty, about 4.24%. These are not
observations of a population.

To guarantee the blueprint by excursion 10, grant it then if the previous
nine failed. This gives `E[min(T, 10)]` of about 6.5132 excursions. Keeping
the original probability and adding a guarantee changes expected issuance.
Ten guaranteed fragments instead make the time predictable; trading fragments
changes ownership and social access. State what resets after a reward.

```python
from math import ceil, log

p, guarantee = 0.1, 10
print(f"still_missing_after_10={(1-p)**10:.6f}")
print(f"still_missing_after_30={(1-p)**30:.6f}")
print(f"mean_with_guarantee={sum((1-p)**k for k in range(guarantee)):.6f}")
print(f"attempts_for_95_percent={ceil(log(0.05)/log(1-p))}")
```

Output values: `0.348678`, `0.042391`, `6.513216`, `29`. “95 percent by 29”
is not an individual guarantee. A rare optional collection item may legitimately
retain this tail. If the blueprint is required for the next scheduled group
episode, design that access promise using its deadline and affected members.

## Follow storage and intermediation

Separate acquisition, later selection and execution. A stored specific recipe
differs from a generic balance that can buy any recipe later. Grinding Gear
Games described stored Harvest crafts and community-mediated trading in 2021;
3.19.0 changed acquisition to tradable lifeforce spent on a later craft choice.
This establishes a historical change in representation and timing, not current
rules or a universal market effect. [H21] [H22]

Construct this original chain:

1. Bo earns a nontransferable **repair voucher**. It repairs one ferry selected
   when used; his workshop accepts ferries owned by other members.
2. Ava lends her ferry to Bo. He consumes his voucher repairing her ferry.
3. Ava receives it and pays Bo 2 scrap under an allowed service agreement.

Banning voucher transfer did not prohibit this service. If repair must be
personal, specify that the target belongs to the voucher holder and decide
what ownership changes do to eligibility. If service trading is intended,
define custody, target selection, payment, failure, cancellation and return.
Atomic escrow and an informal breakable promise permit different risks.

For community access, inspect the group that can pool providers and
opportunities. A rare voucher per individual may be commonly obtainable
through a large network. Without network records, report a permitted path
and unknown prevalence; a communication channel does not establish frequency.

## Make an acquisition change play

Specify bearer, acquisition condition, change, application and remaining choice.
Separate account, character, crew, world and human learning. ArenaNet's 2015
Mastery announcement tied account acquisition to movement and other benefits;
this illustrates bearer and application, not an assurance that a new person
understands an inherited ability. [M15]

In the invented ferry episode, Bo earns the **winch** unlock by completing one
training salvage and spending 4 scrap. The next route offers these actions:

| State and action | Time | Cost | Remaining choice |
| --- | ---: | ---: | --- |
| No winch: carry cargo on ridge | 3 turns | 0 fuel | Slow and exposed on turn 2; preserves fuel |
| Winch equipped: lift across canal | 1 turn | 1 fuel | Fast; leaves less fuel for return |
| Winch owned but not equipped | Ridge route only | 0 fuel | Ownership alone does not add a usable action |

Give Bo the actual unlock and action description, then perform “lift across
canal,” deduct fuel and put cargo on the far bank. An unlock log checks
acquisition only. If the new route has no cost, risk or disadvantage, decide
whether it intentionally replaces the old route or erases a desired choice.
If Bo cannot identify where to use it, consult
[learning and help](../../game-information-design/references/learning-and-help.md).
Adding experience does not answer that difficulty.

Alternate progression can preserve an irreversible career, allow free loadout
changes, price respecs, offer a trial, award a witnessed title, or add access
without power. Construct the consequence; “horizontal” or “vertical” does not
settle compatibility or dominance.

## Revise with an appropriate observation

Inspect a reachable beginning and an affected later state, including a missing
expected unlock when legal. Bind simulated strategies to explicit policies and
their omissions. A single legal loop may establish that growth is possible;
it cannot establish that people will discover or use it at scale.

For observed flows retain units, holder, operation meaning, build, cohort and
missing events. Use the shared
[environment contracts](../../game-design/references/environment-contracts.md)
for operations and evidence. If the rule changes repeated loss or changes its
holder at a boundary, continue through [loss](loss-and-continuation.md) or
[state transfer](game-state-transfer.md).

## Source anchors

- [D11] Joris Dormans, *Simulating Mechanics to Study Emergence in Games*,
  AIIDE 2011, “Four Economic Functions,” “Modeling SimWar” and “Discussion.”
  [Primary paper](https://ojs.aaai.org/index.php/AIIDE/article/download/12477/12336/16005).
- [H21] Grinding Gear Games, *Development Manifesto: Harvest Crafting*, 2021,
  stored crafts and community trading. [Primary post](https://www.pathofexile.com/forum/view-thread/3069670).
- [H22] Grinding Gear Games, *Content Update 3.19.0*, 2022, Harvest changes.
  [Primary patch notes](https://www.pathofexile.com/forum/view-thread/3293287).
- [M15] Crystin Cox and Nellie Hughes / ArenaNet, *Reimagining Progression:
  The Mastery System*, 2015-02-05. [Primary announcement](https://www.guildwars2.com/en/news/reimagining-progression-the-mastery-system/).

Procedures and examples are local design transfers. Sources support the stated
distinctions and historical cases, not the effectiveness of this skill or the
appeal of the invented game.

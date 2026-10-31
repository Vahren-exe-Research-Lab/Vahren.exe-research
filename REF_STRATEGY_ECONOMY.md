# Strategy, education, merchant and defense — curated C/T016/T025–T029

Scope: original ver0.67 normalized DAT STATIC-SCRIPT; unconfirmed native side effects and observable gameplay VERIFY. Golden PASS=0, strict MATCH=0. This is a cross-domain AI entrypoint, not new C-owner READY.
Primary sources: data/T016_GAMEPLAY_SYSTEMS.md, data/T025_STRATEGIC_PROGRESSION.md, data/T026_EDUCATION_MATRIX.md, data/T027_MERCHANT_PRICE_PURCHASE.md, data/T029_DEFENSE_RESEARCH.md. Related timing: REF_RANDOM_EVENTS.md and REF_SCRIPT_VM_CONTEXT.md.

## 1. World economy and progress (T025)
- Source-level base polip increase is 5 + owned spot count, but master and nonmaster entry paths distribute the additions across event_end and World with distinct turn-local guards. Do not duplicate rewards under World reentry.
- Buying 20 polip costs 8000 power money (master) or 4000 personal money (nonmaster); selling 20 polip returns 4000/2000. Source exchange rates do not create a profitable immediate cycle.
- In random scenario, seihap rewards expansion only when territory count exceeds the previously recorded high-water value. Recovering previously lost spots up to that value does not grant new points. Other sources/state lifetimes remain VERIFY.

## 2. Education score bands and retained state (T026)
- 12 regular courses: allowed uses per turn = 2 +(ownedSpots>10) +(ownedSpots>20), at most one per course per turn, normally cost 5 polip on success. Score baseline 50 plus teacher/student, stat-difference, location and history modifiers; not a universal random success rate.
- Shared score growth bands are <25 / 25..49 / 50..74 / >=75 but stat increases, unlocks and thresholds are course-specific. Tea main1 lacks an internal score reset yet its normal wrapper clears it; tea tournament is a separate entry path.
- Preserve source quirks: karate student branch reads teacher kmr; baseball move_up can remain uncleared for some score/student branches; with one remaining singing skill an index clamp may request the same skill twice. Variable persistence, addSkill duplicate effects and gameplay bugs are NOT confirmed.
- Verified normalized source SHA256: lecture.dat 8860A43913A7EC6BD70D3CD4E6531C764D592A13F5355635E958C191218B513C; ev10_baseball.dat B1F15E28F4E46C2914C3F7DB4C70B782B16E96E8E38167293F336CCEE72DE53D.

## 3. Merchant staged integer pricing, stock boundary (T027)
- item_price_fluctuation adds an optional random term first, then applies rate dependent on difficulty with randomev79 override priority. Each eligible inflation repetition and per-item/vendor/diplomacy factor does ordered integer multiplication/division; a 1-factor is skip sentinel, not simply 1x. The FamiMa-only random-event discount cannot be assigned to all merchants.
- Common purchase_item_base has a source guard hole for stock=5 and money exactly 5*positive item price: the five-item choice uses strict < while lower-quantity branches also fail, so no choice call is issued by that helper. Previous item_mer/item_stock lifetime and purchase result are VERIFY; do not “fix” comparator before reproducing.
- Verified source ev_M_famima.dat SHA256 D726042910CB5EA33D78D1DF9BE9CB08051AB5D41919B8284C7D4F01F8A37F41.

## 4. Castle and three-track defense research (T029)
- Castle strengthening price is set from actual player spot count at purchase, not the earlier temporary costcastle=1. Eligible owned spots get addCastle(+100) with value capped at 5000. Three research tracks use 5000/10000/20000 staged money costs and normally stop at Level3; residual Level4 source declarations need independent reachability checks.
- siege_politic and event_castleset have separate counters, entry gates and phases; siege_politic mode1/2/3 reset thresholds are 10/8/5 qualifying invocations, not necessarily literal turns. If poN and pooN variants coexist, NPC research slots and player display cache may diverge; actual mixed-runtime scenario is VERIFY.
- Verified source siege_politic.dat SHA256 362CB8553ACDB36F10E5939EDE977A3739AE24FDBF23501E209ED87A4FD255E5. Never consume denied/incomplete T030 production graph.

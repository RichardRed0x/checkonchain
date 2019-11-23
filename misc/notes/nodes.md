The main problem with UASF is that nodes which don't have the support of miners and economic nodes (exchanges, stores that accept that particular variant, etc) are worthless.  You can refuse to upgrade your node (which you can do in Decred too, btw), but what good is it when you can't transact because blocks aren't being mined (or are being mined with such low hash rates that it's highly vulnerable to attack), and exchanges and stores aren't accepting your rule set?  In effect, UASF is basically a big game of chicken.  It's like rioting in the street hoping the powers that be ultimately cave to your demands.  
It also is not tenable when there are multiple changes at play.  One change, maybe you can get enough people to riot.  Two changes?  Three changes?


Yet another problem is suffers from is fake signalling. It is exceedingly easy to fire up a bunch of nodes all signalling that they're in favor of some change. I can write a script to fire up more nodes than are collectively on the entire public BTC network right now and spend a few K in VPSes across the world to mask it (which is the network with the most public facing nodes last I checked at 9380 as of this moment) that make it appear like there is broad support for something, when there really isn't. Then, if the miners blink and upgrade, the rest are going to follow suit, because their chains will stop.



All of the new nodes would reject them, so old nodes are somewhat protected from that class of bug as long as they are also connected to some newer nodes.
However, if you can partition the victim off the network with a sybil attack, you can trick them into all kinds of nastiness (which happens with soft forks too).

old nodes would trust a new node = Soft forks. The old nodes have zero clue about the new rules.


Sybil attack in a SF is just creating lots of new nodes such that vulnerable node is in the minority. Thus you are tricking the old ones into invalidating false coins. BUT the flip side is that if a malicious actor was to spin up a load of 'old nodes' to exploit a bug, it could in theory trick all the 'honest old' nodes to supporting their truth. I suspect that would cause a natural chain split and then the miners would be picking a side. Theory is they would support the honest chain however that assumes that miners are honest. In the case of a nation state malicious actor, seems like its not actually as secure as the narrative says.



create a transaction that has a time lock (CLTV).  It is not yet valid on the newer nodes who enforce it, but, to the old nodes, it's a NOP opcode, and is perfectly valid.  So, I sybil your node and partition you from the network into nodes that I control all running the old rules.  Now, I send you some time locked coins for a big purchase.  Your wallet shows the balance go up, they appear spendable and all is well.  You diligently wait for 144 confirmations (roughly 1 day). because this is a big sum, and you want to be positive to wait for what should be enough more than enough as reorgs that big or near impossible.  You believe everything is great.  So, you release the merchandise.  Now, you try to spend those coins and your transactions get rejected because the time lock hasn't expired yet.
Much worse things can happen with something like the SegWit change, because those transactions are spendable by anyone under the old node rules.
# Project Journal

I made this project because I wanted one magnetic design that felt narrow enough to finish but rich enough to teach me something real.

The original curiosity was simple: mu-metal is usually introduced as shielding material, but what happens if I treat it as an active part of a switching mechanism instead? That question turned out to be better than I expected because it forced a few useful design judgments.

The first one was material honesty. It would have been easy to throw mu-metal everywhere and make the project sound more exotic. That would have made the design worse. Once I worked through the circuit, it became pretty clear that mu-metal is most useful here as a local shunt, while the broader return path should stay in a more ordinary soft magnetic material.

The second lesson was that geometry beats cleverness. The residual shunt gap ended up mattering more than almost anything else. That immediately changed the flavor of the project. It stopped being a vague "high permeability is good" exercise and became a problem about mechanical control, repeatability, and how much performance is actually worth chasing.

The optimization pass made that even clearer. The numerically best safe point in the current sweep is tighter and larger than the baseline, but I still prefer the baseline as the more believable first build. That is probably the most useful habit this project reinforced for me: not treating the best spreadsheet point as automatically the best design.

I also like that this repo has a complete shape now. There is a concept, a model, a sweep, a few visual explanations, and a clear list of what would come next. It feels less like a one-off calculation and more like the start of a proper experimental build.

If I come back to it, I want the next version to answer one practical question clearly: what does the sensor actually see, not just what does the center of the gap see? That is where simulation or bench measurements start to matter.

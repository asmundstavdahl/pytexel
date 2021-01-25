#!/bin/env python3

# %%
import pstats
p: pstats.Stats = pstats.Stats('profile')
p.strip_dirs().sort_stats("cumtime").print_stats()

# %%

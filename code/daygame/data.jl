# daygame datasets: [cumulative_approaches cumulative_events] per row

# Roy Walker
rw_lay  = [511 5; 901 10; 977 10; 1060 11; 1143 13; 1216 14; 1380 16; 1448 18; 1557 19;
           1990 27; 2063 27; 2130 27; 2230 27; 2373 31; 2540 35; 2876 44; 3442 62;
           3567 63; 3991 83; 4092 84]
rw_date = [511 19; 901 38; 977 38; 1060 40; 1143 46; 1216 48; 1380 58; 1448 63; 1557 64;
           1990 81; 2063 81; 2130 84; 2230 85; 2373 91; 2540 97; 2876 126; 3442 165;
           3567 170; 3991 200; 4092 202]

# Mr. White
mw_lay  = [700 13; 1212 25]
mw_date = [700 30; 1212 68]

# Thomas Crown
tc_lay  = [208 2; 1638 20; 2453 34; 3036 45]
tc_date = [208 12; 1638 79; 2453 116]

# Seven
s_lay  = [38 3; 176 4; 238 5; 318 8; 344 9; 367 11; 434 12; 478 13; 543 13;
          588 14; 663 15; 691 15; 752 17; 774 18; 853 20; 942 20; 1087 24]
s_date = [38 8; 174 11; 236 14; 318 21; 344 23; 367 26; 434 27; 478 27; 543 32;
          588 33; 663 36; 691 41; 752 44; 774 47; 853 53; 942 54; 1087 76]

# Krauser
k_lay  = [1000 27; 1480 50; 2150 65]
k_date = [1000 60; 1480 110; 2150 160]

# Mr. Wolfe — each row = exactly 1 new lay → counting rows gives cumulative lays
w_lay  = [39 1; 200 2; 396 3; 584 4; 619 5; 678 6; 746 7; 825 8; 961 9; 1086 9;
          1122 9; 1174 10; 1220 11; 1267 11; 1317 12; 1322 12]
w_date = [445 11; 593 12; 700 14; 783 15; 858 19; 925 23; 1000 32; 1086 32;
          1122 32; 1174 35; 1220 37; 1267 37; 1317 39; 1322 39]

# Gringo Daygame — 1st dates only, explicit period-by-period tracking
gringo_lay  = [387 4; 624 5; 826 12; 898 13; 1036 15; 1256 19; 1555 21; 1803 28; 2000 31]
gringo_date = [387 16; 624 24; 826 47; 898 50; 1036 60; 1256 76; 1555 107; 1803 132; 2000 152]

# D.J. Caird — lay data solid; date totals estimated lower bounds
djcaird_lay  = [350 12; 415 13; 889 19; 1175 29; 1461 31]
djcaird_date = [1175 41; 1461 48]

# Smirking Soldier — reconstructed from bodycount page + individual posts
smirksoldier_lay  = [573 5; 643 7; 673 9; 723 10; 850 11; 932 13]
smirksoldier_date = [573 3; 643 3]

# Barry Burgle — dates include idates (not separated); still informative
barryburgle_lay  = [562 2; 1619 3; 2268 6; 2522 8]
barryburgle_date = [562 10; 1619 40; 2268 74; 2522 85]

# Brown Daygame
browndaygame_lay  = [150 1; 204 2; 281 3; 372 4]
browndaygame_date = [150 2; 204 2; 281 9; 372 15]

# Coffee Daygame — lay data ok; date weak (only 2 anchored points)
coffeedaygame_lay  = [431 1; 850 1; 1170 11; 1400 15; 1415 16]
coffeedaygame_date = [1170 19; 1400 33]

# Viking Flaneur — 0 lays 2017-2020 (stopped trying); truncated to pre-plateau
vikingflaneur_lay  = [1010 4; 1550 6]
vikingflaneur_date = [1010 12; 1550 18; 1688 22; 1786 25; 1884 28]

# Mr. B — single anchor
mrb_lay  = [1700 6]
mrb_date = [1700 19]

# Pink Panther PUA — 4-year gap 2019-2022 with unknown approaches; treat as unreliable
pinkpanther_lay  = [500 2; 758 3; 867 3]
pinkpanther_date = [500 10; 758 14; 867 14]

# Garret Forward — sparse: 1 lay point, 2 date points, ~2 months of travel only
garret_lay  = [50 1]
garret_date = [40 0; 50 3]

# Jax — only lay #1 anchored (~100 approaches, casual statement)
jax_lay = [100 1]

# theplayerway (puamindset) — 8 approaches, 1 lay; essentially a toy datapoint
playerway_lay  = [8 1]
playerway_date = [8 1]

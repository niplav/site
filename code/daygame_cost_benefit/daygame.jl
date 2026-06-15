# daygame ratio curve fitting
# port of data.kg + load.kg (sigmoid fit only) + new blog data
#
# deps: Plots, Optim
# run:  julia daygame.jl

using Plots
using Optim

gr()

# ============================================================
# Data — [cumulative_approaches cumulative_events] per row
# ============================================================

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

# ============================================================
# Ratio helpers
# ============================================================

ratio_pts(data) = (Float64.(data[:, 1]), data[:, 2] ./ data[:, 1])

# Dense running ratio for Wolfe (relies on each row = 1 new lay)
wolfe_lay_dense(xs) = [count(w_lay[:, 1] .< x) / x for x in xs]

# ============================================================
# Sigmoid fit
# ============================================================

shrunk_logistic(x, slope, intercept, ceiling) =
    ceiling / (1 + exp(intercept + slope * x))

function fit_ratio(datasets; ceiling_bound)
    all_data = vcat(datasets...)
    xs = Float64.(all_data[:, 1])
    ys = all_data[:, 2] ./ xs
    f(p) = sum((shrunk_logistic.(xs, p[1], p[2], p[3]) .- ys).^2)
    r = optimize(f, Fminbox(LBFGS()),
                 [-1e-2, 0.0, 0.0], [0.0, 10.0, ceiling_bound],
                 [LAY_SLOPE, LAY_INTERCEPT, ceiling_bound * 0.9])
    Optim.minimizer(r)
end

# Pre-fitted parameters (original scipy run on rw/tc/w; rerun fit_ratio() to update)
const LAY_SLOPE     = -0.00032469342601662376
const LAY_INTERCEPT =  1.0921062524727312
const LAY_CEIL      =  0.032999999999999995

const DATE_SLOPE     = -0.00032682619283946467
const DATE_INTERCEPT =  0.4249112313623176
const DATE_CEIL      =  0.06999999999999999

layratio(x)  = shrunk_logistic(x, LAY_SLOPE,  LAY_INTERCEPT,  LAY_CEIL)
dateratio(x) = shrunk_logistic(x, DATE_SLOPE, DATE_INTERCEPT, DATE_CEIL)

# ============================================================
# Dataset registry — controls plotting and curve-fitting
#
# Each entry: (data_matrix, color, label, in_lay_fit, in_date_fit)
# Toggle the booleans to include/exclude from fit and plot.
# ============================================================

const C_RW       = RGB(0.109, 0.847, 0.588)
const C_RW_D     = RGB(0.147, 0.468, 0.354)
const C_SEVEN    = RGB(0.8,   0.8,   0.1)
const C_MWH      = RGB(0.4,   0.4,   1.0)
const C_TC       = RGB(0.7,   0.2,   0.7)
const C_TC_D     = RGB(0.5,   0.1,   0.5)
const C_KR       = RGB(1.0,   0.0,   0.0)
const C_WF       = RGB(1.0,   0.65,  0.1)
const C_WF_D     = RGB(0.8,   0.55,  0.05)
const C_GRINGO   = RGB(0.2,   0.7,   0.9)
const C_DJCAIRD  = RGB(0.9,   0.4,   0.1)
const C_SMIRK    = RGB(0.5,   0.5,   0.5)
const C_BARRY    = RGB(0.6,   0.9,   0.3)
const C_BROWN    = RGB(0.85,  0.5,   0.2)
const C_COFFEE   = RGB(0.55,  0.27,  0.07)
const C_VIKING   = RGB(0.1,   0.3,   0.7)
const C_MRB      = RGB(0.7,   0.1,   0.5)
const C_PINK     = RGB(1.0,   0.5,   0.7)
const C_GARRET   = RGB(0.3,   0.8,   0.5)
const C_JAX      = RGB(0.6,   0.2,   0.8)
const C_PLAYER   = RGB(0.4,   0.6,   0.2)

# (lay_data, color, label, in_lay_fit)
LAY_DATASETS = [
    (rw_lay,            C_RW,      "Roy Walker",      true),
    (mw_lay,            C_MWH,     "Mr. White",       true),
    (tc_lay,            C_TC,      "Thomas Crown",    true),
    (s_lay,             C_SEVEN,   "Seven",           true),
    (k_lay,             C_KR,      "Krauser",         true),
    # Wolfe handled separately (dense)
    (gringo_lay,        C_GRINGO,  "Gringo",          true),
    (djcaird_lay,       C_DJCAIRD, "DJ Caird",        true),
    (smirksoldier_lay,  C_SMIRK,   "Smirk. Soldier",  true),
    (barryburgle_lay,   C_BARRY,   "Barry Burgle",    true),
    (browndaygame_lay,  C_BROWN,   "Brown DG",        true),
    (coffeedaygame_lay, C_COFFEE,  "Coffee DG",       true),
    (vikingflaneur_lay, C_VIKING,  "Viking Flaneur",  false),  # pre-plateau only, don't fit
    (mrb_lay,           C_MRB,     "Mr. B",           true),
    (pinkpanther_lay,   C_PINK,    "Pink Panther",    false),  # 4-year gap, don't fit
    (garret_lay,        C_GARRET,  "Garret Forward",  false),  # too sparse
    (jax_lay,           C_JAX,     "Jax",             false),
    (playerway_lay,     C_PLAYER,  "theplayerway",    false),
]

# (date_data, color, label, in_date_fit)
DATE_DATASETS = [
    (rw_date,             C_RW_D,    "Roy Walker",      true),
    (mw_date,             C_MWH,     "Mr. White",       true),
    (tc_date,             C_TC_D,    "Thomas Crown",    true),
    (s_date,              C_SEVEN,   "Seven",           true),
    (k_date,              C_KR,      "Krauser",         true),
    (w_date,              C_WF_D,    "Mr. Wolfe",       true),
    (gringo_date,         C_GRINGO,  "Gringo",          true),
    (djcaird_date,        C_DJCAIRD, "DJ Caird",        true),
    (smirksoldier_date,   C_SMIRK,   "Smirk. Soldier",  false),  # only 2 pts, sparse
    (barryburgle_date,    C_BARRY,   "Barry Burgle",    false),   # includes idates
    (browndaygame_date,   C_BROWN,   "Brown DG",        true),
    (coffeedaygame_date,  C_COFFEE,  "Coffee DG",       true),
    (vikingflaneur_date,  C_VIKING,  "Viking Flaneur",  true),
    (mrb_date,            C_MRB,     "Mr. B",           true),
    (pinkpanther_date,    C_PINK,    "Pink Panther",    false),  # 4-year gap
    (garret_date,         C_GARRET,  "Garret Forward",  false),
    (playerway_date,      C_PLAYER,  "theplayerway",    false),
]

# ============================================================
# Plots
# ============================================================

line_ratio!(p, data, c; kw...) =
    plot!(p, ratio_pts(data)..., color=c, marker=:circle,
          markersize=4, markerstrokewidth=0, linewidth=1.5; kw...)

const MAX_APPR = 5000
const XS = 1:MAX_APPR

function plot_layratio(suffix; only_fit=false)
    datasets = only_fit ? filter(x -> x[4], LAY_DATASETS) : LAY_DATASETS
    p = plot(xlabel="Approaches", ylabel="Cumulative lay ratio",
             ylims=(0, 0.04), legend=:topleft, size=(900,600), dpi=150)
    plot!(p, XS, layratio.(XS), color=:black, linewidth=2, label="Fitted sigmoid")
    for (data, c, label, _) in datasets
        line_ratio!(p, data, c; label=label)
    end
    plot!(p, 1:67:1320, wolfe_lay_dense(1:67:1320),
          color=C_WF, marker=:circle, markersize=3, markerstrokewidth=0,
          linewidth=1.5, label="Mr. Wolfe")
    savefig(p, "layratio_data$(suffix).png")
end

function plot_dateratio(suffix; only_fit=false)
    datasets = only_fit ? filter(x -> x[4], DATE_DATASETS) : DATE_DATASETS
    p = plot(xlabel="Approaches", ylabel="Cumulative date ratio",
             ylims=(0, 0.08), legend=:topleft, size=(900,600), dpi=150)
    plot!(p, XS, dateratio.(XS), color=:black, linewidth=2, label="Fitted sigmoid")
    for (data, c, label, _) in datasets
        line_ratio!(p, data, c; label=label)
    end
    savefig(p, "dateratio_data$(suffix).png")
end

function plot_ratio(suffix; only_fit=false)
    lay_ds  = only_fit ? filter(x -> x[4], LAY_DATASETS)  : LAY_DATASETS
    date_ds = only_fit ? filter(x -> x[4], DATE_DATASETS) : DATE_DATASETS
    p = plot(xlabel="Approaches", ylabel="Cumulative ratios",
             ylims=(0, 0.08), legend=:topleft, size=(900,600), dpi=150)
    plot!(p, XS, layratio.(XS),  color=:black, linewidth=2, label="Lay fit")
    plot!(p, XS, dateratio.(XS), color=:blue,  linewidth=2, label="Date fit")
    for (data, c, label, _) in lay_ds
        line_ratio!(p, data, c; label=label)
    end
    plot!(p, 1:67:1320, wolfe_lay_dense(1:67:1320),
          color=C_WF, marker=:circle, markersize=3, markerstrokewidth=0,
          linewidth=1.5, label="Mr. Wolfe (lay)")
    for (data, c, label, _) in date_ds
        line_ratio!(p, data, c; label=label, marker=:diamond, linestyle=:dash)
    end
    savefig(p, "ratio_data$(suffix).png")
end

for (suffix, only_fit) in [("", false), ("_reduced", true)]
    plot_layratio(suffix; only_fit)
    plot_dateratio(suffix; only_fit)
    plot_ratio(suffix; only_fit)
    @info "plots$(suffix) done"
end

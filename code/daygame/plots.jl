# daygame ratio curve fitting
# port of data.kg + load.kg (sigmoid fit only) + new blog data
#
# deps: Plots, Optim
# run:  julia daygame.jl

using Plots
using Optim

gr()

include("data.jl")

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
             ylims=(0, 0.04), legend=:outertopright, size=(900,600), dpi=150)
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
             ylims=(0, 0.08), legend=:outertopright, size=(900,600), dpi=150)
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
             ylims=(0, 0.08), legend=:outertopright, size=(900,600), dpi=150)
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

using Distributions, Plots

x_normal=abs.(rand(Normal(0, 1), 1000))
y_normal=abs.(rand(Normal(0, 1), 1000))

x_lognormal=abs.(rand(LogNormal(0, 1), 1000))
y_lognormal=abs.(rand(LogNormal(0, 1), 1000))

p1=scatter(x_normal, y_normal, c=:blue, label="Both normally distributed", xlabel="Effectiveness", ylabel="Popularity")
p2=scatter(x_lognormal, y_lognormal, c=:red, label="Both lognormally distributed", xlabel="Effectiveness", ylabel="Popularity")

combined_plot=plot(p1, p2, size=(850, 450))

savefig(combined_plot, "tails.png")

p3=scatter(x_lognormal, y_normal, c=:yellow, size=(600, 600), label="Effectiveness lognormal, popularity normal", xlabel="Effectiveness", ylabel="Popularity")

savefig(p3, "different.png")

--curent age of the user of this script
curage=tonumber(arg[1]) and tonumber(arg[1]) or 20

--value of one year of life
val_year=tonumber(arg[2]) and tonumber(arg[2]) or 50000

--probability of cryonics success
prob_succ=tonumber(arg[3]) and tonumber(arg[3]) or 0.05

--probability of being preserved
prob_pres=tonumber(arg[4]) and tonumber(arg[4]) or 0.9

--years gained by cryonics
years_gain=tonumber(arg[5]) and tonumber(arg[5]) or 4260

--starting value for probability for signing up to cryo, exponentially decreasing
decay=tonumber(arg[6]) and tonumber(arg[6]) or 0.95

--CMS cost
cms=tonumber(arg[7]) and tonumber(arg[7]) or 180

--Cost of preservation/life insurance
preservation_cost=tonumber(arg[8]) and tonumber(arg[8]) or 90000

--Year in which longevity escape velocity occurs
levyear=tonumber(arg[9]) and tonumber(arg[9]) or 2080

--Current year
curyear=tonumber(arg[10]) and tonumber(arg[10]) or os.date("*t", os.time()).year

--Revival year
revival_year=tonumber(arg[11]) and tonumber(arg[11]) or 2110

actval={78.36, 78.64, 78.66, 78.67, 78.68, 78.69, 78.69, 78.70, 78.71, 78.71, 78.72, 78.72, 78.73, 78.73, 78.74, 78.75, 78.75, 78.77, 78.79, 78.81, 78.83, 78.86, 78.88, 78.91, 78.93, 78.96, 78.98, 79.01, 79.03, 79.06, 79.09, 79.12, 79.15, 79.18, 79.21, 79.25, 79.29, 79.32, 79.37, 79.41, 79.45, 79.50, 79.55, 79.61, 79.66, 79.73, 79.80, 79.87, 79.95, 80.03, 80.13, 80.23, 80.34, 80.46, 80.59, 80.73, 80.88, 81.05, 81.22, 81.42, 81.62, 81.83, 82.05, 82.29, 82.54, 82.80, 83.07, 83.35, 83.64, 83.94, 84.25, 84.57, 84.89, 85.23, 85.58, 85.93, 86.30, 86.68, 87.08, 87.49, 87.92, 88.38, 88.86, 89.38, 89.91, 90.47, 91.07, 91.69, 92.34, 93.01, 93.70, 94.42, 95.16, 95.94, 96.72, 97.55, 98.40, 99.27, 100.14, 101.02, 101.91}

--Causes of death for certain age ranges, with probabilities for
--successful cryopreservation for each cause of death
--Add totaldeath field to each entry

deathcause=
{
	{
		lowbound=0,
		upbound=1,
		impact={0.7, 0.9, 0.75, 0.5, 0.55, 0.6, 0.65, 0.8, 0.7, 0.4},
		numbers={4473, 3679, 1358, 1334, 1168, 724, 579, 428, 390, 375}
	},
	{
		lowbound=1,
		upbound=4,
		impact={0.55, 0.75, 0.5, 0.6, 0.85, 0.85, 0.6, 0.65, 0.85, 0.3},
		numbers={1126, 384, 353, 326, 122, 115, 62, 54, 50, 43}
	},
	{
		lowbound=5,
		upbound=9,
		impact={0.55, 0.6, 0.75, 0.5, 0.85, 0.85, 0.85, 0.3, 0.65, 0.3},
		numbers={734, 393, 201, 121, 71, 68, 68, 34, 34, 19}
	},
	{
		lowbound=10,
		upbound=14,
		impact={0.55, 0.6, 0.6, 0.8, 0.5, 0.85, 0.85, 0.3, 0.85, 0.3},
		numbers={692, 596, 450, 172, 168, 101, 64, 54, 51, 30}
	},
	{
		lowbound=15,
		upbound=24,
		total_deaths=30154,
		impact={0.55, 0.6, 0.5, 0.6, 0.85, 0.85, 0.85, 0.85, 0.85, 0.55},
		numbers={12044, 6211, 4607, 1371, 905, 354, 246, 200, 165, 151}
	},
	{
		lowbound=25,
		upbound=34,
		total_deaths=58844,
		impact={0.55, 0.55, 0.5, 0.6, 0.85, 0.7, 0.85, 0.3, 0.55, 0.85},
		numbers={24614, 8020, 5234, 3864, 3561, 1008, 837, 567, 482, 457}
	},
	{
		lowbound=35,
		upbound=44,
		total_deaths=80380,
		impact={0.55, 0.5, 0.85, 0.5, 0.5, 0.7, 0.85, 0.3, 0.85, 0.65},
		numbers={22667, 10640, 10532, 7521, 3304, 3108, 2282, 1704, 956, 829}
	},
	{
		lowbound=45,
		upbound=55,
		total_deaths=164837,
		impact={0.6, 0.85, 0.55, 0.45, 0.7, 0.85, 0.3, 0.85, 0.65, 0.85},
		numbers={37301, 32220, 23056, 8345, 8157, 6144, 5128, 3807, 2380, 2339}
	},
	{
		lowbound=55,
		upbound=64,
		total_deaths=374836,
		impact={0.6, 0.85, 0.55, 0.85, 0.85, 0.7, 0.3, 0.45, 0.65, 0.85},
		numbers={113947, 81042, 23693, 18804, 14941, 13945, 12789, 8540, 5956, 5858}
	},
	{
		lowbound=65,
		upbound=101,
		total_deaths=2099263,
		impact={0.85, 0.6, 0.85, 0.3, 0.2, 0.85, 0.55, 0.85, 0.75, 0.35},
		numbers={526509, 431102, 135560, 127244, 120658, 60182, 57213, 48888, 42232, 32988}
	}
}

for i=1, #deathcause do
	local sum=0
	for j=1, #deathcause[i].numbers do
		sum=sum+deathcause[i].numbers[j]
	end
	if deathcause[i].total_deaths==nil then
		deathcause[i].total_deaths=sum*1.355
	end
	deathcause[i].numbers[#deathcause[i].numbers+1]=deathcause[i].total_deaths-sum
	deathcause[i].impact[#deathcause[i].impact+1]=0.6
end

--probability of still signing up for cryonics at a given age

function prob_signup(age)
	return decay^(age-curage)
end

b=0.108
eta=0.0001

function gompertz(age)
	return math.exp(-eta*(math.exp(b*age)-1))
end

function prob_liveto(age)
	return gompertz(age)/gompertz(curage)+extinction_risk(curyear+(age-curage))
end

function prob_diebeforelev(age)
	if curyear+(age-curage)>levyear then
		return 0
	else
		return 1-(gompertz(curage+(levyear-curyear))/gompertz(age))+extinction_risk(curyear+(age-curage))
	end
end

function avg_pres_quality(age)
	local alldeaths=0
	local weighteddeaths=0
	for i=1, #deathcause do
		local l=deathcause[i].lowbound
		local u=deathcause[i].upbound
		local factor=1
		if l<age and age<=u then
			factor=(age-l)/(u-l)
		end
		if age<=u then
			alldeaths=alldeaths+factor*deathcause[i].total_deaths
			for j=1, #deathcause[i].numbers do
				weighteddeaths=weighteddeaths+factor*deathcause[i].numbers[j]*deathcause[i].impact[j]
			end
		end
	end
	return weighteddeaths/alldeaths
end

-- Probability of human extinction by a given year

perils_end=2100
risk_before_perils_end=0.165
annual_risk_before_perils_end=0.0024
annual_risk_after_perils_end=2*10e-5

function extinction_risk(year)
	if year>perils_end then
		-- rescaling, can be at most 1-risk_before_perils_end
		post_perils_risk=(1-risk_before_perils_end)*(1-math.pow(1-annual_risk_after_perils_end, year-perils_end))
		return risk_before_perils_end+post_perils_risk
	elseif year==perils_end then
		return risk_before_perils_end
	else
		return 1-math.pow(1-annual_risk_before_perils_end, year-curyear)
	end
end

-- Adjusted benefit function

--I only get the benefit if
--1. I haven't died before signing up
--2. I die before LEV
function benefit(age)
    local ext_risk = extinction_risk(curyear + (age - curage))
    return prob_pres * prob_succ * years_gain * val_year * prob_liveto(age) * prob_diebeforelev(age) * avg_pres_quality(age)
end

function benefit(age)
	post_revival_risk=(extinction_risk(revival_year+years_gain)-extinction_risk(revival_year))
	expected_post_revival_years=prob_pres*prob_succ*(1-post_revival_risk)*years_gain
	return expected_post_revival_years*val_year*prob_liveto(age)*prob_diebeforelev(age)*avg_pres_quality(age)
end

function cms_age(age)
	return actval[age]-10
end

function cms_fees(age)
	return cms*(actval[age]-cms_age(age))
end

function membership_fees(age)
	local left=math.min(math.floor(actval[age])-age, levyear-curyear)
	local cost=0

	if age<25 then
		newage=25
		cost=(newage-age)*310
	end
	if left>=30 then
		cost=cost+(left-30)*305
		left=30
	end
	if left>=25 then
		cost=cost+(left-25)*368
		left=24
	end
	if left>=20 then
		cost=cost+(left-20)*430
		left=20
	end
	if age<=25 then
		cost=cost+(left-(25-age))*525
	else
		cost=cost+left*525
	end

	return 300+cost
end

--Assumes that insurance companies have accurately priced LEV & others
--in already

function pres_cost(age)
	return preservation_cost
end

function cost(age)
	return membership_fees(age)+pres_cost(age)+cms_fees(age)
end

function value(age)
	return prob_signup(age)*prob_liveto(age)*(benefit(age)-cost(age))
end

for age=curage,math.floor(actval[curage]) do
	print(value(age) .. ": " .. age)
end

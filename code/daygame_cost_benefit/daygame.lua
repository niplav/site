--Is daygame worth it? A little model designed to find that out.
--Also, calculating the optimal number of approaches.

--TODO: Sources for nearly all of these numbers
--TODO: How often do people who do daygame sleep with their lays?
--Probably has quadratically diminishing returns on each time they have sex.

--A bit under minimum wage
hour_val=5
--Price of middle range quality prostitution+a sense of pride and accomplishment
prost_cost=250
pride_val=500
first_lay_val=prost_cost+pride_val
--How much a date costs (rough estimate)
date_cost=40
--The average number of dates before a lay
avg_dates=2
--The average length of a date (in hours) (total 7 hours for 2 dates, mystery's number)
date_len=3.5

--One every 15 minutes seems fair, but most experienced daygamers seem to do less?
appr_per_hour=4
--The definite upper limit seems to be 1 in 30 for professionals
--but for the average person not willing to travel for daygame,
--that seems a bit much
ratio_expert=0.02
--The general consensus seems to be 1 in 100 for beginners, but
--I've read reports of guys not getting any lays within the first ~200
--approaches.
ratio_beginner=0.005

function ratio(appr)
	--grows to approximate the expert ratio, starting from the beginner ratio
	return ratio_beginner+(ratio_expert-ratio_beginner)*(1-500/(appr+500))
end

function benefit(appr)
	local lay_ratio=ratio(appr)
	--positive side-effects of daygame of behavior
	--it seems like those grow very slowly after an initial surge
	local sideeff_val=200*math.log((appr+1)*0.2)
	return first_lay_val*math.sqrt(lay_ratio*appr)+sideeff_val
end

function cost(appr)
	--I could be working minimum wage!
	local opportunity_cost=hour_val*appr/appr_per_hour
	--mental cost is at first positive (the first approaches are very hard)
	--then daygame becomes an enjoyable activity and the mental cost is negative
	--i.e a benefit, but the enjoyment fades over time
	local mental_cost=-(200*math.log((appr+100)*0.01))-200
	--one can abuse the ratio to find out how many dates one will have to pay
	--maybe a constant factor is not appropriate?
	local date_ratio=3*ratio(appr)
	local total_date_cost=date_ratio*date_cost*avg_dates
	local date_opp_cost=date_ratio*date_len*avg_dates*hour_val
	return opportunity_cost+mental_cost+total_date_cost+date_opp_cost
end

for i=1,10000 do
	print((benefit(i)-cost(i)) .. ": " .. i)
end

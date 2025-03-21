import squigglepy as sq

num_ontological_categories=sq.to(0, 10)
cost_new_entity=sq.lognorm(lognorm_mean=(1/0.045)*10**53, lognorm_sd=20)
prop_universe_entities=num_ontological_categories/sq.to(1, 3)
new_entity_cost=cost_new_entity/prop_universe_entities

gwp=sq.norm(mean=10**14, sd=1)
prop_spent_on_freedom=sq.beta(a=2, b=8)
real_freewill_mult=sq.to(4, 20)
chance_freewill_exists=sq.beta(a=1, b=4)
total_value=prop_spent_on_freedom*gwp*real_freewill_mult*(1-chance_freewill_exists)

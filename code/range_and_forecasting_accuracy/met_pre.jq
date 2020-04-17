[
	.[]|
	.results|
	.[]|
	select(.possibilities.type=="binary")|
	select([.resolution==0,.resolution==1]|any)|
	[
		[{res: .resolution, restime: .resolve_time, id: .id}],
		[
			.prediction_timeseries|
			.[]|
			{commpred: .community_prediction, predtime:.t}
		]
	]|
	combinations|
	{id: .[0].id, res: .[0].res, restime: .[0].restime, commpred: .[1].commpred, predtime: .[1].predtime}
]

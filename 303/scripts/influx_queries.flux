from(bucket:"DPI")
	|> range(start: 2023-01-01T00:00:00Z)
	|> group(columns: ["_measurement"])
	|> count()

from(bucket:"DPI")
	|> range(start: 2023-01-01T00:00:00Z)

from(bucket: "DPI")
	|> range(start: 2023-01-01T00:00:00Z)
	|> filter(fn: (r) => r._field == "1_Temperature")
	|> filter(fn: (r) => r._value < 10.0)

from(bucket:"DPI")
	|> range(start: 2023-01-05T05:00:00.000000Z)
	|> count()

from(bucket:"DPI")
	|> range(start: 2023-01-05T05:00:00.000000Z)

from(bucket:"DPI")
	|> range(start: 2023-01-04T00:00:00Z, stop: 2023-01-05T00:00:00Z)

from(bucket:"DPI")
	|> range(start: 2023-01-04T00:00:00Z, stop: 2023-01-05T00:00:00Z)
	|> count()

from(bucket:"DPI")
	|> range(start: 2023-01-04T00:00:00Z, stop: 2023-01-05T00:00:00Z)
	|> filter(fn: (r) => r._field == "gnss" and
			     r._value > 20.0)

from(bucket:"DPI")
	|> range(start: 2023-01-04T00:00:00Z, stop: 2023-01-05T00:00:00Z)
	|> filter(fn: (r) => r._field == "gnss" and
			     r._value > 20.0)
	|> count()

from(bucket:"DPI")
	|> range(start: 2023-01-04T00:00:00Z, stop: 2023-01-05T00:00:00Z)
	|> filter(fn: (r) => r._field == "gnss" and
			     r._value > 20.0 and
			     r._value < 25.0)
	|> count()

from(bucket:"DPI")
	|> range(start: 2023-01-04T00:00:00Z, stop: 2023-01-05T00:00:00Z)
	|> filter(fn: (r) => r._field == "gnss" and
			     r._value > 20.0 and
			     r._value < 25.0)

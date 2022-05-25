"""
RuuviTagReactive and Reactive Extensions Subject examples
"""

from ruuvitag_sensor.ruuvi_rx import RuuviTagReactive
from rx import operators as ops

tags = {
    'F4:A5:74:89:16:57': 'sauna',
    'CC:2C:6A:1E:59:3D': 'bedroom',
    'BB:2C:6A:1E:59:3D': 'livingroom'
}

ruuvi_rx = RuuviTagReactive(list(tags.keys()))

# Print all notifications
ruuvi_rx.get_subject().\
    subscribe(print)

# Get updates only for F4:A5:74:89:16:57
ruuvi_rx.get_subject().pipe(
    ops.filter(lambda x: x[0] == 'F4:A5:74:89:16:57')
).subscribe(lambda x: print(x[1]))

# Print only last updated every 10 seconds for F4:A5:74:89:16:57
ruuvi_rx.get_subject().pipe(
    ops.filter(lambda x: x[0] == 'F4:A5:74:89:16:57'),
    ops.sample(10.0)
).subscribe(lambda data: print(data))

# Print only last updated every 10 seconds for every found sensor
ruuvi_rx.get_subject().pipe(
    ops.group_by(lambda x: x[0])
).subscribe(lambda x: x.pipe(ops.sample(10.0)).subscribe(print))

# Print all from the last 10 seconds for F4:A5:74:89:16:57
ruuvi_rx.get_subject().pipe(
    ops.filter(lambda x: x[0] == 'F4:A5:74:89:16:57'),
    ops.buffer_with_time(10.0)
).subscribe(lambda datas: print(datas))

# Execute subscribe only once for F4:A5:74:89:16:57
# when temperature goes over 80 degrees
ruuvi_rx.get_subject().pipe(
    ops.filter(lambda x: x[0] == 'F4:A5:74:89:16:57'),
    ops.filter(lambda x: x[1]['temperature'] > 80),
    ops.take(1)
).subscribe(lambda x: print('Sauna is ready! Temperature: {}'.format(x[1]['temperature'])))

# Execute only every time when pressure changes for F4:A5:74:89:16:57
ruuvi_rx.get_subject().pipe(
    ops.filter(lambda x: x[0] == 'F4:A5:74:89:16:57'),
    ops.distinct_until_changed(lambda x: x[1]['pressure']),
).subscribe(lambda x: print('Pressure changed: {}'.format(x[1]['pressure'])))

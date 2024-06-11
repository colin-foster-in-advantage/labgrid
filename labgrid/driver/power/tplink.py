""" Tested with TP Link KP303, and should be compatible with any strip supported by kasa """

import asyncio
from kasa import SmartStrip, SmartPlug, SmartDevice


def _target_get(device: SmartDevice, index):
    if device.is_strip:
        assert (
            len(device.children) > index
        ), "Trying to access non-existant plug socket on strip"
        return device.children[index]
    elif device.is_plug:
        return device
    assert(), "Trying to access invalid device"


def _device_get(host, index):
    if index < 0:
        device = SmartPlug(host)
    else:
        device = SmartStrip(host)
    return device


async def _power_set(host, port, index, value):
    """We embed the coroutines in an `async` function to minimise calls to `asyncio.run`"""
    assert port is None
    index = int(index)
    device = _device_get(host, index)
    await device.update()
    target = _target_get(device, index)
    if value is True:
        await target.turn_on()
    elif value is False:
        await target.turn_off()


def power_set(host, port, index, value):
    asyncio.run(_power_set(host, port, index, value))


def power_get(host, port, index):
    assert port is None
    index = int(index)
    device = _device_get(host, index)
    asyncio.run(device.update())
    target = _target_get(device, index)
    return target.is_on

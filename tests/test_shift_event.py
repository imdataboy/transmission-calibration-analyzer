from transmission_analyzer.models.shift_event import ShiftEvent


def test_create_shift_event():
    event = ShiftEvent(
        time=5.0,
        from_gear=1,
        to_gear=2,
        shift_type="upshift"
    )

    assert event.time == 5.0
    assert event.from_gear == 1
    assert event.to_gear == 2
    assert event.shift_type == "upshift"


def test_gear_delta():
    upshift = ShiftEvent(
        time=5.0,
        from_gear=1,
        to_gear=3,
        shift_type="upshift"
    )

    downshift = ShiftEvent(
        time=10.0,
        from_gear=4,
        to_gear=2,
        shift_type="downshift"
    )

    assert upshift.gear_delta == 2
    assert downshift.gear_delta == -2


def test_skip_shift():
    normal_shift = ShiftEvent(
        time=5.0,
        from_gear=1,
        to_gear=2,
        shift_type="upshift"
    )

    skip_shift= ShiftEvent(
        time=10.0,
        from_gear=1,
        to_gear=3,
        shift_type="upshift"
    )

    down_skip_shift = ShiftEvent(
        time=4.0,
        from_gear=3,
        to_gear=1,
        shift_type="downshift"
    )

    assert normal_shift.is_skip_shift is False
    assert skip_shift.is_skip_shift is True
    assert down_skip_shift.is_skip_shift is True
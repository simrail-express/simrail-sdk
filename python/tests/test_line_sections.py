from simrail_sdk import line_sections, stations, enums

r = line_sections.line_section_registry


def test_get_after_halt():
    ls = r.get_after(1, stations.Brwinow, enums.Parity.ODD)
    raise NotImplementedError(ls)


def test_get_after_freight_group():
    raise NotImplementedError


def test_get_after_block_post():
    raise NotImplementedError


def test_get_after_branch_off_point():
    raise NotImplementedError


def test_get_after_station_parity_odd():
    raise NotImplementedError


def test_get_after_station_parity_even():
    raise NotImplementedError


def test_get_after_end_of_line():
    raise NotImplementedError


def test_name():
    raise NotImplementedError

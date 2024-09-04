from simrail_sdk import stations


def test_printable_name():
    assert stations.GrodziskMazowiecki.printable_name == "Grodz Maz"


def test_branch_off_points():
    assert stations.GrodziskMazowiecki.branch_off_points == {
        stations.GrodziskMazowieckiR58,
        stations.GrodziskMazowieckiR64,
    }


def test_is_junction():
    assert stations.GrodziskMazowiecki.is_junction
    assert not stations.SosnowiecPorabka.is_junction


def test_is_station():
    assert stations.WarszawaGrochow.is_station  # stth
    assert stations.GrodziskMazowiecki.is_station  # st
    assert not stations.SosnowiecPorabka.is_station  # po


def test_is_traffic_post():
    assert stations.GrodziskMazowiecki.is_traffic_post  # st
    assert stations.Knapowka.is_traffic_post  # podg
    assert not stations.SosnowiecPorabka.is_traffic_post  # po

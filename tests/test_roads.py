import pytest

from world import roads as mod

CASES = [
    ('point_segment_distance', [[0, 1], [0, 0], [2, 0]], 1.0, True),
    ('point_segment_distance', [[3, 0], [0, 0], [2, 0]], 1.0, True),
    ('segment_intersection', [[0, 0], [2, 2], [0, 2], [2, 0]], [1.0, 1.0], True),
    ('segment_intersection', [[0, 0], [1, 0], [2, 0], [3, 0]], None, False),
    ('catmull_rom', [[0, 0], [1, 1], [2, 1], [3, 0], 0.5], [1.5, 1.125], True),
    ('road_width', [4, 3.5], 14.0, True),
    ('graph_degree', [[(0, 1), (1, 0), (1, 2)], 1], 2, False),
    ('snap_to_grid', [1.26, 0.5], 1.5, True),
    ('samples_for_length', [10, 2], 6, False),
    ('zoning_depth', [7, 2], 11.0, True),
    ('turn_angle', [[0, 0], [1, 0], [1, 1]], 90.0, True),
    ('commit_tiles', [[True, True]], True, False),
    ('point_segment_distance', [[1, 0], [0, 0], [2, 0]], 0.0, True),
    ('segment_intersection', [[0, 0], [0, 0], [0, 0], [1, 1]], None, False),
    ('samples_for_length', [0, 2], 1, False),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_roads_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected

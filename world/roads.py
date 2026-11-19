"""程序化道路：图、曲线与路口的核心几何与图工具。"""

import math

_EPS = 1e-12


def point_segment_distance(point, a, b):
    """点到线段距离。"""
    px, py = float(point[0]), float(point[1])
    ax, ay = float(a[0]), float(a[1])
    bx, by = float(b[0]), float(b[1])

    dx, dy = bx - ax, by - ay
    length_sq = dx * dx + dy * dy
    if length_sq <= _EPS:
        # 退化线段：退化为到端点的距离
        return math.hypot(px - ax, py - ay)

    # 投影参数夹紧到 [0, 1]，避免把线段外部的点投到延长线上
    t = ((px - ax) * dx + (py - ay) * dy) / length_sq
    t = min(1.0, max(0.0, t))

    cx, cy = ax + t * dx, ay + t * dy
    return math.hypot(px - cx, py - cy)


def segment_intersection(a, b, c, d):
    """线段求交，含端点。"""
    ax, ay = float(a[0]), float(a[1])
    bx, by = float(b[0]), float(b[1])
    cx, cy = float(c[0]), float(c[1])
    dx, dy = float(d[0]), float(d[1])

    rx, ry = bx - ax, by - ay
    sx, sy = dx - cx, dy - cy

    denom = rx * sy - ry * sx
    if abs(denom) <= _EPS:
        # 平行、共线或退化线段：没有唯一交点
        return None

    qpx, qpy = cx - ax, cy - ay
    t = (qpx * sy - qpy * sx) / denom
    u = (qpx * ry - qpy * rx) / denom

    # 闭区间：端点接触也算相交
    if t < -_EPS or t > 1.0 + _EPS or u < -_EPS or u > 1.0 + _EPS:
        return None

    return [ax + t * rx, ay + t * ry]


def catmull_rom(p0, p1, p2, p3, t):
    """Catmull-Rom 曲线采样。"""
    t = float(t)
    t2 = t * t
    t3 = t2 * t

    # 三次 Hermite 基函数
    h00 = 2.0 * t3 - 3.0 * t2 + 1.0
    h10 = t3 - 2.0 * t2 + t
    h01 = -2.0 * t3 + 3.0 * t2
    h11 = t3 - t2

    dims = min(len(p0), len(p1), len(p2), len(p3))
    result = []
    for i in range(dims):
        a0, a1, a2, a3 = (float(p[i]) for p in (p0, p1, p2, p3))
        # Catmull-Rom 张力：切线取相邻点差的一半（张力 0.5）
        m1 = 0.5 * (a2 - a0)
        m2 = 0.5 * (a3 - a1)
        result.append(h00 * a1 + h10 * m1 + h01 * a2 + h11 * m2)
    return result


def road_width(lanes, lane_width):
    """路宽按车道数与车道宽计算。"""
    return float(lanes) * float(lane_width)


def graph_degree(edges, node):
    """图度数按去重边计算。"""
    unique_edges = {frozenset((edge[0], edge[1])) for edge in edges}
    return sum(1 for edge in unique_edges if node in edge)


def snap_to_grid(value, cell):
    """网格吸附。"""
    value = float(value)
    cell = float(cell)
    if cell <= 0.0:
        return value
    # 四舍五入到最近的网格线（含 .5 进位）
    return math.floor(value / cell + 0.5) * cell


def samples_for_length(length, step):
    """采样数按长度与步长。"""
    length = float(length)
    step = float(step)
    if length <= 0.0 or step <= 0.0:
        return 1
    # 包含起点与最后一个不超过 length 的采样点
    return int(math.floor(length / step + 1e-9)) + 1


def zoning_depth(road_width, setback):
    """退界深度。"""
    # 道路两侧各退让一次
    return float(road_width) + 2.0 * float(setback)


def turn_angle(a, b, c):
    """转角角度（度）。"""
    v1x, v1y = float(b[0]) - float(a[0]), float(b[1]) - float(a[1])
    v2x, v2y = float(c[0]) - float(b[0]), float(c[1]) - float(b[1])

    if (abs(v1x) <= _EPS and abs(v1y) <= _EPS) or (abs(v2x) <= _EPS and abs(v2y) <= _EPS):
        return 0.0

    cross = v1x * v2y - v1y * v2x
    dot = v1x * v2x + v1y * v2y
    # 有符号转角：左转为正，右转为负
    return math.degrees(math.atan2(cross, dot))


def commit_tiles(statuses):
    """批量瓦片全部成功才提交。"""
    return all(statuses)

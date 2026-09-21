"""A prescribed rest-to-rest motion and small numerical integration helpers."""
import math


def smooth_move(t, duration, start, end):
    """Quintic motion: return position, velocity, acceleration in matching units."""
    q = min(1.0, max(0.0, t / duration))
    distance = end - start
    position = start + distance * (10 * q ** 3 - 15 * q ** 4 + 6 * q ** 5)
    velocity = distance / duration * (30 * q ** 2 - 60 * q ** 3 + 30 * q ** 4)
    acceleration = distance / duration ** 2 * (60 * q - 180 * q ** 2 + 120 * q ** 3)
    return position, velocity, acceleration


def motion_times(duration, intervals=200):
    """Include endpoints and exact acceleration-extremum times."""
    values = [duration * i / intervals for i in range(intervals + 1)]
    values.extend(duration * (3 + sign * math.sqrt(3)) / 6 for sign in (-1, 1))
    return sorted(set(values))


def trapezoid(x, y):
    return sum((x[i + 1] - x[i]) * (y[i + 1] + y[i]) / 2 for i in range(len(x) - 1))


def rk4_step(derivative, t, state, h):
    """Classical fourth-order Runge-Kutta for a short state vector."""
    k1 = derivative(t, state)
    k2 = derivative(t + h / 2, [s + h * k / 2 for s, k in zip(state, k1)])
    k3 = derivative(t + h / 2, [s + h * k / 2 for s, k in zip(state, k2)])
    k4 = derivative(t + h, [s + h * k for s, k in zip(state, k3)])
    return [s + h * (a + 2 * b + 2 * c + d) / 6 for s, a, b, c, d in zip(state, k1, k2, k3, k4)]

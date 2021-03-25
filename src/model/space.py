from api.communication.events import EventSource, EventHandler, EventListener

from typing import List, Tuple, Mapping
from itertools import combinations
from model.body import Body


class Space:
    def __init__(self, dimensions: Tuple[int, int] = (-1, -1), drag: float = 0, gravity: float = 0):
        super(Space, self).__init__()

        self.bodies = list()  # type: List[Body]
        self.dimensions = dimensions
        self.drag = drag
        self.gravity = gravity
        self.gravity_mapping = {}  # type: Mapping[Body, List[Body]]

    def add_body(self, kind=None, *args, **kwargs):
        if kind is None:
            raise TypeError('Needs a kind')
        body = kind(*args, **kwargs, space=self)
        self.bodies.append(body)
        return body

    def add_many(self, bodies):
        self.bodies.extend(bodies)

    def update(self, dt):
        self.handle_collisions()
        for body in self.bodies:
            body.checkbounds(*self.dimensions, strategy=body.wrap)
            body.update(dt)

    def handle_collisions(self):
        for body_a, body_b in combinations(self.bodies, 2):
            if body_a.collides_with(body_b):
                self._correct_velocities(body_a, body_b)

    def _correct_velocities(self, body_a: Body, body_b: Body):
        m1 = body_a.mass
        m2 = body_b.mass

        p1 = body_a.position
        p2 = body_b.position

        v1 = body_a.velocity
        v2 = body_b.velocity

        v1_new = v1 - (p1 - p2) * ((2 * m2) / (m1 + m2)) * (((v1 - v2) * (p1 - p2)) / (p1 - p2).distance_squared())
        v2_new = v2 - (p2 - p1) * ((2 * m1) / (m1 + m2)) * (((v2 - v1) * (p2 - p1)) / (p2 - p1).distance_squared())

        body_a.velocity = v1_new
        body_b.velocity = v2_new

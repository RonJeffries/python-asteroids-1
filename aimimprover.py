

class AimImprover:
    def __init__(self, best_target_position, target_velocity, shooter_position, missile_speed, safe_distance):
        self.original_target_position = best_target_position
        self.target_velocity = target_velocity
        self.shooter_position = shooter_position
        self.missile_speed = missile_speed
        self.safe_distance = safe_distance

    def improved_aiming_point(self, initial_aiming_point):
        missile_travel_distance = self.shooter_position.distance_to(initial_aiming_point) - self.safe_distance
        missile_travel_time = missile_travel_distance / self.missile_speed
        ship_motion = missile_travel_time * self.target_velocity
        anticipated_ship_position = self.original_target_position + ship_motion
        return anticipated_ship_position

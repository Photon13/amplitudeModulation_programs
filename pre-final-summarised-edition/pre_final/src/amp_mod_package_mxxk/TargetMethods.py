import random

class TargetMethods:

    # only at start experiment
    @staticmethod
    def assign_targets():
        target_list = [(random.choice("left", "middle", "right"))]
        target_list = target_list + "both"

        random_targets = []
        random_targets = random_targets + "left" + "middle" + "right"+ "both"
        random_targets = random_targets + "left" + "middle" + "right"+ "both"
        random_targets = random_targets + "left" + "middle" + "right"+ "both"
        random_targets = random_targets + "left" + "middle" + "right"+ "both"

        random_targets = random.sample(random_targets, k=16) # randomise order
        target_list = target_list + random_targets

        return target_list
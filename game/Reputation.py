# game/Reputation.py
from enum import Enum

class ReputationLevel(Enum):
    UNKNOWN = "Unknown"
    HATED = "Hated"
    DISLIKED = "Disliked"
    NEUTRAL = "Neutral"
    LIKED = "Liked"
    FRIENDLY = "Friendly"

class ReputationManager:
    THRESHOLDS = {
        ReputationLevel.HATED: -10,
        ReputationLevel.DISLIKED: -1,
        ReputationLevel.NEUTRAL: 0,
        ReputationLevel.LIKED: 10,
        ReputationLevel.FRIENDLY: 20,
    }

    # Points gained or lost for specific actions
    BUY_ITEM = 2
    SELL_ITEM = 1
    ATTACK_MEMBER = -25

    @staticmethod
    def get_level_from_points(points):
        if points is None:
            return ReputationLevel.UNKNOWN.value

        level = ReputationLevel.NEUTRAL
        if points <= ReputationManager.THRESHOLDS[ReputationLevel.HATED]:
            level = ReputationLevel.HATED
        elif points <= ReputationManager.THRESHOLDS[ReputationLevel.DISLIKED]:
            level = ReputationLevel.DISLIKED
        elif points >= ReputationManager.THRESHOLDS[ReputationLevel.FRIENDLY]:
            level = ReputationLevel.FRIENDLY
        elif points >= ReputationManager.THRESHOLDS[ReputationLevel.LIKED]:
            level = ReputationLevel.LIKED
        
        return level.value

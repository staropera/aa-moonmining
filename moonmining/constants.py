from enum import IntEnum

# EVE IDs
EVE_CATEGORY_ID_ASTEROID = 25

EVE_GROUP_ID_REFINERY = 1406
EVE_GROUP_ID_MOON = 8

EVE_GROUP_ID_UBIQUITOUS_MOON_ASTEROIDS = 1884
EVE_GROUP_ID_COMMON_MOON_ASTEROIDS = 1920
EVE_GROUP_ID_UNCOMMON_MOON_ASTEROIDS = 1921
EVE_GROUP_ID_RARE_MOON_ASTEROIDS = 1922
EVE_GROUP_ID_EXCEPTIONAL_MOON_ASTEROIDS = 1923

EVE_TYPE_ID_MOON = 14

DOGMA_ATTRIBUTE_ID_ORE_QUALITY = 2699

DATETIME_FORMAT = "%Y-%b-%d %H:%M"
VALUE_DIVIDER = 1_000_000_000


class IconSize(IntEnum):
    SMALL = 32
    MEDIUM = 64
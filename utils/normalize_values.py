from typing import List

theme_map = {
    0: "Religion & Beliefs",
    1: "Loved Ones",
    2: "Travel & Culture",
    3: "Achievements & Triumph",
    4: "Aspirations",
    5: "Cues of Reassurance",
    6: "Hobbies & Interests",
    7: "Practicality & Utility",
}


def get_theme_name(array_location: int) -> str:
    """
    Get theme name based on array location from theme_mapping.json.
    """
    return theme_map[array_location]


def floor_negative_values(values: List[float]) -> List[float]:
    """
    Floor negative values to 0.
    """
    return list(map(lambda x: max(x, 0), values))


def get_theme_values_dict(values: List[float]) -> dict[str, float]:
    """
    Get theme values dictionary from list of values.
    returns: {"theme_name": value}
    """
    values = floor_negative_values(values)
    total = sum(values)
    normalized_values = list(map(lambda x: x / total, values))
    theme_values_dict = {}
    for i, value in enumerate(normalized_values):
        theme_name = get_theme_name(i)
        theme_values_dict[theme_name] = round(value, 2)
    return theme_values_dict

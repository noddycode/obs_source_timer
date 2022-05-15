import obspython as obs

time_multipliers = {
    "Hour": 3600000,
    "Minute": 60000,
    "Second": 1000
}

active_flag = False

class ScriptSettings():

    def __init__(self, source_name, frequency, frequency_unit, duration, duration_unit):
        self.source_name = source_name
        self.frequency = frequency
        self.frequency_unit = frequency_unit
        self.duration = duration
        self.duration_unit = duration_unit


def get_all_source_names():
    sources = obs.obs_enum_sources()
    source_names = [obs.obs_source_get_name(s) for s in sources]
    obs.source_list_release(sources)
    return sorted(source_names)


def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """

    props = obs.obs_properties_create()

    source_names = get_all_source_names()
    obs_scene_list = obs.obs_properties_add_list(props, "source", "Source", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    for source_name in source_names:
        obs.obs_property_list_add_string(obs_scene_list, source_name, source_name)

    obs.obs_properties_add_int(props, "frequency", "Show every",
                               1, 1000000, 1)

    obs_unit_list = obs.obs_properties_add_list(props, "frequency_unit", "", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    for unit in time_multipliers:
        obs.obs_property_list_add_string(obs_unit_list, unit + "(s)", unit)

        obs.obs_properties_add_int(props, "duration", "For",
                               1, 1000000, 1)

    obs_unit_list = obs.obs_properties_add_list(props, "duration_unit", "", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    for unit in time_multipliers:
        obs.obs_property_list_add_string(obs_unit_list, unit + "(s)", unit)

    obs.obs_properties_add_button(props, "start_button", "Start", start_timers)
    obs.obs_properties_add_button(props, "stop_button", "Stop", stop_timers)

    return props


def stop_timers(_, _2):
    obs.timer_remove(duration_timer)
    obs.timer_remove(frequency_timer)


def start_timers(_, _2):
    stop_timers(None, None)
    duration_timer()


def set_visibility(is_visible):
    current_scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
    scene_item = obs.obs_scene_find_source(current_scene, script_settings.source_name)
    obs.obs_sceneitem_set_visible(scene_item, is_visible)
    obs.obs_scene_release(current_scene)


def duration_timer():
    set_visibility(False)
    obs.timer_add(frequency_timer, script_settings.frequency * time_multipliers[script_settings.frequency_unit])
    obs.timer_remove(duration_timer)


def frequency_timer():
    set_visibility(True)
    obs.timer_add(duration_timer, script_settings.duration * time_multipliers[script_settings.duration_unit])
    obs.timer_remove(frequency_timer)
   

def script_update(settings):
    """
    Called when user updates a setting
    """
    # Quartzi got cut in half by Home Depot associates
    global script_settings

    stop_timers(None, None)

    settings_values = [
        obs.obs_data_get_string(settings, "source"),
        obs.obs_data_get_int(settings, "frequency"),
        obs.obs_data_get_string(settings, "frequency_unit"),
        obs.obs_data_get_int(settings, "duration"),
        obs.obs_data_get_string(settings, "duration_unit")
    ]

    script_settings = ScriptSettings(*settings_values)
    


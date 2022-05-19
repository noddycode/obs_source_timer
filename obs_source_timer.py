import obspython as obs

time_multipliers = {
    "Hour": 3600000,
    "Minute": 60000,
    "Second": 1000
}

active_flag = False
source_dict = {}


# Simple class to hold settings after each update
class CurrentSettings():
    source_name = ""
    frequency = 0
    frequency_unit = ""
    duration = 0
    duration_unit = ""

class SourceController():

    def __init__(self, source_name, frequency, frequency_unit, duration, duration_unit):
        self.source_name = source_name
        self.frequency = frequency
        self.frequency_unit = frequency_unit
        self.duration = duration
        self.duration_unit = duration_unit

    def set_visibility(self, is_visible):
        current_scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
        scene_item = obs.obs_scene_find_source(current_scene, self.source_name)
        obs.obs_sceneitem_set_visible(scene_item, is_visible)
        obs.obs_scene_release(current_scene)

    def duration_timer(self):
        self.set_visibility(False)
        obs.timer_add(self.frequency_timer, self.frequency * time_multipliers[self.frequency_unit])
        obs.timer_remove(self.duration_timer)

    def frequency_timer(self):
        self.set_visibility(True)
        obs.timer_add(self.duration_timer, self.duration * time_multipliers[self.duration_unit])
        obs.timer_remove(self.frequency_timer)

    def stop_timers(self, props, prop):
        obs.timer_remove(self.duration_timer)
        obs.timer_remove(self.frequency_timer)

    def start_timers(self, props, prop):
        self.stop_timers(None, None)
        self.frequency_timer()

def get_all_source_names():
    sources = obs.obs_enum_sources()
    source_names = [obs.obs_source_get_name(s) for s in sources]
    obs.source_list_release(sources)
    return sorted(source_names)


def add_update_controller(props, prop):
    global source_dict

    source_dict[CurrentSettings.source_name] = SourceController(
        CurrentSettings.source_name, 
        CurrentSettings.frequency, 
        CurrentSettings.frequency_unit, 
        CurrentSettings.duration, 
        CurrentSettings.duration_unit)


def set_existing_properties(props, prop, settings):
    if CurrentSettings.source_name not in source_dict:
        return True

    controller = source_dict[CurrentSettings.source_name]

    obs.obs_data_set_int(settings, "frequency", controller.frequency)
    obs.obs_data_set_string(settings, "frequency_unit", controller.frequency_unit)
    obs.obs_data_set_int(settings, "duration", controller.duration)
    obs.obs_data_set_string(settings, "duration_unit", controller.duration_unit)
    obs.obs_properties_apply_settings(props, settings)

    return True

def start_timers(props, prop):
    controller = source_dict[CurrentSettings.source_name]
    controller.start_timers(props, prop)

def stop_timers(props, prop):
    controller = source_dict[CurrentSettings.source_name]
    print(controller)
    controller.stop_timers(props, prop)

def stop_all_timers(props, prop):
    for controller in source_dict.values():
        controller.stop_timers(props, prop)


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

    obs.obs_properties_add_button(props, "add_update_button", "Add/Update", add_update_controller)
    obs.obs_property_set_modified_callback(obs_scene_list, set_existing_properties)

    obs.obs_properties_add_button(props, "start_button", "Start Timer", start_timers)
    obs.obs_properties_add_button(props, "stop_button", "Stop Timer", stop_timers)
    obs.obs_properties_add_button(props, "stop_all_button", "Stop All", stop_all_timers)

    return props


def script_update(settings):
    """
    Called when user updates a setting
    """
    CurrentSettings.source_name = obs.obs_data_get_string(settings, "source")
    CurrentSettings.frequency = obs.obs_data_get_int(settings, "frequency")
    CurrentSettings.frequency_unit = obs.obs_data_get_string(settings, "frequency_unit")
    CurrentSettings.duration = obs.obs_data_get_int(settings, "duration")
    CurrentSettings.duration_unit = obs.obs_data_get_string(settings, "duration_unit")


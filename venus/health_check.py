import yaml




def apply_health_checks(filename):
    with open(filename) as stream:
        data_as_dict = yaml.load(stream)
    for health_check_type, health_check_attrs in data_as_dict[
        'health_checks'].items():
        print(health_check_type)
        # print(health_check_attrs)

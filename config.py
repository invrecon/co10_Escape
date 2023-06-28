import json


def configure_sogpf():
    overwrite("Configs/SOGPF.json", update_config_sogpf)


def configure_ws():
    overwrite("Configs/WS.json", update_config_ws)


def configure_main():
    overwrite("Configs/config.json", update_config_main)


def overwrite(path, update_config):
    with open(path, "r") as file:
        config = json.load(file)

    update_config(config)

    with open(path, "w") as file:
        json.dump(config, file, indent=4)


def update_config_sogpf(config):
    config['Missions'] = list(filter(
        lambda mission: mission['island'] in ["Cam Lao Nam", "Khe Sanh", "The Bra"],
        config['Missions']
    ))


def update_config_ws(config):
    config['Missions'] = list(filter(
        lambda mission: mission['island'] == "Sefrou-Ramal",
        config['Missions']
    ))


def update_config_main(config):
    islands = ["Altis", "Stratis", "Tanoa", "Malden 2035", "Livonia", "Sefrou-Ramal"]

    config['Subconfigs'] = list(filter(
        lambda subconfig: subconfig in ["./Configs/WS.json", "./Configs/SOGPF.json"],
        config['Subconfigs']
    ))

    config['Islands'] = list(filter(
        lambda island: island['name'] in islands,
        config['Islands']
    ))

    by_island = filter(
        lambda mission: mission['island'] in islands,
        config['Missions']
    )
    tanoa_apex = filter(
        lambda mission: mission['mod'].startswith("Vanilla Apex") if mission ['island'] == "Tanoa" else True,
        by_island
    )
    livonia_contact = filter(
        lambda mission: mission['mod'] == "Vanilla Contact US" if mission ['island'] == "Livonia" else True,
        tanoa_apex
    )
    without_sefrou = filter(
        lambda mission: mission ['island'] != "Sefrou-Ramal",
        livonia_contact
    )

    config['Missions'] = list(without_sefrou)
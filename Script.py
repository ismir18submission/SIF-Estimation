import Main
import Config

database = "sif"

idmt_config_list = [Config.make_config("Fender Strat Clean Neck SC", idmt=True),
                    Config.make_config("Ibanez Power Strat Clean Bridge HU", idmt=True),
                    Config.make_config("Ibanez Power Strat Clean Bridge+Neck SC", idmt=True),
                    Config.make_config("Ibanez Power Strat Clean Neck HU", idmt=True)
                    ]

sif_config_list = [Config.make_config("electric_fretted", idmt=False),
                   Config.make_config("electric_plucked", idmt=False),
                   Config.make_config("acoustic_fretted", idmt=False),
                   Config.make_config("acoustic_plucked", idmt=False),
                   Config.make_config("bass_fretted", idmt=False),
                   Config.make_config("bass_plucked", idmt=False),
                   ]

if database == "sif":
    config_list = sif_config_list
else:
    config_list = idmt_config_list

for config in config_list:
    est = Main.sif_main(config)

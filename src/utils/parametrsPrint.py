from src.localisation import localisation


class printparam(object):
    """
    Class for printing parametrs from input file
    At initialisation gets 'param' - list of text data ("0" or "1") and translate it to boolean
    """
    def __init__(self, param, local=localisation()):
        loc = local.loc(__file__)  # text for this file
        [self.input,
         self.replication,
         self.cations_2sphere_cat,
         self.cations_2sphere_ani,
         self.cations_1sphere_cat,
         self.cations_1sphere_ani,
         self.min_x2,
         self.P_distrib,
         self.cations_conf,
         self.final_conf,
         self.GULP,
         self.distrib_diag
         ] = list(map(lambda x: x == "1", param))

    def __str__(self):
        t = "\n".join(
        map(lambda a,b: "\x1b[36m" + a + ":\x1b[0m\t" + str(b),
            ["input cell coordinates",
             "replication",
            "cations_2sphere_cat",
            "cations_2sphere_ani",
            "cations_1sphere_cat",
            "cations_1sphere_ani",
            "min_x2",
            "P_distrib",
            "cations_conf",
            "final_conf",
            "GULP",
            "distrib_diag"],
            [self.input,
             self.replication,
             self.cations_2sphere_cat,
             self.cations_2sphere_ani,
             self.cations_1sphere_cat,
             self.cations_1sphere_ani,
             self.min_x2,
             self.P_distrib,
             self.cations_conf,
             self.final_conf,
             self.GULP,
             self.distrib_diag
             ])
        )
        return t
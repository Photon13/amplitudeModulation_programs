class Fams:

    famA : float = 33.503 #33.0
    famB : float = 42.197 #43.0
    famC : float = 52.321 #53.0

    famCombinationsDictLMR : dict = {
        "participant_1" :   [famB, famA, famC],      # BAC
        "participant_2" :   [famA, famC, famB],      # ACB
        "participant_3" :   [famC, famA, famB],      # CAB
        "participant_4" :   [famB, famC, famA]       # BCA
        }
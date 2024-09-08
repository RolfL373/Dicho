#Sound files, ordered alphabetically
sound_files = ['bal_dalle.wav', 'bal_gale.wav', 'bal.wav','bar_gare.wav','bar_tard.wav',
               'bar.wav','base.wav','basse_casse.wav','basse_passe.wav', 'basse.wav',
               'cage.wav','caille.wav', 'cale.wav', 'car_dard.wav', 'car_tard.wav',
               'car.wav','case_gaz.wav','case.wav','casse_basse.wav','casse_passe.wav',
               'casse.wav','dalle_bal.wav','dalle_gale.wav','dalle.wav','dard_car.wav',
               'dard_par.wav','dard_tard.wav','dard.wav','gage_page.wav','gage.wav',
               'gale_bal.wav','gale_dalle.wav','gale.wav','gare_bar.wav','gare_tard.wav',
               'gare.wav','gaz_case.wav','gaz.wav','page_gage.wav','page.wav',
               'paille_taille.wav','paille.wav','par_dard.wav','par.wav','passe_basse.wav',
               'passe_casse.wav','passe.wav','taille_paille.wav','taille.wav','tard_bar.wav',
               'tard_car.wav','tard_dard.wav','tard_gare.wav','tard.wav','tasse.wav'
               ]

codage = ['L', 'L', 'S', 'L', 'VL',
          'S', 'S', 'VL', 'V', 'S',
          'S', 'S', 'S', 'VL', 'L',
          'S', 'V', 'S', 'VL', 'L',
          'S', 'L', 'L', 'S', 'VL',
          'VL', 'V', 'S', 'VL', 'S',
          'L', 'L', 'S', 'L', 'VL',
          'S', 'V', 'S', 'VL', 'S',
          'L', 'S', 'VL', 'S', 'V',
          'L', 'S', 'L', 'S', 'VL',
          'L', 'V', 'VL', 'S', 'S'
          ]
#Index array for 'Training', pointing to "L","V" and "VL" single sound files
# tr_index= [2,5,6,9,10,11,12,15,17,20,23,27,29,32,35,37,39,41,43,46,48,53,54]

#Index array for "Training" sounds, only "L" sounds
tr_index= [2,5,15,20,23,32,35,41,46,48,53]

#Index array for 4x36=144 dichotomic sound files with "L", "V" and "VL" pairs
# di_index = [44,16,38,50,42,16,4,45,52,44,22,51,18,47,3,51,21,13,49,19,36,25,14,28,26,0,34,8,24,33,36,40,7,26,31,8,
#             8,36,28,14,25,36,49,19,34,8,31,26,7,40,33,26,0,24,4,45,16,42,50,38,51,21,52,44,13,3,16,47,18,51,22,44,
#             16,51,18,50,44,21,38,51,3,45,4,13,22,42,16,47,44,52,36,49,19,33,26,28,0,14,7,34,8,40,36,25,31,24,8,26,
#             36,26,7,14,8,0,28,26,33,19,49,24,31,25,36,40,8,34,16,4,45,3,51,38,21,50,18,52,44,47,16,42,22,13,44,51]

#Index array for 4x12 = 48 dichotomic sound files, only with "L" pairs
di_index = [50,45,22,47,3,21,19,14,0,33,40,31,14,19,31,40,33,0,45,50,21,3,47,22,50,21,3,45,22,47,19,33,0,14,40,31,14,
            0,33,19,31,40,45,3,21,50,47,22]

# sounds_L=[50,45,22,47,3,21,19,14,0,33,40,31]

tab_paires = (
    {"pair1": "bal/dalle",
    "pair2": "dalle/bal"
}, {
    "pair1": "bar/gare",
    "pair2": "gare/bar"
}, {
    "pair1": "car/tard",
    "pair2": "tard/car"
}, {
    "pair1": "casse/passe",
    "pair2": "passe/casse"
}, {
    "pair1": "dalle/gale",
    "pair2": "gale/dalle"
}, {
    "pair1": "paille/taille",
    "pair2": "taille/paille"
}, {
    "pair1": "basse/passe",
    "pair2": "passe/basse"
}, {
    "pair1": "case/gaz",
    "pair2": "gaz/case"
}, {
    "pair1": "dard/tard",
    "pair2": "tard/dard"
}, {
    "pair1": "bar/tard",
    "pair2": "tard/bar"
}, {
    "pair1": "basse/casse",
    "pair2": "casse/basse"
}, {
    "pair1": "car/dard",
    "pair2": "dard/car"
}, {
    "pair1": "dard/par",
    "pair2": "par/dard"
}, {
    "pair1": "gage/page",
    "pair2": "page/gage"
}, {
    "pair1": "gare/tard",
    "pair2": "tard/gare"
})

#Client output to CSV file - start with header
client_header=["INDEX","BLOC","STIMULUS","REPONSE","ERREUR","OGVOIS","ODVOIS","REPONSVOIS","CODAGE"]

# Reference data
reference_ages = [4, 5, 6, 7, 8, 9, 10, 15]  # Reference ages
reference_values = [0.295, 0.480, 0.865, 0.889, 1.055, 1.078, 1.066, 1.288]  # Reference values "L"
confidence_intervals = [0.76, 0.36, 0.24, 0.37, 0.22, 0.27, 0.23, 0.37]

#Block size (=12 for "L" only, =36  for "L, V, VL" test
bloc_size=12
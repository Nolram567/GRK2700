import json
import math

import numpy as np

if __name__ == "__main__":
    template = [
        {'name': 'Alt Duvenstedt', 'lat': 54.3586037, 'lng': 9.6437579, 'PAM_Mittelwert': 1.396},
        {'name': 'Bad Segeberg', 'lat': 53.9422672, 'lng': 10.3137943, 'PAM_Mittelwert': 1.499},
        {'name': 'Flensburg', 'lat': 54.7833021, 'lng': 9.4333264, 'PAM_Mittelwert': 1.603},
        {'name': 'Lohne', 'lat': 52.665257, 'lng': 8.2363523, 'PAM_Mittelwert': 1.838},
        {'name': 'Oldenburg', 'lat': 53.1389753, 'lng': 8.2146017, 'PAM_Mittelwert': 1.569},
        {'name': 'Lüneburg', 'lat': 53.248706, 'lng': 10.407855, 'PAM_Mittelwert': 1.632},
        {'name': 'Neustadt am Rübenberge', 'lat': 52.5055135, 'lng': 9.4635826, 'PAM_Mittelwert': 1.774},
        {'name': 'Rostock', 'lat': 54.0924445, 'lng': 12.1286127, 'PAM_Mittelwert': 1.237},
        {'name': 'Schwerin', 'lat': 53.6288297, 'lng': 11.4148038, 'PAM_Mittelwert': 1.43},
        {'name': 'Stralsund', 'lat': 54.3096314, 'lng': 13.0820846, 'PAM_Mittelwert': 1.181},
        {'name': 'Bergen', 'lat': 49.7808936, 'lng': 7.4176059, 'PAM_Mittelwert': 1.863},
        {'name': 'Pasewalk', 'lat': 53.5053677, 'lng': 13.9889049, 'PAM_Mittelwert': 1.192},
        {'name': 'Frankfurt an der Oder', 'lat': 52.3412273, 'lng': 14.549452, 'PAM_Mittelwert': 1.32},
        {'name': 'Fürstenwalde', 'lat': 50.76058, 'lng': 13.8681537, 'PAM_Mittelwert': 'Es liegen keine Daten vor.'},
        {'name': 'Potsdam', 'lat': 52.4009309, 'lng': 13.0591397, 'PAM_Mittelwert': 1.413},
        {'name': 'Pritzwalk', 'lat': 53.1492896, 'lng': 12.1761903, 'PAM_Mittelwert': 1.836},
        {'name': 'Lüderitz', 'lat': 52.5084647, 'lng': 11.7427093, 'PAM_Mittelwert': 'Es liegen keine Daten vor.'},
        {
            'name': 'Brandenburg an der Havel',
            'lat': 52.4108261,
            'lng': 12.5497933,
            'PAM_Mittelwert': 'Es liegen keine Daten vor.'
        },
        {'name': 'Neuruppin', 'lat': 52.9243859, 'lng': 12.8092919, 'PAM_Mittelwert': 1.603},
        {'name': 'Borken', 'lat': 51.8443183, 'lng': 6.8582247, 'PAM_Mittelwert': 1.542},
        {'name': 'Hagen', 'lat': 51.3582945, 'lng': 7.473296, 'PAM_Mittelwert': 1.218},
        {'name': 'Gütersloh', 'lat': 51.9063997, 'lng': 8.3782078, 'PAM_Mittelwert': 1.289},
        {'name': 'Horn-Bad Meinberg', 'lat': 51.8801277, 'lng': 8.9731695, 'PAM_Mittelwert': 1.232},
        {'name': 'Drolshagen', 'lat': 51.0239917, 'lng': 7.7740693, 'PAM_Mittelwert': 1.447},
        {'name': 'Halberstadt', 'lat': 51.8953514, 'lng': 11.0520563, 'PAM_Mittelwert': 1.199},
        {'name': 'Hildesheim', 'lat': 52.1521636, 'lng': 9.9513046, 'PAM_Mittelwert': 1.34},
        {'name': 'Northeim', 'lat': 51.76438235, 'lng': 9.858328873964005, 'PAM_Mittelwert': 1.693},
        {'name': 'Magdeburg', 'lat': 52.1315889, 'lng': 11.6399609, 'PAM_Mittelwert': 1.162},
        {'name': 'Bergisch-Gladbach', 'lat': 50.9929303, 'lng': 7.1277379, 'PAM_Mittelwert': 1.52},
        {'name': 'Düren', 'lat': 50.8031684, 'lng': 6.4820806, 'PAM_Mittelwert': 1.505},
        {'name': 'Troisdorf', 'lat': 50.8153071, 'lng': 7.1593271, 'PAM_Mittelwert': 1.457},
        {'name': 'Krefeld', 'lat': 51.3331205, 'lng': 6.5623343, 'PAM_Mittelwert': 1.551},
        {'name': 'Mönchengladbach', 'lat': 51.1947131, 'lng': 6.4353792, 'PAM_Mittelwert': 1.511},
        {'name': 'Montabaur', 'lat': 50.4362219, 'lng': 7.8302494, 'PAM_Mittelwert': 1.336},
        {'name': 'Schweich', 'lat': 49.8224303, 'lng': 6.7515418, 'PAM_Mittelwert': 1.504},
        {'name': 'Wittlich', 'lat': 49.9850353, 'lng': 6.88844, 'PAM_Mittelwert': 1.242},
        {'name': 'Altenkirchen', 'lat': 50.6880109, 'lng': 7.6477412, 'PAM_Mittelwert': 1.412},
        {'name': 'Heidelberg', 'lat': 49.4093582, 'lng': 8.694724, 'PAM_Mittelwert': 1.553},
        {'name': 'Kaiserslautern', 'lat': 49.4432174, 'lng': 7.7689951, 'PAM_Mittelwert': 1.553},
        {'name': 'Erbach', 'lat': 48.3274603, 'lng': 9.8913803, 'PAM_Mittelwert': 2.054},
        {'name': 'Reinheim', 'lat': 49.8364879, 'lng': 8.8238238, 'PAM_Mittelwert': 1.715},
        {'name': 'Kirkel', 'lat': 49.2833031, 'lng': 7.2333295, 'PAM_Mittelwert': 1.424},
        {'name': 'Merzig', 'lat': 49.4427023, 'lng': 6.6374902, 'PAM_Mittelwert': 1.671},
        {'name': 'Mainz', 'lat': 50.0012314, 'lng': 8.2762513, 'PAM_Mittelwert': 1.399},
        {'name': 'Heilbronn', 'lat': 49.142291, 'lng': 9.218655, 'PAM_Mittelwert': 1.645},
        {'name': 'Frankfurt am Main', 'lat': 50.1106444, 'lng': 8.6820917, 'PAM_Mittelwert': 1.565},
        {'name': 'Kleve', 'lat': 51.7854839, 'lng': 6.131367415330141, 'PAM_Mittelwert': 1.443},
        {'name': 'Homberg', 'lat': 50.6407001, 'lng': 8.1058112, 'PAM_Mittelwert': 1.35},
        {'name': 'Kassel', 'lat': 51.3154546, 'lng': 9.4924096, 'PAM_Mittelwert': 1.26},
        {'name': 'Bad Nauheim', 'lat': 50.376802999999995, 'lng': 8.7476036068774, 'PAM_Mittelwert': 1.723},
        {'name': 'Büdingen', 'lat': 50.2972353, 'lng': 9.0990829, 'PAM_Mittelwert': 1.653},
        {'name': 'Gießen', 'lat': 50.5862066, 'lng': 8.6742306, 'PAM_Mittelwert': 1.881},
        {'name': 'Ulrichstein', 'lat': 50.5759667, 'lng': 9.1929639, 'PAM_Mittelwert': 2.29},
        {'name': 'Hofbieber', 'lat': 50.5932038, 'lng': 9.8708724, 'PAM_Mittelwert': 1.491},
        {'name': 'Erfurt', 'lat': 50.9777974, 'lng': 11.0287364, 'PAM_Mittelwert': 1.361},
        {'name': 'Heilbad Heiligenstadt', 'lat': 51.3756186, 'lng': 10.138224, 'PAM_Mittelwert': 1.496},
        {'name': 'Sondershausen', 'lat': 51.3666041, 'lng': 10.8668419, 'PAM_Mittelwert': 1.879},
        {'name': 'Gera', 'lat': 50.8772301, 'lng': 12.0796208, 'PAM_Mittelwert': 1.573},
        {'name': 'Halle', 'lat': 51.4825041, 'lng': 11.9705452, 'PAM_Mittelwert': 1.515},
        {'name': 'Dresden', 'lat': 51.0493286, 'lng': 13.7381437, 'PAM_Mittelwert': 1.461},
        {'name': 'Reichenbach', 'lat': 50.6219793, 'lng': 12.305088373514671, 'PAM_Mittelwert': 2.049},
        {'name': 'Dessau', 'lat': 51.8309956, 'lng': 12.2430723, 'PAM_Mittelwert': 1.465},
        {'name': 'Ansbach', 'lat': 49.3028611, 'lng': 10.5722288, 'PAM_Mittelwert': 1.933},
        {'name': 'Bamberg', 'lat': 49.8916044, 'lng': 10.8868478, 'PAM_Mittelwert': 1.433},
        {'name': 'Würzburg', 'lat': 49.79245, 'lng': 9.932966, 'PAM_Mittelwert': 1.808},
        {'name': 'Hirschau', 'lat': 49.5445912, 'lng': 11.9464314, 'PAM_Mittelwert': 2.129},
        {'name': 'Weiden', 'lat': 49.8068258, 'lng': 7.3007004, 'PAM_Mittelwert': 2.016},
        {'name': 'Ingolstadt', 'lat': 48.7630165, 'lng': 11.4250395, 'PAM_Mittelwert': 2.041},
        {'name': 'Regensburg', 'lat': 49.0195333, 'lng': 12.0974869, 'PAM_Mittelwert': 1.886},
        {'name': 'München', 'lat': 48.1371079, 'lng': 11.5753822, 'PAM_Mittelwert': 1.922},
        {'name': 'Passau', 'lat': 48.5748229, 'lng': 13.4609744, 'PAM_Mittelwert': 2.009},
        {'name': 'Trostberg', 'lat': 48.0321101, 'lng': 12.5654359, 'PAM_Mittelwert': 1.893},
        {'name': 'Farchant', 'lat': 47.5306769, 'lng': 11.1127989, 'PAM_Mittelwert': 1.957},
        {'name': 'Augsburg', 'lat': 48.3668041, 'lng': 10.8986971, 'PAM_Mittelwert': 2.102},
        {'name': 'Calw', 'lat': 48.7112108, 'lng': 8.7452043, 'PAM_Mittelwert': 1.692},
        {'name': 'Kaufbeuren', 'lat': 47.8803788, 'lng': 10.622246, 'PAM_Mittelwert': 1.803},
        {'name': 'Ulm', 'lat': 48.3974003, 'lng': 9.9934336, 'PAM_Mittelwert': 2.017},
        {'name': 'Balingen', 'lat': 48.2737512, 'lng': 8.8557862, 'PAM_Mittelwert': 1.875},
        {'name': 'Rudersberg', 'lat': 48.8831782, 'lng': 9.528413, 'PAM_Mittelwert': 1.795},
        {'name': 'Blindheim', 'lat': 48.631766, 'lng': 10.6185962, 'PAM_Mittelwert': 1.92},
        {'name': 'Waldshut', 'lat': 47.672925, 'lng': 8.2204166, 'PAM_Mittelwert': 1.351},
        {'name': 'Steinen', 'lat': 50.5739599, 'lng': 7.8104924, 'PAM_Mittelwert': 1.672},
        {'name': 'Bräunlingen', 'lat': 47.9300645, 'lng': 8.448329, 'PAM_Mittelwert': 1.784},
        {'name': 'Ravensburg', 'lat': 47.7811014, 'lng': 9.612468, 'PAM_Mittelwert': 1.843},
        {'name': 'Tuttlingen', 'lat': 47.9844315, 'lng': 8.8186606, 'PAM_Mittelwert': 1.639},
        {'name': 'Ohlsbach', 'lat': 48.4316699, 'lng': 7.9939024, 'PAM_Mittelwert': 1.808}]

    local_situational_means = json.load(
        open("../data/local_means_situational_intergenerational.json", 'r', encoding='utf-8'))


    for i, entry in enumerate(template):
        template[i]['PAM_Mittelwert'] = local_situational_means[entry['name']]['PAM-Wert_WSS']

    values = []

    for k in local_situational_means:
        values.append(local_situational_means[k]['PAM-Wert_WSS'])

    print(values)

    values = [entry for entry in values if not math.isnan(entry)]
    median = np.median(values)

    # Erstes Quartil (Q1)
    q1 = np.percentile(values, 25)

    # Drittes Quartil (Q3)
    q3 = np.percentile(values, 75)

    print(f"Median: {median}")
    print(f"Erstes Quartil (Q1): {q1}")
    print(f"Drittes Quartil (Q3): {q3}")
    #print(json.dumps(template, ensure_ascii=False, indent=2))
import plotly.express as px
import pandas as pd

if __name__ == "__main__":
    '''import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    # Ihre Daten als DataFrame
    data = pd.DataFrame([
        {'name': 'Alt Duvenstedt', 'lat': 54.3586037, 'lng': 9.6437579, 'PAM_Mittelwert': 1.216},
        {'name': 'Bad Segeberg', 'lat': 53.9422672, 'lng': 10.3137943, 'PAM_Mittelwert': 1.332},
        {'name': 'Flensburg', 'lat': 54.7833021, 'lng': 9.4333264, 'PAM_Mittelwert': 1.598},
        # ... weitere Einträge
    ])

    # Entfernen Sie Zeilen mit NaN-Werten im PAM_Mittelwert
    data = data.dropna(subset=['PAM_Mittelwert'])

    # Scatter-Geo-Plot erstellen
    fig = go.Figure(data=go.Scattergeo(
        lon=data['lng'],
        lat=data['lat'],
        text=data['name'],
        mode='markers',
        marker=dict(
            size=8,
            opacity=0.8,
            reversescale=True,
            autocolorscale=False,
            symbol='circle',
            line=dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale='Blues',
            cmin=data['PAM_Mittelwert'].min(),
            color=data['PAM_Mittelwert'],
            cmax=data['PAM_Mittelwert'].max(),
            colorbar_title="PAM Mittelwert"
        )))

    # Fügen Sie Layout-Optionen hinzu, um nur Deutschland anzuzeigen
    fig.update_geos(
        projection_type="mercator",
        lonaxis=dict(range=[5, 16]),
        lataxis=dict(range=[47, 56])
    )

    fig.update_layout(
        title='PAM Mittelwerte in verschiedenen Städten Deutschlands',
        geo=dict(
            scope='europe',
            projection_type='mercator',
            showland=True,
            landcolor="rgb(250, 250, 250)"
        )
    )

    fig.show()
'''

    import re

    text = """
    var cities = [
            {name: 'Alt Duvenstedt', lat: 54.3586037, lng: 9.6437579, PAM_Mittelwert: 1.216},
            {name: 'Bad Segeberg', lat: 53.9422672, lng: 10.3137943, PAM_Mittelwert: 1.332},
            {name: 'Flensburg', lat: 54.7833021, lng: 9.4333264, PAM_Mittelwert: 1.598},
            {name: 'Lohne', lat: 52.665257, lng: 8.2363523, PAM_Mittelwert: 1.785},
            {name: 'Oldenburg', lat: 53.1389753, lng: 8.2146017, PAM_Mittelwert: 1.377},
            {name: 'Lüneburg', lat: 53.248706, lng: 10.407855, PAM_Mittelwert: 1.632},
            {name: 'Neustadt am Rübenberge', lat: 52.5055135, lng: 9.4635826, PAM_Mittelwert: 1.781},
            {name: 'Rostock', lat: 54.0924445, lng: 12.1286127, PAM_Mittelwert: 1.237},
            {name: 'Schwerin', lat: 53.6288297, lng: 11.4148038, PAM_Mittelwert: 1.185},
            {name: 'Stralsund', lat: 54.3096314, lng: 13.0820846, PAM_Mittelwert: 1.008},
            {name: 'Bergen', lat: 49.7808936, lng: 7.4176059, PAM_Mittelwert: 1.641},
            {name: 'Pasewalk', lat: 53.5053677, lng: 13.9889049, PAM_Mittelwert: 1.192},
            {name: 'Frankfurt an der Oder', lat: 52.3412273, lng: 14.549452, PAM_Mittelwert: 1.1995},
            {name: 'Fürstenwalde', lat: 50.76058, lng: 13.8681537, PAM_Mittelwert: NaN},
            {name: 'Potsdam', lat: 52.4009309, lng: 13.0591397, PAM_Mittelwert: 1.084},
            {name: 'Pritzwalk', lat: 53.1492896, lng: 12.1761903, PAM_Mittelwert: 1.404},
            {name: 'Lüderitz', lat: 52.5084647, lng: 11.7427093, PAM_Mittelwert: NaN},
            {name: 'Brandenburg an der Havel', lat: 52.4108261, lng: 12.5497933, PAM_Mittelwert: NaN},
            {name: 'Neuruppin', lat: 52.9243859, lng: 12.8092919, PAM_Mittelwert: 1.224},
            {name: 'Borken', lat: 51.8443183, lng: 6.8582247, PAM_Mittelwert: 1.245},
            {name: 'Hagen', lat: 51.3582945, lng: 7.473296, PAM_Mittelwert: 0.968},
            {name: 'Gütersloh', lat: 51.9063997, lng: 8.3782078, PAM_Mittelwert: 0.957},
            {name: 'Horn-Bad Meinberg', lat: 51.8801277, lng: 8.9731695, PAM_Mittelwert: 0.962},
            {name: 'Drolshagen', lat: 51.0239917, lng: 7.7740693, PAM_Mittelwert: 1.185},
            {name: 'Halberstadt', lat: 51.8953514, lng: 11.0520563, PAM_Mittelwert: 0.929},
            {name: 'Hildesheim', lat: 52.1521636, lng: 9.9513046, PAM_Mittelwert: 1.528},
            {name: 'Northeim', lat: 51.76438235, lng: 9.858328873964005, PAM_Mittelwert: 1.338},
            {name: 'Magdeburg', lat: 52.1315889, lng: 11.6399609, PAM_Mittelwert: 1.193},
            {name: 'Bergisch-Gladbach', lat: 50.9929303, lng: 7.1277379, PAM_Mittelwert: 1.4093939393939394},
            {name: 'Düren', lat: 50.8031684, lng: 6.4820806, PAM_Mittelwert: 1.5053333333333332},
            {name: 'Troisdorf', lat: 50.8153071, lng: 7.1593271, PAM_Mittelwert: 1.3366666666666667},
            {name: 'Krefeld', lat: 51.3331205, lng: 6.5623343, PAM_Mittelwert: 1.428666666666667},
            {name: 'Mönchengladbach', lat: 51.1947131, lng: 6.4353792, PAM_Mittelwert: 1.3775757575757575},
            {name: 'Montabaur', lat: 50.4362219, lng: 7.8302494, PAM_Mittelwert: 1.402},
            {name: 'Schweich', lat: 49.8224303, lng: 6.7515418, PAM_Mittelwert: 1.4916666666666665},
            {name: 'Wittlich', lat: 49.9850353, lng: 6.88844, PAM_Mittelwert: 1.0712121212121213},
            {name: 'Altenkirchen', lat: 50.6880109, lng: 7.6477412, PAM_Mittelwert: 1.4120000000000001},
            {name: 'Heidelberg', lat: 49.4093582, lng: 8.694724, PAM_Mittelwert: 1.5276190476190477},
            {name: 'Kaiserslautern', lat: 49.4432174, lng: 7.7689951, PAM_Mittelwert: 1.3433333333333335},
            {name: 'Erbach', lat: 48.3274603, lng: 9.8913803, PAM_Mittelwert: 1.8303333333333338},
            {name: 'Reinheim', lat: 49.8364879, lng: 8.8238238, PAM_Mittelwert: 1.5473333333333334},
            {name: 'Kirkel', lat: 49.2833031, lng: 7.2333295, PAM_Mittelwert: 1.3793333333333333},
            {name: 'Merzig', lat: 49.4427023, lng: 6.6374902, PAM_Mittelwert: 1.6922222222222223},
            {name: 'Mainz', lat: 50.0012314, lng: 8.2762513, PAM_Mittelwert: 1.2022727272727272},
            {name: 'Heilbronn', lat: 49.142291, lng: 9.218655, PAM_Mittelwert: 1.6505555555555558},
            {name: 'Frankfurt am Main', lat: 50.1106444, lng: 8.6820917, PAM_Mittelwert: 1.409},
            {name: 'Kleve', lat: 51.7854839, lng: 6.131367415330141, PAM_Mittelwert: 1.5483333333333331},
            {name: 'Homberg', lat: 50.6407001, lng: 8.1058112, PAM_Mittelwert: 1.1543333333333332},
            {name: 'Kassel', lat: 51.3154546, lng: 9.4924096, PAM_Mittelwert: 1.3566666666666667},
            {name: 'Bad Nauheim', lat: 50.376802999999995, lng: 8.7476036068774, PAM_Mittelwert: 1.4946666666666666},
            {name: 'Büdingen', lat: 50.2972353, lng: 9.0990829, PAM_Mittelwert: 1.5166666666666668},
            {name: 'Gießen', lat: 50.5862066, lng: 8.6742306, PAM_Mittelwert: 1.5603333333333333},
            {name: 'Ulrichstein', lat: 50.5759667, lng: 9.1929639, PAM_Mittelwert: 2.0416666666666665},
            {name: 'Hofbieber', lat: 50.5932038, lng: 9.8708724, PAM_Mittelwert: 1.3563636363636362},
            {name: 'Erfurt', lat: 50.9777974, lng: 11.0287364, PAM_Mittelwert: 1.177},
            {name: 'Heilbad Heiligenstadt', lat: 51.3756186, lng: 10.138224, PAM_Mittelwert: 1.3280952380952382},
            {name: 'Sondershausen', lat: 51.3666041, lng: 10.8668419, PAM_Mittelwert: 1.7993333333333332},
            {name: 'Gera', lat: 50.8772301, lng: 12.0796208, PAM_Mittelwert: 1.3813333333333333},
            {name: 'Halle', lat: 51.4825041, lng: 11.9705452, PAM_Mittelwert: 1.5277777777777777},
            {name: 'Dresden', lat: 51.0493286, lng: 13.7381437, PAM_Mittelwert: 1.288181818181818},
            {name: 'Reichenbach', lat: 50.6219793, lng: 12.305088373514671, PAM_Mittelwert: 1.8946666666666665},
            {name: 'Dessau', lat: 51.8309956, lng: 12.2430723, PAM_Mittelwert: 1.20625},
            {name: 'Ansbach', lat: 49.3028611, lng: 10.5722288, PAM_Mittelwert: 1.6703030303030304},
            {name: 'Bamberg', lat: 49.8916044, lng: 10.8868478, PAM_Mittelwert: 1.3239393939393942},
            {name: 'Würzburg', lat: 49.79245, lng: 9.932966, PAM_Mittelwert: 1.774444444444444},
            {name: 'Hirschau', lat: 49.5445912, lng: 11.9464314, PAM_Mittelwert: 1.9413333333333334},
            {name: 'Weiden', lat: 49.8068258, lng: 7.3007004, PAM_Mittelwert: 1.858},
            {name: 'Ingolstadt', lat: 48.7630165, lng: 11.4250395, PAM_Mittelwert: 1.8936666666666668},
            {name: 'Regensburg', lat: 49.0195333, lng: 12.0974869, PAM_Mittelwert: 1.7163636363636363},
            {name: 'München', lat: 48.1371079, lng: 11.5753822, PAM_Mittelwert: 1.6676666666666666},
            {name: 'Passau', lat: 48.5748229, lng: 13.4609744, PAM_Mittelwert: 2.009333333333333},
            {name: 'Trostberg', lat: 48.0321101, lng: 12.5654359, PAM_Mittelwert: 1.7296666666666667},
            {name: 'Farchant', lat: 47.5306769, lng: 11.1127989, PAM_Mittelwert: 1.9576666666666669},
            {name: 'Augsburg', lat: 48.3668041, lng: 10.8986971, PAM_Mittelwert: 2.102},
            {name: 'Calw', lat: 48.7112108, lng: 8.7452043, PAM_Mittelwert: 1.7277777777777779},
            {name: 'Kaufbeuren', lat: 47.8803788, lng: 10.622246, PAM_Mittelwert: 1.6713333333333331},
            {name: 'Ulm', lat: 48.3974003, lng: 9.9934336, PAM_Mittelwert: 1.8793939393939392},
            {name: 'Balingen', lat: 48.2737512, lng: 8.8557862, PAM_Mittelwert: 1.784},
            {name: 'Rudersberg', lat: 48.8831782, lng: 9.528413, PAM_Mittelwert: 1.7021212121212121},
            {name: 'Blindheim', lat: 48.631766, lng: 10.6185962, PAM_Mittelwert: 1.8412121212121215},
            {name: 'Waldshut', lat: 47.672925, lng: 8.2204166, PAM_Mittelwert: 1.1823333333333335},
            {name: 'Steinen', lat: 50.5739599, lng: 7.8104924, PAM_Mittelwert: 1.5972222222222223},
            {name: 'Bräunlingen', lat: 47.9300645, lng: 8.448329, PAM_Mittelwert: 1.5686666666666667},
            {name: 'Ravensburg', lat: 47.7811014, lng: 9.612468, PAM_Mittelwert: 1.6315000000000002},
            {name: 'Tuttlingen', lat: 47.9844315, lng: 8.8186606, PAM_Mittelwert: 1.4557575757575756},
            {name: 'Ohlsbach', lat: 48.4316699, lng: 7.9939024, PAM_Mittelwert: 1.6236363636363635}
        ];
    """

    result = re.findall(r'PAM_Mittelwert: ([\d\.]+)', text)


    def median(data):
        n = len(data)
        data.sort()
        mid = n // 2  # floor division
        if n % 2 == 0:  # even
            return (data[mid - 1] + data[mid]) / 2
        else:  # odd
            return data[mid]


    def quartiles(data):
        n = len(data)
        data.sort()
        Q2 = median(data)

        lower_half = data[:n // 2]
        upper_half = data[-(n // 2):]

        Q1 = median(lower_half)
        Q3 = median(upper_half)

        return Q1, Q2, Q3


    data = [float(x) for x in
            ['1.216', '1.332', '1.598', '1.785', '1.377', '1.632', '1.781', '1.237', '1.185', '1.008', '1.641', '1.192',
             '1.1995', '1.084', '1.404', '1.224', '1.245', '0.968', '0.957', '0.962', '1.185', '0.929', '1.528',
             '1.338', '1.193', '1.4093939393939394', '1.5053333333333332', '1.3366666666666667', '1.428666666666667',
             '1.3775757575757575', '1.402', '1.4916666666666665', '1.0712121212121213', '1.4120000000000001',
             '1.5276190476190477', '1.3433333333333335', '1.8303333333333338', '1.5473333333333334',
             '1.3793333333333333', '1.6922222222222223', '1.2022727272727272', '1.6505555555555558', '1.409',
             '1.5483333333333331', '1.1543333333333332', '1.3566666666666667', '1.4946666666666666',
             '1.5166666666666668', '1.5603333333333333', '2.0416666666666665', '1.3563636363636362', '1.177',
             '1.3280952380952382', '1.7993333333333332', '1.3813333333333333', '1.5277777777777777',
             '1.288181818181818', '1.8946666666666665', '1.20625', '1.6703030303030304', '1.3239393939393942',
             '1.774444444444444', '1.9413333333333334', '1.858', '1.8936666666666668', '1.7163636363636363',
             '1.6676666666666666', '2.009333333333333', '1.7296666666666667', '1.9576666666666669', '2.102',
             '1.7277777777777779', '1.6713333333333331', '1.8793939393939392', '1.784', '1.7021212121212121',
             '1.8412121212121215', '1.1823333333333335', '1.5972222222222223', '1.5686666666666667',
             '1.6315000000000002', '1.4557575757575756', '1.6236363636363635']]
    Q1, Q2, Q3 = quartiles(data)
    print(f"Q1: {Q1}")
    print(f"Q2 (Median): {Q2}")
    print(f"Q3: {Q3}")



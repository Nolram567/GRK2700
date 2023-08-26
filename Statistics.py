import math

import pandas as pd
import numpy as np

class Statistics:

    df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])
    mydata = df.to_dict("records")

    @staticmethod
    def calculate_local_means_intragenerational(r=True):
        localValues = []
        for i in Statistics.mydata:
            filtered_dict = {k: v for k, v in i.items() if k.startswith("PAM") or k == "ort" or k == "GENERATION"}
            filtered_dict2 = {k: v for k, v in filtered_dict.items() if
                              type(v) == str or (type(v) == float and not math.isnan(v))}
            filtered_dict3 = {k: v for k, v in filtered_dict2.items() if k.startswith("PAM")}
            if len(filtered_dict3) > 0:
                if r:
                    localValues.append({'ort': filtered_dict2['ort'], 'Generation': filtered_dict2['GENERATION'],
                                        'Mean_PAM': round(sum(filtered_dict3.values()) / len(filtered_dict3), 3)})
                else:
                    localValues.append({'ort': filtered_dict2['ort'], 'Generation': filtered_dict2['GENERATION'],
                                        'Mean_PAM': sum(filtered_dict3.values()) / len(filtered_dict3)})
            else:
                localValues.append(
                    {'ort': filtered_dict2['ort'], 'Generation': filtered_dict2['GENERATION'], 'Mean_PAM': math.nan})

        return localValues

    @staticmethod
    def calculate_local_mean_intergenerational(r=True):
        intragenerationalMeans = Statistics.calculate_local_means_intragenerational(r=False)
        resultSet = []
        ticked = []
        for i in intragenerationalMeans:
            if i['ort'] not in ticked:
                ort_to_filter = i['ort']
                filtered_list = [entry for entry in intragenerationalMeans if entry['ort'] == ort_to_filter]
                #print(filtered_list)
                mean_pam_values = [entry['Mean_PAM'] for entry in filtered_list if not math.isnan(entry['Mean_PAM'])]
                if len(mean_pam_values) > 0:
                    average_mean_pam = sum(mean_pam_values) / len(mean_pam_values)
                    if r:
                        resultSet.append({'ort': i['ort'], 'Mean_PAM': round(average_mean_pam, 3)})
                    else:
                        resultSet.append({'ort': i['ort'], 'Mean_PAM': average_mean_pam})
                    ticked.append(ort_to_filter)
                else:
                    resultSet.append({'ort': i['ort'], 'Mean_PAM': math.nan})
                    ticked.append(ort_to_filter)
        return resultSet

    @staticmethod
    def calculate_national_mean_PAM(r=True):
        intergenerationalMeans=Statistics.calculate_local_mean_intergenerational(r=False)
        mean_pam_values = [entry['Mean_PAM'] for entry in intergenerationalMeans if not math.isnan(entry['Mean_PAM'])]
        if r:
            return round(sum(mean_pam_values) / len(mean_pam_values), 3)
        else:
            return sum(mean_pam_values) / len(mean_pam_values)


    @staticmethod
    def calculate_means_for_citys(city_name):
        df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

        df = df[df['ort'] == city_name]

        df = df.drop(columns=["gid", "ort", "Informant"])

        mean_df = df.groupby('GENERATION').mean(numeric_only=True).reset_index()

        mean_all = mean_df.mean(numeric_only=True)

        return [mean_df, mean_all]
    @staticmethod
    def calculate_means_for_regions(city_name):
        df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])

        region = df[df['ort'] == city_name]['Region'].iloc[0]
        df = df[df['Region'] == region]

        df = df.drop(columns=["gid", "ort", "Informant"])

        mean_df = df.groupby('GENERATION').mean(numeric_only=True).reset_index()

        mean_all = mean_df.mean(numeric_only=True)

        return [mean_df, mean_all]

    @staticmethod
    def calculate_mean_local_generation(df):

        df = df[[col for col in df.columns if 'PAM-Wert' in col or 'GENERATION' in col]]

        mean_pam_values = df.groupby('GENERATION').mean()

        mean_pam_values = mean_pam_values.mean(axis=1)

        return mean_pam_values

    @staticmethod
    def calculate_mean_PAM(s):

        s = s.dropna()

        s = s.drop(columns=["Kontrollwert_WSS", "Kontrollwert_NOSO", "Kontrollwert_NOT", "Kontrollwert_INT", "Kontrollwert_FG", "Kontrollwert_WSD"])

        # Berechne den Mittelwert
        mean_PAM = s.mean()

        # Erstelle eine neue Series mit dem berechneten Mittelwert
        mean_series = pd.Series({'Mean_PAM': mean_PAM})

        return mean_series

    @staticmethod
    def calculate_regional_general_PAM_intergenerational(d: dict) -> dict:
        filtered_values = [value for key, value in d.items() if
                           not key.startswith('Kontrollwert') and not np.isnan(value)]
        average_pam = np.mean(filtered_values)
        return average_pam

if __name__ == '__main__':

    print(Statistics.calculate_national_mean_PAM(r=True))
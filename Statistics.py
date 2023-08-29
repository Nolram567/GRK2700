import math
import time

import pandas as pd
import numpy as np

class Statistics:

    df = pd.read_csv('d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])
    mydata = df.to_dict("records")

    @staticmethod
    def calculate_local_means_intragenerational(r=True):
        localValues = []
        for i in Statistics.mydata:
            filtered_dict = {k: v for k, v in i.items() if k.startswith("PAM") or k == "ort" or k == "Region" or k == "GENERATION"}
            filtered_dict2 = {k: v for k, v in filtered_dict.items() if
                              type(v) == str or (type(v) == float and not math.isnan(v))}
            filtered_dict3 = {k: v for k, v in filtered_dict2.items() if k.startswith("PAM")}
            if len(filtered_dict3) > 0:
                if r:
                    localValues.append({'ort': filtered_dict2['ort'], 'Generation': filtered_dict2['GENERATION'],
                                        'Region': filtered_dict2['Region'],
                                        'Mean_PAM': round(sum(filtered_dict3.values()) / len(filtered_dict3), 3)})
                else:
                    localValues.append({'ort': filtered_dict2['ort'], 'Generation': filtered_dict2['GENERATION'],
                                        'Region': filtered_dict2['Region'],
                                        'Mean_PAM': sum(filtered_dict3.values()) / len(filtered_dict3)})
            else:
                localValues.append(
                    {'ort': filtered_dict2['ort'], 'Generation': filtered_dict2['GENERATION'],
                     'Region': filtered_dict2['Region'], 'Mean_PAM': math.nan})


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
                        resultSet.append({'ort': i['ort'], 'Region': i['Region'], 'Mean_PAM': round(average_mean_pam, 3)})
                    else:
                        resultSet.append({'ort': i['ort'], 'Region': i['Region'], 'Mean_PAM': average_mean_pam})
                    ticked.append(ort_to_filter)
                else:
                    resultSet.append({'ort': i['ort'], 'Region': i['Region'], 'Mean_PAM': math.nan})
                    ticked.append(ort_to_filter)


        returnSet = {}

        for d in resultSet:
            ort = d['ort']
            temp = {k: v for k, v in d.items() if k != 'ort'}
            returnSet[ort] = temp

        return returnSet

    @staticmethod
    def calculate_local_situational_means(r=True, internal=True):
        local_situational_means = []
        ticked = []
        for i in Statistics.mydata:
            if i['ort'] not in ticked:
                filtered_list = [entry for entry in Statistics.mydata if entry['ort'] == i['ort']]

                PAM_Variations = ['PAM-Wert_WSS', 'PAM-Wert_NOSO', 'PAM-Wert_NOT', 'PAM-Wert_INT', 'PAM-Wert_FG', 'PAM-Wert_WSD']
                temp = {'ort': i['ort']}
                for j in PAM_Variations:
                    temp[f'values_{j}'] = []
                    for d in filtered_list:
                        temp[f'values_{j}'].append({k: v for k, v in d.items() if k.startswith(j)}[j])

                #print(temp)
                for key, value_list in temp.items():
                    if isinstance(value_list, list):
                        temp[key] = [v for v in value_list if not math.isnan(v)]
                #print(temp)
                if r:
                    local_situational_means.append({'ort': i['ort'], 'Region': i['Region'],
                                                    'PAM-Wert_WSS': round(sum(temp['values_PAM-Wert_WSS']) / len(
                                                        temp['values_PAM-Wert_WSS']), 3) if len(
                                                        temp['values_PAM-Wert_WSS']) != 0 else math.nan,
                                                    'PAM-Wert_NOSO': round(sum(temp['values_PAM-Wert_NOSO']) / len(
                                                        temp['values_PAM-Wert_NOSO']), 3) if len(
                                                        temp['values_PAM-Wert_NOSO']) != 0 else math.nan,
                                                    'PAM-Wert_NOT': round(sum(temp['values_PAM-Wert_NOT']) / len(
                                                        temp['values_PAM-Wert_NOT']), 3) if len(
                                                        temp['values_PAM-Wert_NOT']) != 0 else math.nan,
                                                    'PAM-Wert_INT': round(sum(temp['values_PAM-Wert_INT']) / len(
                                                        temp['values_PAM-Wert_INT']), 3) if len(
                                                        temp['values_PAM-Wert_INT']) != 0 else math.nan,
                                                    'PAM-Wert_FG': round(sum(temp['values_PAM-Wert_FG']) / len(
                                                        temp['values_PAM-Wert_FG']), 3) if len(
                                                        temp['values_PAM-Wert_FG']) != 0 else math.nan,
                                                    'PAM-Wert_WSD': round(sum(temp['values_PAM-Wert_WSD']) / len(
                                                        temp['values_PAM-Wert_WSD']), 3) if len(
                                                        temp['values_PAM-Wert_WSD']) != 0 else math.nan
                                                    })
                else:
                    local_situational_means.append({'ort': i['ort'], 'Region': i['Region'],
                                                    'PAM-Wert_WSS': sum(temp['values_PAM-Wert_WSS']) / len(
                                                        temp['values_PAM-Wert_WSS']) if len(
                                                        temp['values_PAM-Wert_WSS']) != 0 else math.nan,
                                                    'PAM-Wert_NOSO': sum(temp['values_PAM-Wert_NOSO']) / len(
                                                        temp['values_PAM-Wert_NOSO']) if len(
                                                        temp['values_PAM-Wert_NOSO']) != 0 else math.nan,
                                                    'PAM-Wert_NOT': sum(temp['values_PAM-Wert_NOT']) / len(
                                                        temp['values_PAM-Wert_NOT']) if len(
                                                        temp['values_PAM-Wert_NOT']) != 0 else math.nan,
                                                    'PAM-Wert_INT': sum(temp['values_PAM-Wert_INT']) / len(
                                                        temp['values_PAM-Wert_INT']) if len(
                                                        temp['values_PAM-Wert_INT']) != 0 else math.nan,
                                                    'PAM-Wert_FG': sum(temp['values_PAM-Wert_FG']) / len(
                                                        temp['values_PAM-Wert_FG']) if len(
                                                        temp['values_PAM-Wert_FG']) != 0 else math.nan,
                                                    'PAM-Wert_WSD': sum(temp['values_PAM-Wert_WSD']) / len(
                                                        temp['values_PAM-Wert_WSD']) if len(
                                                        temp['values_PAM-Wert_WSD']) != 0 else math.nan
                                                    })
                ticked.append(i['ort'])

        if internal:
            return_set = {}

            for d in local_situational_means:
                ort = d['ort']
                restliche_daten = {k: v for k, v in d.items() if k != 'ort'}
                return_set[ort] = restliche_daten

            return return_set

        return local_situational_means

    @staticmethod
    def calculate_national_mean(r=True):
        intergenerationalMeans=Statistics.calculate_local_mean_intergenerational(r=False)
        mean_pam_values = [entry['Mean_PAM'] for entry in intergenerationalMeans if not math.isnan(entry['Mean_PAM'])]
        if r:
            return round(sum(mean_pam_values) / len(mean_pam_values), 3)
        else:
            return sum(mean_pam_values) / len(mean_pam_values)

    @staticmethod
    def calculate_regional_means_intergenerational(r=True):
        local_means = Statistics.calculate_local_means_intragenerational(r=False)
        regional_values = []
        ticked = []

        for i in local_means:
            if i['Region'] not in ticked:
                filtered_list = [entry for entry in local_means if entry['Region'] == i['Region']]
                #print(filtered_list)
                mean_pam_values = [entry['Mean_PAM'] for entry in filtered_list if not math.isnan(entry['Mean_PAM'])]
                #print(mean_pam_values)
                if r:
                    if len(mean_pam_values) > 0:
                        regional_values.append({'Region': i['Region'], 'Mean_PAM': round(sum(mean_pam_values) / len(mean_pam_values), 3)})
                    else:
                        regional_values.append({'Region': i['Region'], 'Mean_PAM': math.nan})
                else:
                    if len(mean_pam_values) > 0:
                        regional_values.append({'Region': i['Region'], 'Mean_PAM': sum(mean_pam_values) / len(mean_pam_values)})
                    else:
                        regional_values.append({'Region': i['Region'], 'Mean_PAM': math.nan})
                ticked.append(i['Region'])

        returnSet = {}

        for d in regional_values:
            Region = d['Region']
            temp = {k: v for k, v in d.items() if k != 'Region'}
            returnSet[Region] = temp

        return returnSet

    @staticmethod
    def calculate_regional_situational_means(r=True, internal=True):
        local_means = Statistics.calculate_local_situational_means(r=False, internal=False)

        ticked = []
        regional_situational_means = []
        for i in local_means:
            if i['Region'] not in ticked:
                filtered_list = [entry for entry in local_means if entry['Region'] == i['Region']]

                PAM_Variations = ['PAM-Wert_WSS', 'PAM-Wert_NOSO', 'PAM-Wert_NOT', 'PAM-Wert_INT', 'PAM-Wert_FG',
                                  'PAM-Wert_WSD']
                temp = {'Region': i['Region']}
                for j in PAM_Variations:
                    temp[f'values_{j}'] = []
                    for d in filtered_list:
                        temp[f'values_{j}'].append({k: v for k, v in d.items() if k.startswith(j)}[j])

                # print(temp)
                for key, value_list in temp.items():
                    if isinstance(value_list, list):
                        temp[key] = [v for v in value_list if not math.isnan(v)]
                # print(temp)
                if r:
                    regional_situational_means.append({'Region': i['Region'],
                                                    'PAM-Wert_WSS': round(sum(temp['values_PAM-Wert_WSS']) / len(
                                                        temp['values_PAM-Wert_WSS']), 3) if len(
                                                        temp['values_PAM-Wert_WSS']) != 0 else math.nan,
                                                    'PAM-Wert_NOSO': round(sum(temp['values_PAM-Wert_NOSO']) / len(
                                                        temp['values_PAM-Wert_NOSO']), 3) if len(
                                                        temp['values_PAM-Wert_NOSO']) != 0 else math.nan,
                                                    'PAM-Wert_NOT': round(sum(temp['values_PAM-Wert_NOT']) / len(
                                                        temp['values_PAM-Wert_NOT']), 3) if len(
                                                        temp['values_PAM-Wert_NOT']) != 0 else math.nan,
                                                    'PAM-Wert_INT': round(sum(temp['values_PAM-Wert_INT']) / len(
                                                        temp['values_PAM-Wert_INT']), 3) if len(
                                                        temp['values_PAM-Wert_INT']) != 0 else math.nan,
                                                    'PAM-Wert_FG': round(sum(temp['values_PAM-Wert_FG']) / len(
                                                        temp['values_PAM-Wert_FG']), 3) if len(
                                                        temp['values_PAM-Wert_FG']) != 0 else math.nan,
                                                    'PAM-Wert_WSD': round(sum(temp['values_PAM-Wert_WSD']) / len(
                                                        temp['values_PAM-Wert_WSD']), 3) if len(
                                                        temp['values_PAM-Wert_WSD']) != 0 else math.nan
                                                    })
                else:
                    regional_situational_means.append({'Region': i['Region'],
                                                    'PAM-Wert_WSS': sum(temp['values_PAM-Wert_WSS']) / len(
                                                        temp['values_PAM-Wert_WSS']) if len(
                                                        temp['values_PAM-Wert_WSS']) != 0 else math.nan,
                                                    'PAM-Wert_NOSO': sum(temp['values_PAM-Wert_NOSO']) / len(
                                                        temp['values_PAM-Wert_NOSO']) if len(
                                                        temp['values_PAM-Wert_NOSO']) != 0 else math.nan,
                                                    'PAM-Wert_NOT': sum(temp['values_PAM-Wert_NOT']) / len(
                                                        temp['values_PAM-Wert_NOT']) if len(
                                                        temp['values_PAM-Wert_NOT']) != 0 else math.nan,
                                                    'PAM-Wert_INT': sum(temp['values_PAM-Wert_INT']) / len(
                                                        temp['values_PAM-Wert_INT']) if len(
                                                        temp['values_PAM-Wert_INT']) != 0 else math.nan,
                                                    'PAM-Wert_FG': sum(temp['values_PAM-Wert_FG']) / len(
                                                        temp['values_PAM-Wert_FG']) if len(
                                                        temp['values_PAM-Wert_FG']) != 0 else math.nan,
                                                    'PAM-Wert_WSD': sum(temp['values_PAM-Wert_WSD']) / len(
                                                        temp['values_PAM-Wert_WSD']) if len(
                                                        temp['values_PAM-Wert_WSD']) != 0 else math.nan
                                                    })
            ticked.append(i['Region'])

        if internal:
            return_set = {}

            for d in regional_situational_means:
                region = d['Region']
                restliche_daten = {k: v for k, v in d.items() if k != 'Region'}
                return_set[region] = restliche_daten

            return return_set

        return regional_situational_means


if __name__ == '__main__':

    #print(Statistics.calculate_local_mean_intergenerational()['Alt Duvenstedt']['Mean_PAM'])
    #print([entry for entry in Statistics.calculate_local_means_intragenerational() if entry['ort'] == 'Alt Duvenstedt'])
    #print(Statistics.calculate_regional_means_intergenerational()['Nordniederdeutsch']['Mean_PAM'])
    #print(Statistics.calculate_regional_situational_means(internal=False))
    print(Statistics.calculate_regional_means_intergenerational())
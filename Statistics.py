import math
import json
from typing import Tuple, Any, List

import pandas as pd


class Statistics:
    """
    I decided to conduct all Calculations without excessive use of pandas or numpy since all calculations are rather basic
     and working with standard python contributes to traceability and understandability (at least for me since iam more used to it).
     Regular users of pandas and numpy probably perceive this class as cumbersome and bulky.

     This class can be reused if the dataset enlarges. Just call Statistics.serialize(). The correct functioning of the
      class assumes the unchanged file names and the original folder structure.
    """

    df = pd.read_csv('data/d-mess-sel-2.csv', sep=';', na_values=['-', 'n.d.'])
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
                mean_pam_values = [entry['Mean_PAM'] for entry in filtered_list if not math.isnan(entry['Mean_PAM'])]
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

                for key, value_list in temp.items():
                    if isinstance(value_list, list):
                        temp[key] = [v for v in value_list if not math.isnan(v)]
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
                remainder = {k: v for k, v in d.items() if k != 'Region'}
                return_set[region] = remainder

            return return_set

        return regional_situational_means

    @staticmethod
    def calculate_regional_situational_means_intragenerational(r=True):
        regional_situational_means_intra = []
        ticked = []
        for i in Statistics.mydata:
            if i['Region'] not in ticked:
                filtered_list = [entry for entry in Statistics.mydata if entry['Region'] == i['Region']]
                for n in ['jung', 'mittel', 'alt']:
                    filtered_list2 = [entry for entry in filtered_list if entry['GENERATION'] == n]
                    PAM_Variations = ['PAM-Wert_WSS', 'PAM-Wert_NOSO', 'PAM-Wert_NOT', 'PAM-Wert_INT', 'PAM-Wert_FG',
                                      'PAM-Wert_WSD']

                    temp = {'Region': i['Region'], 'Generation': n}
                    for j in PAM_Variations:
                        temp[f'values_{j}'] = []
                        for d in filtered_list2:
                            temp[f'values_{j}'].append({k: v for k, v in d.items() if k.startswith(j)}[j])

                    for key, value_list in temp.items():
                        if isinstance(value_list, list):
                            temp[key] = [v for v in value_list if not math.isnan(v)]

                    if r:
                        regional_situational_means_intra.append({'Region': i['Region'], 'Generation': n,
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
                        regional_situational_means_intra.append({'Region': i['Region'], 'Generation': n,
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
        return regional_situational_means_intra

    @staticmethod
    def serialize():
        statistic_data = {
            "local_means_intragenerational": Statistics.calculate_local_means_intragenerational(),
            "local_means_intergenerational": Statistics.calculate_local_mean_intergenerational(),
            "local_means_situational_intergenerational": Statistics.calculate_local_situational_means(),

            "regional_means_intergenerational": Statistics.calculate_regional_means_intergenerational(),
            "regional_means_situational_intergenerational": Statistics.calculate_regional_situational_means(),
            "regional_means_situational_intragenerational": Statistics.calculate_regional_situational_means_intragenerational()
        }
        for k, v in statistic_data.items():
            with open(f'data/{k}.json', 'w', encoding='utf-8') as f:
                json.dump(v, f, ensure_ascii=False)

    @staticmethod
    def deserialization() -> tuple[json, ...]:
        local_means_intergenerational = json.load(
            open("data/local_means_intergenerational.json", 'r', encoding='utf-8'))
        local_mean_intragenerational = json.load(open("data/local_means_intragenerational.json", 'r', encoding='utf-8'))
        local_situational_means = json.load(
            open("data/local_means_situational_intergenerational.json", 'r', encoding='utf-8'))
        regional_means_intergenerational = json.load(
            open("data/regional_means_intergenerational.json", 'r', encoding='utf-8'))
        regional_situational_means = json.load(
            open("data/regional_means_situational_intergenerational.json", 'r', encoding='utf-8'))
        regional_situational_means_intragenerational = json.load(
            open("data/regional_means_situational_intragenerational.json", 'r', encoding='utf-8'))

        return local_means_intergenerational, local_mean_intragenerational, local_situational_means,\
            regional_means_intergenerational, regional_situational_means, regional_situational_means_intragenerational
    @staticmethod
    def pick_runtime_data(city_name, region, local_means_intergenerational, local_mean_intragenerational,
                         regional_means_intergenerational, regional_situational_means_intragenerational) -> tuple[
        Any, Any, Any, Any, Any, list[Any]]:
       local_mean = local_means_intergenerational[city_name]['Mean_PAM']
       local_mean_young = \
       [entry for entry in local_mean_intragenerational if entry['ort'] == city_name and entry['Generation'] == 'jung'][
           0]['Mean_PAM']
       local_mean_intermediate = [entry for entry in local_mean_intragenerational if
                                  entry['ort'] == city_name and entry['Generation'] == 'mittel'][0]['Mean_PAM']
       local_mean_old = \
       [entry for entry in local_mean_intragenerational if entry['ort'] == city_name and entry['Generation'] == 'alt'][
           0]['Mean_PAM']
       regional_mean = regional_means_intergenerational[region]['Mean_PAM']
       regional_mean_intra = [entry for entry in regional_situational_means_intragenerational if
                              entry['Region'] == region]

       return local_mean, local_mean_young, local_mean_intermediate, local_mean_old, regional_mean, regional_mean_intra

if __name__ == '__main__':

    Statistics.serialize()


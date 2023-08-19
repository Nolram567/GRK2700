import pandas as pd
import numpy as np

class Statistics:

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
    print("success")
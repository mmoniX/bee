from project import BeeData

if __name__ == '__main__':
    try:
        feature = BeeData()
        df = feature.run()
        df.to_csv('readings.csv', sep=',', index=False)
        print(df.head())
        print(df.describe())
    except Exception as ex:
        print(f"Error due to {ex}")
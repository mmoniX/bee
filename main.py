from project import df


if __name__ == '__main__':
    try:
        df.to_csv('readings.csv', sep=',', index=False)
        print(df.describe())
    except Exception as ex:
        print(f"Error due to {ex}")
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("bestSelling_games.csv")

print("Первые 5 строк датасета:")
print(df.head())

print("\nИнформация о датасете:")
print(df.info())

print("\nОсновные статистики:")
print(df.describe())


print("\nПропущенные значения:")
print(df.isnull().sum())

df = df.dropna()

df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
df = df.dropna(subset=["release_date"])

df["release_year"] = df["release_date"].dt.year

df = df[df["estimated_downloads"] < 500_000_000]

print("\nДанные после очистки:")
print(df.info())


plt.figure()
plt.hist(df["rating"], bins=15)
plt.xlabel("Рейтинг")
plt.ylabel("Количество игр")
plt.title("Распределение рейтингов игр")
plt.show()


plt.figure()
plt.scatter(df["estimated_downloads"], df["rating"])
plt.xlabel("Количество загрузок")
plt.ylabel("Рейтинг")
plt.title("Зависимость рейтинга от популярности")
plt.show()


plt.figure()
df.groupby("release_year")["rating"].mean().plot()
plt.xlabel("Год выхода")
plt.ylabel("Средний рейтинг")
plt.title("Средний рейтинг игр по годам")
plt.show()


median_downloads = df["estimated_downloads"].median()

popular_games = df[df["estimated_downloads"] >= median_downloads]["rating"]
less_popular_games = df[df["estimated_downloads"] < median_downloads]["rating"]

popular_mean = popular_games.mean()
less_popular_mean = less_popular_games.mean()

print("\nСредний рейтинг популярных игр:", popular_mean)
print("Средний рейтинг менее популярных игр:", less_popular_mean)

print("\nОписание популярных игр:")
print(popular_games.describe())

print("\nОписание менее популярных игр:")
print(less_popular_games.describe())

difference = abs(popular_mean - less_popular_mean)

print("\nАбсолютная разница средних рейтингов:", difference)

if difference < 0.1:
    print(
        "\nВывод: различие средних рейтингов незначительно. "
        "Гипотеза подтверждена."
    )
else:
    print(
        "\nВывод: наблюдается заметное различие средних рейтингов. "
        "Гипотеза поставлена под сомнение."
    )
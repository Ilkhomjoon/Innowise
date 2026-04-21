from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import config


def read_postgres_table(spark, table_name):
    return spark.read \
        .format("jdbc") \
        .option("url", config.DB_URL) \
        .option("dbtable", table_name) \
        .option("user", config.DB_USER) \
        .option("password", config.DB_PASS) \
        .option("driver", "org.postgresql.Driver") \
        .load()

def main():
    spark = SparkSession.builder \
        .appName("Pagila_PySpark_Project") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
        .getOrCreate()

    print("Loading data from database")
    
    category = read_postgres_table(spark, "category")
    film_category = read_postgres_table(spark, "film_category")
    film = read_postgres_table(spark, "film")
    actor = read_postgres_table(spark, "actor")
    film_actor = read_postgres_table(spark, "film_actor")
    inventory = read_postgres_table(spark, "inventory")
    rental = read_postgres_table(spark, "rental")
    payment = read_postgres_table(spark, "payment")
    customer = read_postgres_table(spark, "customer")
    address = read_postgres_table(spark, "address")
    city = read_postgres_table(spark, "city")

    print("Data Loaded\n")

    print("--- Task 1: Number of movies in each category ---")
    task1_df = film_category.join(category, "category_id") \
        .groupBy(category["name"]) \
        .agg(F.count("film_id").alias("movie_count")) \
        .orderBy(F.col("movie_count").desc())
    task1_df.show()

    print("--- Task 2: 10 actors whose movies rented the most ---")
    task2_df = rental.join(inventory, "inventory_id") \
        .join(film_actor, "film_id") \
        .join(actor, "actor_id") \
        .groupBy(actor["actor_id"], actor["first_name"], actor["last_name"]) \
        .agg(F.count("rental_id").alias("rental_count")) \
        .orderBy(F.col("rental_count").desc()) \
        .limit(10)
    task2_df.show()

    print("--- Task 3: Category of movies on which the most money was spent ---")
    task3_df = payment.join(rental, "rental_id") \
        .join(inventory, "inventory_id") \
        .join(film_category, "film_id") \
        .join(category, "category_id") \
        .groupBy(category["name"]) \
        .agg(F.sum("amount").alias("total_spent")) \
        .orderBy(F.col("total_spent").desc()) \
        .limit(1)
    task3_df.show()

    print("--- Task 4: Names of movies that are not in the inventory ---")
    task4_df = film.join(inventory, "film_id", "left_anti") \
        .select("title")
    task4_df.show()

    print("--- Task 5: Top 3 actors in 'Children' category (including ties) ---")
    children_movies = category.filter(F.col("name") == "Children") \
        .join(film_category, "category_id") \
        .join(film_actor, "film_id") \
        .join(actor, "actor_id") \
        .groupBy(actor["first_name"], actor["last_name"]) \
        .agg(F.count("film_id").alias("movie_count"))

    window_spec = Window.orderBy(F.col("movie_count").desc())
    task5_df = children_movies.withColumn("rank", F.dense_rank().over(window_spec)) \
        .filter(F.col("rank") <= 3) \
        .drop("rank")
    task5_df.show()

    print("--- Task 6: Cities with active/inactive customers sorted by inactive descending ---")
    task6_df = customer.join(address, "address_id") \
        .join(city, "city_id") \
        .groupBy(city["city"]) \
        .agg(
            F.sum(F.when(F.col("active") == 1, 1).otherwise(0)).alias("active_customers"),
            F.sum(F.when(F.col("active") == 0, 1).otherwise(0)).alias("inactive_customers")
        ) \
        .orderBy(F.col("inactive_customers").desc())
    task6_df.show()

    print("--- Task 7: Highest total rental hours category in cities starting with 'a' and containing '-' ---")
    rental_with_hours = rental.withColumn(
        "rental_hours", 
        (F.unix_timestamp("return_date") - F.unix_timestamp("rental_date")) / 3600
    )

    base_df = rental_with_hours.join(inventory, "inventory_id") \
        .join(film_category, "film_id") \
        .join(category, "category_id") \
        .join(customer, "customer_id") \
        .join(address, "address_id") \
        .join(city, "city_id")

    task7_a_df = base_df.filter(F.lower(F.col("city")).startswith("a")) \
        .groupBy(category["name"]) \
        .agg(F.sum("rental_hours").alias("total_hours")) \
        .orderBy(F.col("total_hours").desc()) \
        .limit(1)
    print("Cities starting with 'A':")
    task7_a_df.show()

    task7_dash_df = base_df.filter(F.col("city").contains("-")) \
        .groupBy(category["name"]) \
        .agg(F.sum("rental_hours").alias("total_hours")) \
        .orderBy(F.col("total_hours").desc()) \
        .limit(1)
    print("Cities containing '-':")
    task7_dash_df.show()

if __name__ == "__main__":
    main()
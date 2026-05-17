import psycopg2 as ps
import psqlConfig as config
from psycopg2 import sql

def connect():
    return ps.connect(database = config.database, user = config.user, password = config.password)

def counts_per_stop_for_bird(connection, year: int, bird_name: str):
    table = sql.Identifier(f"year_{year}")

    #convert everything to text just in case
    select_stop_columns = sql.SQL(
        "stop_1::text AS stop_1, stop_2::text AS stop_2, stop_3::text AS stop_3, stop_4::text AS stop_4, "
        "stop_5::text AS stop_5, stop_6::text AS stop_6, stop_7::text AS stop_7, stop_8::text AS stop_8, "
        "stop_9::text AS stop_9, stop_10::text AS stop_10, stop_11::text AS stop_11, stop_12::text AS stop_12, "
        "stop_13::text AS stop_13, stop_14::text AS stop_14, stop_15::text AS stop_15, stop_16::text AS stop_16, "
        "stop_17::text AS stop_17"
    )

    unnest_array_elements = sql.SQL(
        "COALESCE(stop_1,''), COALESCE(stop_2,''), COALESCE(stop_3,''), COALESCE(stop_4,''), "
        "COALESCE(stop_5,''), COALESCE(stop_6,''), COALESCE(stop_7,''), COALESCE(stop_8,''), "
        "COALESCE(stop_9,''), COALESCE(stop_10,''), COALESCE(stop_11,''), COALESCE(stop_12,''), "
        "COALESCE(stop_13,''), COALESCE(stop_14,''), COALESCE(stop_15,''), COALESCE(stop_16,''), "
        "COALESCE(stop_17,'')"
    )

    query = sql.SQL("""
    WITH bird_row AS (
      SELECT
        {select_stop_columns}
      FROM {table}
      WHERE bird_name = %s
      LIMIT 1
    )
    SELECT
      unnested_with_ord.ordinality AS stop_num,
      COALESCE(NULLIF(unnested_with_ord.value, '')::int, 0) AS count
    FROM bird_row,
      unnest(ARRAY[{unnest_array_elements}]) WITH ORDINALITY AS unnested_with_ord(value, ordinality)
    ORDER BY unnested_with_ord.ordinality;
    """).format(select_stop_columns = select_stop_columns, table = table, unnest_array_elements = unnest_array_elements)

    with connection.cursor() as cursor:
        cursor.execute(query, (bird_name,))
        return cursor.fetchall()

def total_sightings_per_bird(connection, year: int):
    table = sql.Identifier(f"year_{year}")

    safe_expressions = [
        sql.SQL("COALESCE(NULLIF(TRIM({column}::text), '')::int, 0)").format(column = sql.Identifier(f"stop_{i}")) for i in range(1, 18)
    ]
    
    per_row_total = sql.SQL(" + ").join(safe_expressions)

    query = sql.SQL("""
    SELECT
      bird_name,
      MAX(({per_row_total})) AS total_sightings
    FROM {table}
    GROUP BY bird_name
    ORDER BY total_sightings DESC, bird_name;
    """).format(per_row_total = per_row_total, table = table)

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def main():
    connection = connect()
    year = 2000
    bird = 'American Crow'

    print(f"Counts per stop for '{bird}' in {year}:")
    rows = counts_per_stop_for_bird(connection, year, bird)
    for stop, count in rows:
        print(f"{stop}: {count}")

    print(f"\nTop birds by total sightings in {year}")
    totals = total_sightings_per_bird(connection, year)
    for bird_name, total in totals[:20]:
        print(f"{bird_name}: {total}")

    connection.close()

if __name__ == "__main__":
    main()
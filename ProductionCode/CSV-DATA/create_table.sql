DO $$
BEGIN
    FOR range3 IN 2020..2025 LOOP
    EXECUTE format('DROP TABLE IF EXISTS %I', 'year_' || range3);
        EXECUTE format(
            'CREATE TABLE %I (
                bird_name TEXT,
                stop_1 INT,
                stop_2 INT,
                stop_3 INT,
                stop_4 INT,
                stop_5 INT,
                stop_6 INT,
                stop_7 INT,
                stop_8 INT,
                stop_9 INT,
                stop_10 INT,
                stop_11 INT,
                stop_12 INT,
                stop_13 INT,
                stop_14 INT,
                stop_15 INT,
                stop_16 INT,
                stop_17 INT
            )',
            'year_' || range3
        );
    END LOOP;

    FOR range2 IN 2008..2018 LOOP
    EXECUTE format('DROP TABLE IF EXISTS %I', 'year_' || range2);
        EXECUTE format(
            'CREATE TABLE %I (
                bird_name TEXT,
                stop_1 INT,
                stop_2 INT,
                stop_3 INT,
                stop_4 INT,
                stop_5 INT,
                stop_6 INT,
                stop_7 INT,
                stop_8 INT,
                stop_9 INT,
                stop_10 INT,
                stop_11 INT,
                stop_12 INT,
                stop_13 INT,
                stop_14 INT,
                stop_15 INT,
                stop_16 INT,
                stop_17 INT
            )',
            'year_' || range2
    );
    END LOOP;

    FOR range1 IN 2000..2004 LOOP
    EXECUTE format('DROP TABLE IF EXISTS %I', 'year_' || range1);
        EXECUTE format(
            'CREATE TABLE %I (
                bird_name TEXT,
                stop_1 INT,
                stop_2 INT,
                stop_3 INT,
                stop_4 INT,
                stop_5 INT,
                stop_6 INT,
                stop_7 INT,
                stop_8 INT,
                stop_9 INT,
                stop_10 INT,
                stop_11 INT,
                stop_12 INT,
                stop_13 INT,
                stop_14 INT,
                stop_15 INT,
                stop_16 INT,
                stop_17 INT
            )',
            'year_' || range1
    );
    END LOOP;
END
$$

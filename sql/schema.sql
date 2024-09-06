CREATE TABLE IF NOT EXISTS pokemon (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    type1 VARCHAR(50),
    type2 VARCHAR(50),
    total INT,
    hp INT,
    attack INT,
    defense INT,
    speed INT,
    sp_atk INT,
    sp_def INT,
    generation INT,
    description TEXT
);
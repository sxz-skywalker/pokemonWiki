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

CREATE TABLE IF NOT EXISTS forum (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    category TINYINT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    content TEXT NOT NULL
);
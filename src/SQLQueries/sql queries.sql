
-- Obtener la banca para cada archivo 
SELECT
    activo,
    cod_activo,
    banca
FROM catalogo_activos
JOIN catalogo_banca
    ON catalogo_activos.cod_banca = catalogo_banca.cod_banca;

-- Obtener el perfil de riesgo maximo para cada act
SELECT
    activo,
    cod_activo,
    perfil_riesgo
FROM (
    SELECT
        activo,
        cod_activo,
        perfil_riesgo,
        ROW_NUMBER() OVER (PARTITION BY cod_activo ORDER BY perfil_riesgo DESC) AS rn
    FROM catalogo_activos
    JOIN cat_perfil_riesgo
        ON catalogo_activos.cod_activo = cat_perfil_riesgo.cod_perfil_riesgo
) AS subquery
WHERE rn = 1;

-- Consolidar la información en una sola tabla
CREATE TABLE tabla_consolidada (
    activo VARCHAR(255),
    cod_activo INTEGER,
    perfil_riesgo VARCHAR(255),
    banca VARCHAR(255)
);


INSERT INTO tabla_consolidada
SELECT
    catalogo_activos.activo,
    a.cod_activo,
    cat_perfil_riesgo.perfil_riesgo,
    catalogo_banca.banca
FROM catalogo_activos
JOIN cat_perfil_riesgo
    ON catalogo_activos.cod_activo = cat_perfil_riesgo.cod_perfil_riesgo
JOIN catalogo_banca 
    ON catalogo_activos.cod_banca = catalogo_banca.cod_banca;


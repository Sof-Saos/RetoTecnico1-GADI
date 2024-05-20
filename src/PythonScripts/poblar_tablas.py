import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="db_challengetalentob",
    user="postgres",
    password="Popipo",
    host="localhost"
)

def poblar_tabla(nombre_tabla, archivo_csv):
    cursor = conn.cursor()

    with open(archivo_csv, 'r') as f:
        datos = f.readlines()

    datos.pop(0)
    datos_convertidos = []
    for fila in datos:
        fila = fila.strip().split(',')
        datos_convertidos.append(tuple(fila))

    cursor.executemany(
        f"""INSERT INTO {nombre_tabla} VALUES (%s, %s)""",
        datos_convertidos
    )
    conn.commit()
    cursor.close()


import psycopg2

def poblar_historico_aba_macroactivos(archivo_csv):
    cursor = conn.cursor()
    with open(archivo_csv, 'r') as f:
        datos = f.readlines()

    datos.pop(0)

    datos_convertidos = []
    for fila in datos:
        fila = fila.strip().split(',')


        fila[3] = str(fila[3])

        try:

            if fila[5] == '':
                fila[5] = 0
            else:
                fila[5] = int(fila[5])
        except ValueError:
            fila[5] = None

        datos_convertidos.append(tuple(fila))

    try:
        cursor.executemany(
            """INSERT INTO historico_aba_macroactivos VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            datos_convertidos
        )
        conn.commit()
    except psycopg2.errors.InvalidTextRepresentation as e:
        print(f"Error al insertar fila: {e}")

    cursor.close()
    conn.close()




poblar_tabla('cat_perfil_riesgo', 'cat_perfil_riesgo.csv')
poblar_tabla('catalogo_activos', 'catalogo_activos.csv')
poblar_tabla('catalogo_banca', 'catalogo_banca.csv')

poblar_historico_aba_macroactivos('historico_aba_macroactivos.csv')

conn.close()


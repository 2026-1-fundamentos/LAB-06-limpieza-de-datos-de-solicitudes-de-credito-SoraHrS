"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import os
    import pandas as pd

    input_path = "files/input/solicitudes_de_credito.csv"
    output_path = "files/output/solicitudes_de_credito.csv"
 
    df = pd.read_csv(input_path, sep=";", index_col=0)
    df = df.dropna()
 
    for col in ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"]:
        df[col] = df[col].str.lower().str.strip()
    for col in ["idea_negocio", "línea_credito"]:
        df[col] = (df[col].str.replace("-", " ", regex=False)
                          .str.replace("_", " ", regex=False)
                          .str.replace(r"\s+", " ", regex=True).str.strip())
 
    df["barrio"] = (df["barrio"].str.lower()
                    .str.replace("-", " ", regex=False)
                    .str.replace("_", " ", regex=False))
 
    df["monto_del_credito"] = (df["monto_del_credito"]
        .str.replace(r"[\$,\s]", "", regex=True)
        .str.replace(r"\.00$", "", regex=True)
        .str.replace(".", "", regex=False).astype(float).astype(int))
 
    f1 = pd.to_datetime(df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce")
    f2 = pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    df["fecha_de_beneficio"] = f1.fillna(f2)
 
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)
    df = df.drop_duplicates()
 
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, sep=";", index=False)
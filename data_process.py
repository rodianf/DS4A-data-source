import pandas as pd
import glob

# List all files in folder with gz extension
extension = 'csvs/*.gz'
all_files = glob.glob(extension)

# Read and concatenate dataframes
df = pd.concat([pd.read_csv(f, sep='\t', header=0, na_values='-')
                for f in all_files], ignore_index=True)

# Filter data from Atlántico and Barranquilla and Soledad
df = df[(df['Departamento'] == 'ATLÁNTICO') &
        ((df['Municipio'] == 'BARRANQUILLA (CT)') |
        (df['Municipio'] == 'SOLEDAD'))].reset_index(drop=True)

# Reset index
#df = df.reset_index(drop=True)

# Neighbourhood data load
neigh_data = pd.read_csv("barrios.csv")

# Inner join with Neighbourhood data to filter
df = pd.merge(df, neigh_data, how='inner', on='Barrio')

# ===========
# Clase sitio
csitio = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9eDm9TuopO6ysMo4wvjNN2F26lb3zaYHCIMQH17g3utZ8xrkgU73VqebPnnJhY_jHJrOjhwzmyH1s/pub?gid=1999911815&single=true&output=csv"

sitio_data = pd.read_csv(csitio)

# Inner join with Neighbourhood data to filter
df = pd.merge(df, sitio_data, how='left', on='Clase de sitio')

# ======================
# Drop unused columns
df = df.drop(columns = ['Departamento', 'Barrio', 'Zona', 'Estado civil', 'Código DANE','Clase de sitio'])

# Rename Barrio column
df = df.rename(columns={'Barrio_Nombre':'Barrio',
			'Nueva clase':'Clase de sitio'})

# Exporta data to csv
df.to_csv('datos.csv', index=False, index_label=False)

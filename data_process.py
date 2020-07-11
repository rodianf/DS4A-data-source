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

# Drop unused columns
df = df.drop(columns = ['Departamento', 'Barrio', 'Zona', 'Estado civil', 'Código DANE'])

# Rename Barrio column
df = df.rename(columns={'Barrio_Nombre':'Barrio'})

# Exporta data to csv
df.to_csv('datos.csv', index=False, index_label=False)

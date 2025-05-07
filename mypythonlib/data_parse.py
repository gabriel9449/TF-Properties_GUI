from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

def insect_plant_preproc(database):
    database = database.drop(columns=['Reference', 'Ingredient ID', 'Unnamed: 7', 'Unnamed: 29', 'Tag'])
    database['Ingredient 2 (Location)'] = database['Ingredient 2 (Location)'].fillna(0)
    database['Ingredient 2 (Location)'] = database['Ingredient 2 (Location)'].astype('int64')

    database['Ingredient sources'] = database['Ingredient sources'].fillna('ND')
    database['Species'] = database['Species'].fillna('ND')
    database['Stage'] = database['Stage'].fillna('ND')
    database['Part'] = database['Part'].fillna('ND')
    database['Treatment'] = database['Treatment'].fillna('ND')
    database['Defatting treatment'] = database['Defatting treatment'].fillna('ND')
    database['Drying '] = database['Drying '].fillna('ND')

    database['Ashes'] = database['Ashes'].replace('ND',0)
    database['Insoluble dietary fiber'] = database['Insoluble dietary fiber'].replace('ND',0)
    database['Soluble dietary fiber'] = database['Soluble dietary fiber'].replace('ND',0)

    database['WHC '] = database['WHC '].fillna(0)
    database['OHC'] = database['OHC'].fillna(0)
    database['FC'] = database['FC'].fillna(0)
    database['EC Oil'] = database['EC Oil'].fillna(0)
    database['EC H20'] = database['EC H20'].fillna(0)

    LE = LabelEncoder() 
    database['Ingredient sources'] = LE.fit_transform(database['Ingredient sources'])
    database['Mix'] = LE.fit_transform(database['Mix'])
    database['Species'] = LE.fit_transform(database['Species'])
    database['Stage'] = LE.fit_transform(database['Stage'])
    database['Part'] = LE.fit_transform(database['Part'])
    database['Treatment'] = LE.fit_transform(database['Treatment'])
    database['Defatting treatment'] = LE.fit_transform(database['Defatting treatment'])
    database['Drying '] = LE.fit_transform(database['Drying '])
    scaler = StandardScaler().fit(database)
    
    return database, scaler
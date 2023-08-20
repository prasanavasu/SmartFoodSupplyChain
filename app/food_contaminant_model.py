
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report



def food_contaminant(food,species,geno_type,month,state,ingred):
# Load the dataset
    data = pd.read_csv('outbreaks.csv')


    # In[113]:


    # Data preprocessing
    data = data.drop(["Location"], axis=1)  # Remove irrelevant column
    data = data.dropna()  # Drop rows with NaN values


    # In[114]:


    # Convert categorical variables to numerical using Label Encoding
    label_encoders = {}
    for column in ["Food", "Species", "Serotype/Genotype","Ingredient", "State"]:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le



    data = data.drop(["Illnesses"], axis=1)  # Remove irrelevant column


    # In[117]:


    data = data.drop(["Hospitalizations"], axis=1)  # Remove irrelevant column


    # In[118]:


    data = data.drop(["Fatalities"], axis=1)  # Remove irrelevant column


    # In[119]:


    data = data.drop(["Month"], axis=1)  # Remove irrelevant column


    # In[120]:


    # Define features and target variable
    X = data.drop(["Status"], axis=1)
    y = data["Status"]


    # In[121]:


    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # In[122]:


    # Initialize and train the model (Random Forest)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)


    # Predictions
    y_pred = model.predict(X_test)

    # Model evaluation
    accuracy = accuracy_score(y_test, y_pred)
    classification_rep = classification_report(y_test, y_pred)


    # New data for prediction (replace with actual data)
    new_data = pd.DataFrame({
    "Food": [food],
    "Species": [species],
    "Serotype/Genotype": [geno_type],
    "Month": [month],  # Replace with the appropriate month
    "State": [state],  # Replace with the appropriate state
    "Ingredient": [ingred],    # Replace with the appropriate ingredient
    # Add other features as needed
    })


    # In[106]:


    # Apply label encoding to categorical variables

    categorical_columns = ["Month", "State", "Ingredient","Serotype/Genotype","Species", "Food"]
    new_data_encoded = pd.get_dummies(new_data, columns=categorical_columns)

    new_data_encoded


    # In[107]:


    # Create a DataFrame with the same structure as X_train
    # new_data_encoded = pd.DataFrame(columns=X_train.columns, data=new_data)
    # new_data_encoded


    # In[108]:


    # Make predictions with the model
    predictions = model.predict(new_data_encoded)


    # In[109]:



    for i, prediction in enumerate(predictions):
        print(f"Prediction for input {i+1}: {'Contaminated' if prediction == 1 else 'Not Contaminated'}")
    return prediction


    # In[ ]:





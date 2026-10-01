from pathlib import Path
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

BASE_DIR=Path(__file__).resolve().parent.parent
df=pd.read_csv(BASE_DIR/"ml"/"data"/"students.csv")
features=["study_hours","attendance","previous_score"]
X_train,X_test,y_train,y_test=train_test_split(df[features],df["final_score"],test_size=.2,random_state=42)
model=LinearRegression().fit(X_train,y_train)
print(f"Test mean absolute error: {mean_absolute_error(y_test,model.predict(X_test)):.2f} points")
with (BASE_DIR/"backend"/"model"/"model.pkl").open("wb") as f: pickle.dump(model,f)
print("Saved backend/model/model.pkl")

# Student Performance Predictor
A small classroom project: **Frontend → Python prediction API → scikit-learn model**. It can run locally with Flask or deploy to Vercel.

It predicts a student's final score from study hours, attendance, and previous score. The dataset is synthetic and this is an educational demo, not a real academic decision system.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ml/train_model.py
python backend/app.py
```
Open http://127.0.0.1:5000

Windows PowerShell activation:
```powershell
.venv\Scripts\Activate.ps1
```

## Test API
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"study_hours":5,"attendance":85,"previous_score":72}'
```

## Structure
```text
frontend/       HTML/CSS/JavaScript
backend/        Flask API + saved ML model
ml/             training script + synthetic CSV
api/            Vercel Python prediction function
public/         Static frontend served by Vercel
deployment/     AWS EC2 guide
```

## Deploy to Vercel

The Vercel deployment serves the frontend from `public/` and exposes the model through `POST /api/predict`. The checked-in model is included with the Python function; training is not run during deployment.

1. Push this project to a Git provider supported by Vercel.
2. In Vercel, select **Add New → Project** and import the repository.
3. Keep the project root at the repository root. No build command or environment variables are required.
4. Deploy. Vercel detects the Python function from `api/predict.py` and installs runtime dependencies from the root `requirements.txt`.

You can also deploy from this directory with the Vercel CLI (`vercel`). The first run links the local project to your Vercel account; use `vercel --prod` for a production deployment.

Test the deployed API with:
```bash
curl -X POST https://YOUR-VERCEL-DOMAIN/api/predict -H "Content-Type: application/json" -d '{"study_hours":5,"attendance":85,"previous_score":72}'
```

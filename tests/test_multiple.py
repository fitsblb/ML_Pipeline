# test_multiple.py
import requests
import json

def test_multiple_predictions():
    # Different test cases for diabetes prediction
    test_cases = [
        {
            "name": "High Risk Patient",
            "data": {
                "Pregnancies": 6,
                "Glucose": 148,
                "BloodPressure": 72,
                "SkinThickness": 35,
                "Insulin": 0,
                "BMI": 33.6,
                "DiabetesPedigreeFunction": 0.627,
                "Age": 50
            }
        },
        {
            "name": "Low Risk Patient",
            "data": {
                "Pregnancies": 1,
                "Glucose": 85,
                "BloodPressure": 66,
                "SkinThickness": 29,
                "Insulin": 0,
                "BMI": 26.6,
                "DiabetesPedigreeFunction": 0.351,
                "Age": 31
            }
        },
        {
            "name": "Medium Risk Patient",
            "data": {
                "Pregnancies": 3,
                "Glucose": 120,
                "BloodPressure": 80,
                "SkinThickness": 25,
                "Insulin": 90,
                "BMI": 28.5,
                "DiabetesPedigreeFunction": 0.4,
                "Age": 45
            }
        },
        {
            "name": "Young Low Risk",
            "data": {
                "Pregnancies": 0,
                "Glucose": 95,
                "BloodPressure": 70,
                "SkinThickness": 20,
                "Insulin": 80,
                "BMI": 22.0,
                "DiabetesPedigreeFunction": 0.2,
                "Age": 25
            }
        }
    ]

    print("🩺 Testing Multiple Diabetes Predictions")
    print("=" * 50)

    for i, test in enumerate(test_cases, 1):
        try:
            response = requests.post(
                "http://localhost:8000/predict",
                headers={"Content-Type": "application/json"},
                data=json.dumps(test["data"]),
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result["prediction"][0]
                risk_level = "🔴 DIABETES RISK" if prediction == 1 else "🟢 NO DIABETES"
                
                print(f"\n{i}. {test['name']}")
                print(f"   Prediction: {risk_level}")
                print(f"   Confidence: {prediction}")
                print(f"   Key factors: Glucose={test['data']['Glucose']}, BMI={test['data']['BMI']}, Age={test['data']['Age']}")
            else:
                print(f"\n{i}. {test['name']}: ❌ Error {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"\n❌ Cannot connect to server. Is it running on http://localhost:8000?")
            break
        except Exception as e:
            print(f"\n{i}. {test['name']}: ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("Testing completed!")

if __name__ == "__main__":
    test_multiple_predictions()
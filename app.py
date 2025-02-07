from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# CORS Handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="Enter a valid integer")):
    """Classify the given number and return its properties."""
    try:
        # Properties
        properties = ["odd" if number % 2 else "even"]
        if is_prime(number):
            properties.append("prime")
        if is_perfect(number):
            properties.append("perfect")
        if is_armstrong(number):
            properties.append("armstrong")

        # Digit Sum
        digit_sum = sum(int(digit) for digit in str(number))

        # Fetch Fun Fact
        fun_fact_url = f"http://numbersapi.com/{number}"
        fun_fact = requests.get(fun_fact_url).text

        # Response JSON
        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact
        }
    except Exception as e:
        return {"error": True, "message": str(e)}

@app.get("/")
def health_check():
    return {"message": "API is running!"}


import math
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(abs(n))) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect_number(n: int) -> bool:
    if n <= 0:
        return False
    divisor_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisor_sum == n

def is_armstrong_number(n: int) -> bool:
    if n < 0:
        return False
    num_str = str(abs(n))
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == abs(n)

def generate_armstrong_fun_fact(number: int) -> str:
    num_str = str(abs(number))
    power = len(num_str)
    calculation = ' + '.join([f'{digit}^{power}' for digit in num_str])
    return f"{number} is an Armstrong number because {calculation} = {number}"

async def get_fun_fact(number: int) -> str:
    try:
        if is_armstrong_number(number):
            return generate_armstrong_fun_fact(number)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://numbersapi.com/{number}")
            return response.text if response.status_code == 200 else "No fun fact available"
    except Exception:
        return "No fun fact available"

@app.get("/api/classify-number")
async def classify_number(number: str = Query(None, description="Number to classify")):
    if number is None:
        return JSONResponse(
            status_code=400,
            content={
                "error": True,
                "message": "Number parameter is required",
                "number": None
            }
        )
    
    try:
        number = int(number)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={
                "number": number,
                "error": True,
                "message": "Invalid number format"
            }
        )
    
    properties = []
    if number % 2 == 1:
        properties.append("odd")
    else:
        properties.append("even")
    
    if is_prime(number):
        properties.append("prime")
    if is_perfect_number(number):
        properties.append("perfect")
    if is_armstrong_number(number):
        properties.append("armstrong")
    
    digit_sum = sum(int(digit) for digit in str(abs(number)))
    fun_fact = await get_fun_fact(number)
    
    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect_number(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

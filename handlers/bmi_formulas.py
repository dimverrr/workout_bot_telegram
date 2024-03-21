def metric_bmi(height_m, weight_kg):
    bmi = weight_kg / (height_m) ** 2
    return interpret_bmi(round(bmi, 1))


def imperial_bmi(height_in, weight_lb):
    weight_kg = weight_lb * 0.453592
    height_m = height_in * 0.0254
    return metric_bmi(height_m, weight_kg)


def interpret_bmi(bmi):
    if bmi < 18.5:
        return f"Your BMI is {bmi}. Underweight."
    elif 18.5 <= bmi < 24.9:
        return f"Your BMI is {bmi}. Normal weight."
    elif 25 <= bmi < 29.9:
        return f"Your BMI is {bmi}. Overweight."
    else:
        return f"Your BMI is {bmi}. Obese."

#!/usr/bin/env python3
"""
Synthetic Data Generator for Shiksha Radar MVP
Generates NCERT Class 5 Mathematics aligned synthetic data with student archetypes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

CONCEPT_HIERARCHY = {
    "Fractions": {
        "sub_concepts": {
            "denominator_handling": {
                "questions_per_difficulty": 3,
                "error_types": ["denominator_handling", "simplification", "arithmetic"],
                "error_probs": [0.6, 0.2, 0.2]
            },
            "simplification": {
                "questions_per_difficulty": 3,
                "error_types": ["simplification", "denominator_handling", "arithmetic"],
                "error_probs": [0.5, 0.3, 0.2]
            },
            "addition": {
                "questions_per_difficulty": 3,
                "error_types": ["denominator_handling", "arithmetic", "careless"],
                "error_probs": [0.4, 0.4, 0.2]
            },
            "subtraction": {
                "questions_per_difficulty": 2,
                "error_types": ["denominator_handling", "arithmetic", "careless"],
                "error_probs": [0.4, 0.4, 0.2]
            },
            "multiplication": {
                "questions_per_difficulty": 2,
                "error_types": ["simplification", "arithmetic", "conceptual"],
                "error_probs": [0.4, 0.3, 0.3]
            },
            "comparison": {
                "questions_per_difficulty": 2,
                "error_types": ["denominator_handling", "conceptual", "careless"],
                "error_probs": [0.3, 0.5, 0.2]
            }
        }
    },
    "Decimals": {
        "sub_concepts": {
            "place_value": {
                "questions_per_difficulty": 3,
                "error_types": ["conceptual", "arithmetic", "careless"],
                "error_probs": [0.5, 0.3, 0.2]
            },
            "addition_subtraction": {
                "questions_per_difficulty": 3,
                "error_types": ["decimal_placement", "arithmetic", "careless"],
                "error_probs": [0.5, 0.3, 0.2]
            },
            "multiplication": {
                "questions_per_difficulty": 2,
                "error_types": ["decimal_placement", "arithmetic", "conceptual"],
                "error_probs": [0.5, 0.3, 0.2]
            },
            "division": {
                "questions_per_difficulty": 2,
                "error_types": ["decimal_placement", "arithmetic", "conceptual"],
                "error_probs": [0.5, 0.3, 0.2]
            }
        }
    },
    "Algebra": {
        "sub_concepts": {
            "patterns": {
                "questions_per_difficulty": 3,
                "error_types": ["conceptual", "careless", "arithmetic"],
                "error_probs": [0.4, 0.3, 0.3]
            },
            "variables": {
                "questions_per_difficulty": 3,
                "error_types": ["conceptual", "formula_selection", "arithmetic"],
                "error_probs": [0.5, 0.3, 0.2]
            },
            "equations": {
                "questions_per_difficulty": 3,
                "error_types": ["sign_error", "formula_selection", "arithmetic"],
                "error_probs": [0.4, 0.3, 0.3]
            },
            "sign_rules": {
                "questions_per_difficulty": 2,
                "error_types": ["sign_error", "conceptual", "careless"],
                "error_probs": [0.6, 0.2, 0.2]
            }
        }
    },
    "Geometry": {
        "sub_concepts": {
            "2d_shapes": {
                "questions_per_difficulty": 3,
                "error_types": ["conceptual", "careless", "arithmetic"],
                "error_probs": [0.4, 0.3, 0.3]
            },
            "3d_shapes": {
                "questions_per_difficulty": 2,
                "error_types": ["conceptual", "careless", "arithmetic"],
                "error_probs": [0.4, 0.3, 0.3]
            },
            "area_perimeter": {
                "questions_per_difficulty": 3,
                "error_types": ["area_perimeter_confusion", "unit_conversion", "arithmetic"],
                "error_probs": [0.5, 0.2, 0.3]
            },
            "angles": {
                "questions_per_difficulty": 2,
                "error_types": ["conceptual", "arithmetic", "careless"],
                "error_probs": [0.4, 0.4, 0.2]
            },
            "symmetry": {
                "questions_per_difficulty": 2,
                "error_types": ["conceptual", "careless", "arithmetic"],
                "error_probs": [0.4, 0.3, 0.3]
            }
        }
    },
    "Measurement": {
        "sub_concepts": {
            "length": {
                "questions_per_difficulty": 3,
                "error_types": ["unit_conversion", "arithmetic", "careless"],
                "error_probs": [0.4, 0.4, 0.2]
            },
            "weight": {
                "questions_per_difficulty": 2,
                "error_types": ["unit_conversion", "arithmetic", "careless"],
                "error_probs": [0.4, 0.4, 0.2]
            },
            "capacity": {
                "questions_per_difficulty": 2,
                "error_types": ["unit_conversion", "arithmetic", "careless"],
                "error_probs": [0.4, 0.4, 0.2]
            },
            "time": {
                "questions_per_difficulty": 2,
                "error_types": ["unit_conversion", "arithmetic", "conceptual"],
                "error_probs": [0.4, 0.4, 0.2]
            }
        }
    },
    "Data_Handling": {
        "sub_concepts": {
            "tables": {
                "questions_per_difficulty": 2,
                "error_types": ["careless", "arithmetic", "conceptual"],
                "error_probs": [0.4, 0.4, 0.2]
            },
            "bar_graphs": {
                "questions_per_difficulty": 2,
                "error_types": ["conceptual", "careless", "arithmetic"],
                "error_probs": [0.5, 0.3, 0.2]
            },
            "pictographs": {
                "questions_per_difficulty": 2,
                "error_types": ["conceptual", "careless", "arithmetic"],
                "error_probs": [0.5, 0.3, 0.2]
            }
        }
    }
}

ARCHETYPES = {
    "fractions_struggler": {
        "name": "Student A",
        "description": "Fractions difficulty (high error rate only in Fractions, denominator-dominant)",
        "base_error_rates": {
            "Fractions": 0.45,
            "Decimals": 0.10,
            "Algebra": 0.10,
            "Geometry": 0.10,
            "Measurement": 0.10,
            "Data_Handling": 0.10
        },
        "dominant_errors": {
            "Fractions": ["denominator_handling", "simplification"]
        }
    },
    "algebra_struggler": {
        "name": "Student B",
        "description": "Algebra difficulty (sign errors + formula selection)",
        "base_error_rates": {
            "Fractions": 0.10,
            "Decimals": 0.10,
            "Algebra": 0.45,
            "Geometry": 0.10,
            "Measurement": 0.10,
            "Data_Handling": 0.10
        },
        "dominant_errors": {
            "Algebra": ["sign_error", "formula_selection"]
        }
    },
    "random_mistakes": {
        "name": "Student C",
        "description": "Random mistakes (moderate error rate across all concepts, no clear pattern)",
        "base_error_rates": {
            "Fractions": 0.25,
            "Decimals": 0.25,
            "Algebra": 0.25,
            "Geometry": 0.25,
            "Measurement": 0.25,
            "Data_Handling": 0.25
        },
        "dominant_errors": {}
    },
    "improving": {
        "name": "Student D",
        "description": "Improving over time (error rate decays across assessments)",
        "base_error_rates": {
            "Fractions": 0.35,
            "Decimals": 0.30,
            "Algebra": 0.30,
            "Geometry": 0.25,
            "Measurement": 0.25,
            "Data_Handling": 0.20
        },
        "dominant_errors": {},
        "improvement_rate": 0.15
    },
    "persistent": {
        "name": "Student E",
        "description": "Persistent difficulties (high error rate across all concepts, stable)",
        "base_error_rates": {
            "Fractions": 0.40,
            "Decimals": 0.38,
            "Algebra": 0.38,
            "Geometry": 0.35,
            "Measurement": 0.35,
            "Data_Handling": 0.30
        },
        "dominant_errors": {}
    },
    "on_track": {
        "name": "Student F",
        "description": "On track (low error rate everywhere)",
        "base_error_rates": {
            "Fractions": 0.05,
            "Decimals": 0.05,
            "Algebra": 0.05,
            "Geometry": 0.05,
            "Measurement": 0.05,
            "Data_Handling": 0.05
        },
        "dominant_errors": {}
    }
}

DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
DIFFICULTY_WEIGHTS = [0.4, 0.4, 0.2]
ERROR_TYPE_MODIFIER = {
    "easy": 0.7,
    "medium": 1.0,
    "hard": 1.4
}

QUESTION_TEMPLATES = {
    "Fractions": {
        "denominator_handling": [
            "Add {frac1} + {frac2}",
            "Subtract {frac1} - {frac2}",
            "Compare {frac1} and {frac2}",
            "Find equivalent fraction of {frac1} with denominator {denom}",
            "Simplify {frac1}"
        ],
        "simplification": [
            "Simplify {frac1} to lowest terms",
            "Reduce {frac1}",
            "Write {frac1} in simplest form"
        ],
        "addition": [
            "Add {frac1} + {frac2}",
            "Find the sum: {frac1} + {frac2}"
        ],
        "subtraction": [
            "Subtract {frac1} - {frac2}",
            "Find the difference: {frac1} - {frac2}"
        ],
        "multiplication": [
            "Multiply {frac1} × {frac2}",
            "Find the product: {frac1} × {frac2}"
        ],
        "comparison": [
            "Which is greater: {frac1} or {frac2}?",
            "Compare {frac1} and {frac2} using <, >, or ="
        ]
    },
    "Decimals": {
        "place_value": [
            "What is the place value of {digit} in {decimal}?",
            "Write {decimal} in expanded form",
            "Identify the tenths/hundredths digit in {decimal}"
        ],
        "addition_subtraction": [
            "Add {decimal1} + {decimal2}",
            "Subtract {decimal1} - {decimal2}"
        ],
        "multiplication": [
            "Multiply {decimal1} × {decimal2}",
            "Find {decimal1} × {decimal2}"
        ],
        "division": [
            "Divide {decimal1} ÷ {decimal2}",
            "Find {decimal1} ÷ {decimal2}"
        ]
    },
    "Algebra": {
        "patterns": [
            "Complete the pattern: {pattern}",
            "Find the next term: {pattern}",
            "What is the rule for this pattern: {pattern}?"
        ],
        "variables": [
            "If x = {val}, find the value of {expr}",
            "Evaluate {expr} when x = {val}",
            "Write an expression for: {word_problem}"
        ],
        "equations": [
            "Solve for x: {equation}",
            "Find x: {equation}",
            "What is the value of x in {equation}?"
        ],
        "sign_rules": [
            "Calculate: {signed_expr}",
            "Simplify: {signed_expr}",
            "Evaluate: {signed_expr}"
        ]
    },
    "Geometry": {
        "2d_shapes": [
            "How many sides does a {shape} have?",
            "Identify the shape: {description}",
            "Which of these is a {shape}?"
        ],
        "3d_shapes": [
            "How many faces/edges/vertices does a {shape} have?",
            "Identify the 3D shape: {description}",
            "Name the shape with {num} faces and {num} vertices"
        ],
        "area_perimeter": [
            "Find the area of a rectangle with length {l} cm and breadth {b} cm",
            "Find the perimeter of a square with side {s} cm",
            "A rectangle has area {a} sq cm and length {l} cm. Find its breadth."
        ],
        "angles": [
            "What type of angle is {deg}°?",
            "Find the missing angle: {angle_problem}",
            "Classify the angle: {deg}°"
        ],
        "symmetry": [
            "How many lines of symmetry does a {shape} have?",
            "Is the figure symmetric? (Yes/No)",
            "Draw the line of symmetry for {shape}"
        ]
    },
    "Measurement": {
        "length": [
            "Convert {val} m to cm",
            "Convert {val} km to m",
            "Add: {val1} m {val2} cm + {val3} m {val4} cm"
        ],
        "weight": [
            "Convert {val} kg to g",
            "Convert {val} g to kg",
            "Total weight: {val1} kg {val2} g + {val3} kg {val4} g"
        ],
        "capacity": [
            "Convert {val} L to mL",
            "Convert {val} mL to L",
            "Total capacity: {val1} L {val2} mL + {val3} L {val4} mL"
        ],
        "time": [
            "Convert {val} hours to minutes",
            "Convert {val} minutes to seconds",
            "What time is {val} minutes after {time}?"
        ]
    },
    "Data_Handling": {
        "tables": [
            "How many students scored between {range}?",
            "What is the total frequency in the table?",
            "Find the missing value in the table"
        ],
        "bar_graphs": [
            "Which category has the highest value?",
            "What is the value for {category}?",
            "How many more {cat1} than {cat2}?"
        ],
        "pictographs": [
            "If one symbol represents {val}, how many for {category}?",
            "Which category has {num} symbols?",
            "Total count represented by the pictograph"
        ]
    }
}

FRACTIONS_POOL = ["1/2", "1/3", "1/4", "2/3", "3/4", "2/5", "3/5", "4/5", "1/6", "5/6", "2/7", "3/7", "4/7", "5/7", "6/7"]
DECIMALS_POOL = ["0.5", "0.25", "0.75", "0.1", "0.2", "0.3", "0.4", "0.6", "0.7", "0.8", "0.9", "1.5", "2.5", "0.125", "0.375"]
SHAPES_2D = ["triangle", "square", "rectangle", "pentagon", "hexagon", "circle"]
SHAPES_3D = ["cube", "cuboid", "sphere", "cylinder", "cone", "pyramid"]


def generate_questions():
    """Generate questions.csv and concept_map.csv"""
    questions = []
    concept_map = []
    q_id = 1
    
    for concept, concept_data in CONCEPT_HIERARCHY.items():
        sub_concepts = concept_data.get("sub_concepts", {})
        for sub_concept, config in sub_concepts.items():
            templates = QUESTION_TEMPLATES.get(concept, {}).get(sub_concept, [])
            if not templates:
                templates = [f"Question about {sub_concept} in {concept}"]
            
            for difficulty in DIFFICULTY_LEVELS:
                num_q = config["questions_per_difficulty"]
                for i in range(num_q):
                    question_id = f"Q{q_id:04d}"
                    template = random.choice(templates)
                    
                    text = template
                    expected_answer = ""
                    
                    if concept == "Fractions":
                        if "frac" in template:
                            frac1 = random.choice(FRACTIONS_POOL)
                            frac2 = random.choice(FRACTIONS_POOL)
                            text = template.replace("{frac1}", frac1).replace("{frac2}", frac2)
                        if "denom" in template:
                            text = template.replace("{denom}", str(random.randint(2, 12)))
                        expected_answer = "varies"
                    elif concept == "Decimals":
                        if "decimal" in template:
                            dec = random.choice(DECIMALS_POOL)
                            text = template.replace("{decimal}", dec)
                            text = text.replace("{decimal1}", random.choice(DECIMALS_POOL))
                            text = text.replace("{decimal2}", random.choice(DECIMALS_POOL))
                        if "digit" in template:
                            text = text.replace("{digit}", str(random.randint(0, 9)))
                        expected_answer = "varies"
                    elif concept == "Algebra":
                        if "val" in template:
                            text = text.replace("{val}", str(random.randint(-10, 10)))
                        if "expr" in template:
                            text = text.replace("{expr}", random.choice(["2x+3", "x-5", "3x", "x/2", "x+7"]))
                        if "equation" in template:
                            text = text.replace("{equation}", random.choice(["2x+3=11", "x-5=10", "3x=15", "x/2=4"]))
                        if "pattern" in template:
                            text = text.replace("{pattern}", random.choice(["2, 4, 6, 8, ?", "1, 4, 9, 16, ?", "5, 10, 15, 20, ?"]))
                        if "signed_expr" in template:
                            text = text.replace("{signed_expr}", random.choice(["-5 + -3", "-2 × -4", "6 - -3", "-12 ÷ -3"]))
                        if "word_problem" in template:
                            text = text.replace("{word_problem}", "5 more than a number")
                        expected_answer = "varies"
                    elif concept == "Geometry":
                        if "shape" in template:
                            shape = random.choice(SHAPES_2D + SHAPES_3D)
                            text = text.replace("{shape}", shape)
                        if "description" in template:
                            text = text.replace("{description}", "a shape with 4 equal sides")
                        if "num" in template:
                            text = text.replace("{num}", str(random.randint(4, 8)))
                        if "l" in template:
                            text = text.replace("{l}", str(random.randint(2, 20)))
                        if "b" in template:
                            text = text.replace("{b}", str(random.randint(2, 15)))
                        if "s" in template:
                            text = text.replace("{s}", str(random.randint(2, 15)))
                        if "a" in template:
                            text = text.replace("{a}", str(random.randint(10, 100)))
                        if "deg" in template:
                            text = text.replace("{deg}", str(random.choice([30, 45, 60, 90, 120, 135, 150, 180])))
                        if "angle_problem" in template:
                            text = text.replace("{angle_problem}", "a triangle with angles 50° and 60°")
                        expected_answer = "varies"
                    elif concept == "Measurement":
                        if "val" in template:
                            text = text.replace("{val}", str(random.randint(1, 10)))
                        if "val1" in template:
                            text = text.replace("{val1}", str(random.randint(1, 10)))
                        if "val2" in template:
                            text = text.replace("{val2}", str(random.randint(1, 99)))
                        if "val3" in template:
                            text = text.replace("{val3}", str(random.randint(1, 10)))
                        if "val4" in template:
                            text = text.replace("{val4}", str(random.randint(1, 99)))
                        if "time" in template:
                            text = text.replace("{time}", f"{random.randint(1, 12)}:{random.randint(0, 59):02d}")
                        expected_answer = "varies"
                    elif concept == "Data_Handling":
                        if "range" in template:
                            text = text.replace("{range}", f"{random.randint(0, 50)}-{random.randint(51, 100)}")
                        if "category" in template:
                            text = text.replace("{category}", random.choice(["Apples", "Bananas", "Oranges", "Mangoes"]))
                        if "cat1" in template:
                            text = text.replace("{cat1}", "Apples").replace("{cat2}", "Bananas")
                        if "val" in template:
                            text = text.replace("{val}", str(random.randint(2, 10)))
                        if "num" in template:
                            text = text.replace("{num}", str(random.randint(1, 10)))
                        expected_answer = "varies"
                    
                    questions.append({
                        "question_id": question_id,
                        "text": text,
                        "concept": concept,
                        "sub_concept": sub_concept,
                        "difficulty": DIFFICULTY_LEVELS.index(difficulty) + 1,
                        "expected_answer": expected_answer
                    })
                    
                    concept_map.append({
                        "question_id": question_id,
                        "concept": concept,
                        "sub_concept": sub_concept
                    })
                    
                    q_id += 1
    
    return pd.DataFrame(questions), pd.DataFrame(concept_map)


def generate_students(n=50):
    """Generate students.csv with archetypes"""
    students = []
    archetype_keys = list(ARCHETYPES.keys())
    
    for i in range(1, n + 1):
        archetype_key = archetype_keys[i % len(archetype_keys)]
        archetype = ARCHETYPES[archetype_key]
        
        students.append({
            "student_id": f"Student_{i:03d}",
            "grade": 5,
            "section": chr(ord('A') + (i % 4)),
            "archetype": archetype_key
        })
    
    return pd.DataFrame(students)


def generate_responses(students_df, questions_df, n_assessments=6):
    """Generate responses.csv with longitudinal data"""
    responses = []
    response_id = 1
    
    base_date = datetime(2025, 7, 15)
    
    for assessment_num in range(1, n_assessments + 1):
        assessment_date = base_date + timedelta(weeks=assessment_num * 3)
        assessment_id = f"ASM{assessment_num:03d}"
        
        questions_per_assessment = 20
        selected_questions = questions_df.sample(n=min(questions_per_assessment, len(questions_df)), random_state=assessment_num)
        
        for _, student in students_df.iterrows():
            student_id = student["student_id"]
            archetype_key = student["archetype"]
            archetype = ARCHETYPES[archetype_key]
            
            improvement_factor = 1.0
            if "improvement_rate" in archetype:
                improvement_factor = max(0.3, 1.0 - (assessment_num - 1) * archetype["improvement_rate"])
            
            for _, question in selected_questions.iterrows():
                concept = question["concept"]
                sub_concept = question["sub_concept"]
                difficulty = question["difficulty"]
                
                base_error_rate = archetype["base_error_rates"].get(concept, 0.15)
                error_rate = base_error_rate * ERROR_TYPE_MODIFIER[DIFFICULTY_LEVELS[difficulty - 1]] * improvement_factor
                error_rate = min(0.9, max(0.02, error_rate))
                
                is_correct = np.random.random() > error_rate
                
                if is_correct:
                    student_answer = question["expected_answer"]
                    error_type = ""
                else:
                    config = CONCEPT_HIERARCHY[concept]["sub_concepts"][sub_concept]
                    dominant_errors = archetype.get("dominant_errors", {}).get(concept, [])
                    
                    if dominant_errors and np.random.random() < 0.7:
                        error_type = np.random.choice(dominant_errors)
                    else:
                        error_type = np.random.choice(config["error_types"], p=config["error_probs"])
                    
                    student_answer = f"incorrect_{error_type}"
                
                responses.append({
                    "response_id": f"R{response_id:06d}",
                    "student_id": student_id,
                    "assessment_id": assessment_id,
                    "question_id": question["question_id"],
                    "student_answer": student_answer,
                    "is_correct": is_correct,
                    "error_type": error_type if not is_correct else "",
                    "created_at": assessment_date.isoformat()
                })
                
                response_id += 1
    
    return pd.DataFrame(responses)


def main():
    output_dir = "data/synthetic"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating questions and concept map...")
    questions_df, concept_map_df = generate_questions()
    print(f"Generated {len(questions_df)} questions across {questions_df['concept'].nunique()} concepts")
    
    print("Generating students...")
    students_df = generate_students(50)
    print(f"Generated {len(students_df)} students")
    
    print("Generating responses...")
    responses_df = generate_responses(students_df, questions_df, 6)
    print(f"Generated {len(responses_df)} responses across 6 assessments")
    
    questions_df.to_csv(f"{output_dir}/questions.csv", index=False)
    concept_map_df.to_csv(f"{output_dir}/concept_map.csv", index=False)
    students_df[["student_id", "grade", "section"]].to_csv(f"{output_dir}/students.csv", index=False)
    responses_df.to_csv(f"{output_dir}/responses.csv", index=False)
    
    print("\nFiles written to data/synthetic/:")
    print(f"  - students.csv: {len(students_df)} rows")
    print(f"  - questions.csv: {len(questions_df)} rows")
    print(f"  - concept_map.csv: {len(concept_map_df)} rows")
    print(f"  - responses.csv: {len(responses_df)} rows")
    
    print("\nArchetype distribution:")
    for arch_key, arch in ARCHETYPES.items():
        count = len(students_df[students_df["archetype"] == arch_key])
        print(f"  {arch_key}: {count} students - {arch['description']}")


if __name__ == "__main__":
    main()
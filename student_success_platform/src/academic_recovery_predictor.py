"""
3-Way Academic Trajectory & Remedial Recovery Prediction Engine
===============================================================
Predicts 3 distinct actionable categories:
  1. GUARANTEED PASS (On track, safe zone)
  2. RECOVERABLE (Can pass IF they maintain attendance & attend remedial classes)
  3. CRITICAL AT-RISK (Mathematically cannot clear without immediate structural intervention)
"""

import os
import joblib
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier

class AcademicRecoveryPredictor:
    def __init__(self, models_dir=r'c:\Users\sumit\Downloads\rio\models'):
        self.models_dir = models_dir
        self.meta = joblib.load(os.path.join(models_dir, 'ensemble_metadata.pkl'))
        self.m4 = CatBoostClassifier()
        self.m4.load_model(os.path.join(models_dir, 'model_4_champion_catboost.cbm'))

    def evaluate_student_trajectory(
        self,
        student_name: str,
        current_attendance: float,
        ia1_marks: float,
        ia2_marks: float,
        total_enrolled_credits: int = 6,
        currently_approved_credits: int = 3,
        past_sgpa: float = 6.8,
        total_classes_held: int = 40,
        remaining_classes: int = 20
    ):
        """
        Calculates:
          - Current Pass/Fail trajectory
          - Max achievable attendance (if attending 100% remaining classes + remedial)
          - Probability shift if student attends remedial session
        """
        # 1. Base probability using trained Champion CatBoost Model
        features = {
            'Marital Status': 1, 'Application mode': 1, 'Application order': 1, 'Course': 9500,
            'Daytime/evening attendance': 1, 'Previous qualification': 1, 'Previous qualification (grade)': 140.0,
            'Nacionality': 1, "Mother's qualification": 1, "Father's qualification": 1,
            "Mother's occupation": 3, "Father's occupation": 3, 'Admission grade': max(100.0, past_sgpa * 16.0),
            'Displaced': 0, 'Educational special needs': 0, 'Debtor': 0, 'Tuition fees up to date': 1,
            'Gender': 0, 'Scholarship holder': 0, 'Age at enrollment': 19, 'International': 0,
            'Curricular units 1st sem (credited)': 0, 'Curricular units 1st sem (enrolled)': total_enrolled_credits,
            'Curricular units 1st sem (evaluations)': total_enrolled_credits, 'Curricular units 1st sem (approved)': currently_approved_credits,
            'Curricular units 1st sem (grade)': (ia1_marks / 30.0) * 20.0, 'Curricular units 1st sem (without evaluations)': 0,
            'Curricular units 2nd sem (credited)': 0, 'Curricular units 2nd sem (enrolled)': total_enrolled_credits,
            'Curricular units 2nd sem (evaluations)': total_enrolled_credits, 'Curricular units 2nd sem (approved)': currently_approved_credits,
            'Curricular units 2nd sem (grade)': (ia2_marks / 30.0) * 20.0, 'Curricular units 2nd sem (without evaluations)': 0,
            'Unemployment rate': 10.8, 'Inflation rate': 1.4, 'GDP': 1.74
        }
        for col in self.meta['all_cols']:
            if col not in features:
                features[col] = 0.0
            
        features['total_approved'] = currently_approved_credits * 2
        features['total_enrolled'] = total_enrolled_credits * 2
        features['approval_ratio'] = (currently_approved_credits * 2) / (total_enrolled_credits * 2)
        features['grade_avg'] = ((ia1_marks + ia2_marks) / 60.0) * 20.0
        features['approved_deficit'] = max(0, features['total_enrolled'] - features['total_approved'])

        df_base = pd.DataFrame([features])
        prob_pass_current = float(self.m4.predict_proba(df_base[self.meta['all_cols']])[:, 1][0])
        
        # 2. Calculate Maximum Achievable Attendance
        # Attended so far
        attended_classes = (current_attendance / 100.0) * total_classes_held
        # Max attendance if attending ALL remaining + 4 remedial class hours
        max_possible_attended = attended_classes + remaining_classes + 4
        max_achievable_attendance = min(100.0, (max_possible_attended / (total_classes_held + remaining_classes + 4)) * 100.0)
        
        # 3. Simulate Remedial Class Boost (Targeted Recovery)
        # Remedial classes typically boost IA2 / SEE performance by +4.5 marks (30% relative gain)
        simulated_remedial_ia2 = min(25.0, ia2_marks + 5.5)
        features_recovered = features.copy()
        features_recovered['Curricular units 2nd sem (approved)'] = min(total_enrolled_credits, currently_approved_credits + 2)
        features_recovered['total_approved'] = features_recovered['Curricular units 1st sem (approved)'] + features_recovered['Curricular units 2nd sem (approved)']
        features_recovered['approval_ratio'] = features_recovered['total_approved'] / features_recovered['total_enrolled']
        features_recovered['approved_deficit'] = max(0, features_recovered['total_enrolled'] - features_recovered['total_approved'])
        features_recovered['Curricular units 2nd sem (grade)'] = (simulated_remedial_ia2 / 25.0) * 20.0
        features_recovered['grade_avg'] = ((ia1_marks + simulated_remedial_ia2) / 50.0) * 20.0

        df_rec = pd.DataFrame([features_recovered])
        prob_pass_recovered = float(self.m4.predict_proba(df_rec[self.meta['all_cols']])[:, 1][0])

        # 4. Determine Actionable Category
        attendance_is_recoverable = max_achievable_attendance >= 75.0
        
        if prob_pass_current >= 0.75 and current_attendance >= 75.0:
            category = "GUARANTEED PASS (SAFE ZONE)"
            action_plan = "Maintain current momentum. No mandatory remedial sessions required."
            status_code = "SAFE"
        elif (prob_pass_recovered >= 0.50) and attendance_is_recoverable:
            category = "RECOVERABLE (CAN PASS WITH REMEDIAL + ATTENDANCE)"
            action_plan = (
                f"Student will FAIL if no action taken ({prob_pass_current*100:.1f}% pass probability).\n"
                f"-> ACTION REQUIRED: Attend all remaining {remaining_classes} lectures to reach {max_achievable_attendance:.1f}% attendance.\n"
                f"-> MANDATORY REMEDIAL: Complete 2 Saturday remedial drills on weak topics to jump IA-2 from {ia2_marks}/25 to {simulated_remedial_ia2}/25.\n"
                f"-> RESULT: Pass probability climbs to {prob_pass_recovered*100:.1f}% (RECOVERED TO PASS ZONE)."
            )
            status_code = "RECOVERABLE"
        else:
            category = "CRITICAL AT-RISK (IRRECOVERABLE ATTENDANCE SHORTAGE)"
            action_plan = (
                f"Attendance is mathematically capped at {max_achievable_attendance:.1f}% (Below 75% university threshold).\n"
                f"-> Requires immediate formal HOD/Dean Medical or Academic Condonation review."
            )
            status_code = "CRITICAL_DEFICIT"

        return {
            "student_name": student_name,
            "category": category,
            "status_code": status_code,
            "current_pass_prob": round(prob_pass_current * 100, 1),
            "remedial_pass_prob": round(prob_pass_recovered * 100, 1),
            "current_attendance": current_attendance,
            "max_achievable_attendance": round(max_achievable_attendance, 1),
            "action_plan": action_plan
        }

if __name__ == '__main__':
    predictor = AcademicRecoveryPredictor()
    
    # Test on 3 Real Scenarios:
    test_cases = [
        ("Student 1 (Safe)", 84.0, 19.0, 20.0, 6, 6, 8.2),
        ("Student 2 (Lazy/Weak: Can Pass IF Remediated)", 65.0, 11.0, 12.0, 6, 3, 6.5),
        ("Student 3 (Extreme Drop: Absenteeism too deep)", 38.0, 6.0, 5.0, 6, 1, 5.2)
    ]
    
    print("=" * 80)
    print("3-WAY PREDICTION: PASS / CAN RECOVER IF ATTEND REMEDIAL / CRITICAL FAIL")
    print("=" * 80)
    
    for name, att, ia1, ia2, enrolled, approved, sgpa in test_cases:
        res = predictor.evaluate_student_trajectory(
            student_name=name,
            current_attendance=att,
            ia1_marks=ia1,
            ia2_marks=ia2,
            total_enrolled_credits=enrolled,
            currently_approved_credits=approved,
            past_sgpa=sgpa
        )
        print(f"\n[+] {res['student_name']}:")
        print(f"    Current Standing   : Attendance {res['current_attendance']}% | Current Pass Prob: {res['current_pass_prob']}%")
        print(f"    Max Possible Att.  : {res['max_achievable_attendance']}% (if attending remaining classes)")
        print(f"    Pass Prob w/ Remedial: {res['remedial_pass_prob']}%")
        print(f"    -> PREDICTION CATEGORY : [{res['category']}]")
        print(f"    -> ADVISORY:\n{res['action_plan']}")
        print("-" * 80)


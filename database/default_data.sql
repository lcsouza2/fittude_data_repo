-- Users
INSERT INTO "user" (email, name, password) VALUES
('john.doe@email.com', 'John Doe', 'hashed_password_1'),
('jane.smith@email.com', 'Jane Smith', 'hashed_password_2'),
('bob.wilson@email.com', 'Bob Wilson', 'hashed_password_3'),
('alice.jones@email.com', 'Alice Jones', 'hashed_password_4'),
('mike.brown@email.com', 'Mike Brown', 'hashed_password_5');

-- Muscle Groups (including some NULL user_id for defaults)
INSERT INTO muscle_group (group_name, user_id, active) VALUES
('Upper Body', NULL, true),
('Lower Body', NULL, true),
('Core', 1, true),
('Arms', 2, true),
('Back', 3, true);

-- Equipment (including some NULL user_id for defaults)
INSERT INTO equipment (user_id, group_name, equipment_name, active) VALUES
(NULL, 'Upper Body', 'Barbell', true),
(NULL, 'Lower Body', 'Squat Rack', true),
(1, 'Core', 'Exercise Ball', true),
(2, 'Arms', 'Dumbbells', true),
(3, 'Back', 'Pull-up Bar', true);

-- Muscles (including some NULL user_id for defaults)
INSERT INTO muscle (user_id, group_name, muscle_name, active) VALUES
(NULL, 'Upper Body', 'Chest', true),
(NULL, 'Lower Body', 'Quadriceps', true),
(1, 'Core', 'Abs', true),
(2, 'Arms', 'Biceps', true),
(3, 'Back', 'Lats', true);

-- Exercises (including some NULL user_id for defaults)
INSERT INTO exercise (user_id, exercise_name, description, active) VALUES
(NULL, 'Bench Press', 'Lying on bench, press barbell up', true),
(NULL, 'Squat', 'Stand with barbell, squat down and up', true),
(1, 'Crunches', 'Lie on back, lift shoulders up', true),
(2, 'Bicep Curls', 'Stand with dumbbells, curl up', true),
(3, 'Pull-ups', 'Hang from bar, pull up body', true);

-- Exercise Muscles (relationships)
INSERT INTO exercise_muscle (muscle_id, exercise_id) VALUES
(1, 1),  -- Chest - Bench Press
(2, 2),  -- Quadriceps - Squat
(3, 3),  -- Abs - Crunches
(4, 4),  -- Biceps - Bicep Curls
(5, 5);  -- Lats - Pull-ups

-- Exercise Equipment (relationships)
INSERT INTO exercise_equipment (equipment_id, exercise_id) VALUES
(1, 1),  -- Barbell - Bench Press
(2, 2),  -- Squat Rack - Squat
(3, 3),  -- Exercise Ball - Crunches
(4, 4),  -- Dumbbells - Bicep Curls
(5, 5);  -- Pull-up Bar - Pull-ups

-- Workout Plans
INSERT INTO workout_plan (user_id, workout_plan_name, workout_plan_goal, active) VALUES
(1, 'Beginner Program', 'Build basic strength', true),
(2, 'Intermediate Split', 'Muscle hypertrophy', true),
(3, 'Advanced Training', 'Power development', true),
(4, 'Weight Loss Plan', 'Fat burning', true),
(5, 'Maintenance Plan', 'Maintain fitness', true);

-- Workout Splits
INSERT INTO workout_split (split, workout_plan_id, active) VALUES
('Push', 1, true),
('Pull', 1, true),
('Legs', 2, true),
('Upper Body', 3, true),
('Lower Body', 4, true);

-- Workout Reports
INSERT INTO workout_report (workout_plan_id, report_date, split) VALUES
(1, '2025-06-01', 'Push'),
(1, '2025-06-02', 'Pull'),
(2, '2025-06-01', 'Legs'),
(3, '2025-06-01', 'Upper Body'),
(4, '2025-06-01', 'Lower Body');

-- Split Exercises
INSERT INTO split_exercise (workout_plan_id, split, exercise_id, execution_order, sets, reps, advanced_technique, rest_time, active) VALUES
(1, 'Push', 1, 1, 3, '10', NULL, 90, true),
(1, 'Pull', 5, 1, 3, '8', NULL, 120, true),
(2, 'Legs', 2, 1, 4, '12', 'Drop Set', 120, true),
(3, 'Upper Body', 4, 1, 3, '15', NULL, 60, true),
(4, 'Lower Body', 2, 1, 5, '5', 'Super Set', 180, true);

-- Set Reports
INSERT INTO set_report (workout_report_id, exercise_id, split, workout_plan_id, execution_order, set_number, reps, weight, notes) VALUES
(1, 1, 'Push', 1, 1, 1, '10', 135, 'Felt strong'),
(2, 5, 'Pull', 1, 1, 1, '8', 0, 'Body weight only'),
(3, 2, 'Legs', 2, 1, 1, '12', 225, 'Good form'),
(4, 4, 'Upper Body', 3, 1, 1, '15', 30, 'Light weight'),
(5, 2, 'Lower Body', 4, 1, 1, '5', 315, 'New PR');
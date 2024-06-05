SELECT 
    t1.teacher_id,
    t1.total_assignments,
    t1.grade_A_count
FROM 
    (
        SELECT 
            teacher_id,
            COUNT(*) AS total_assignments,
            SUM(CASE WHEN grade = 'A' THEN 1 ELSE 0 END) AS grade_A_count
        FROM 
            assignments
        WHERE 
            state = 'GRADED'
        GROUP BY 
            teacher_id
    ) AS t1
JOIN 
    (
        SELECT 
            teacher_id,
            MAX(total_assignments) AS max_total_assignments
        FROM 
            (
                SELECT 
                    teacher_id,
                    COUNT(*) AS total_assignments
                FROM 
                    assignments
                WHERE 
                    state = 'GRADED'
                GROUP BY 
                    teacher_id
            )
    ) AS t2
ON 
    t1.teacher_id = t2.teacher_id AND t1.total_assignments = t2.max_total_assignments;


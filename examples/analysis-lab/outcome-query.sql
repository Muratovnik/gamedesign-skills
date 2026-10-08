WITH per_session AS (
    SELECT s.session_id, s.actor_id, s.build_id, s.cohort,
           s.capture_complete, s.expected_resolution_tick,
           COUNT(e.event_id) AS recorded_events,
           COALESCE(MAX(e.sequence_no), 0) AS last_sequence,
           COALESCE(MAX(CASE WHEN e.event_name = 'action_accepted' THEN 1 ELSE 0 END), 0) AS attempted,
           COALESCE(MAX(CASE WHEN e.event_name = :outcome_event
               AND (:before_resolution = 0 OR e.run_tick < s.expected_resolution_tick)
               THEN 1 ELSE 0 END), 0) AS success_event,
           COALESCE(MAX(CASE WHEN e.event_name = 'episode_end' THEN e.run_tick ELSE -1 END), -1) AS end_tick
    FROM sessions s LEFT JOIN events e ON e.session_id = s.session_id AND e.build_id = s.build_id
    WHERE s.build_id = :build_id AND s.cohort = :cohort
    GROUP BY s.session_id
)
SELECT *, CASE
    WHEN capture_complete != 1 OR recorded_events != last_sequence OR end_tick < expected_resolution_tick THEN 'unknown'
    WHEN attempted = 0 THEN 'not_attempted'
    WHEN success_event = 1 THEN 'success'
    ELSE 'failure'
END AS outcome
FROM per_session
ORDER BY session_id;

SELECT
  "table",
  SUM(num_records) as num_records,
  SUM(total_duration_seconds) as total_duration_seconds,
  SUM(rows) as total_rows
FROM (
  SELECT
      t.table,
      SUM(1) as num_records,
      SUM(datediff('second', starttime, endtime)) as total_duration_seconds,
      SUM(rows) as rows,
      'scan' as op_type
  FROM
      stl_scan s
  LEFT JOIN
      svv_table_info t ON t.table_id = s.tbl
  WHERE
    starttime >= %s
  GROUP BY
    t.table

  UNION

  SELECT
      t.table,
      SUM(1) as num_records,
      SUM(datediff('second', starttime, endtime)) as total_duration_seconds,
      SUM(rows) as rows,
      'insert' as op_type
  FROM
      stl_insert s
  LEFT JOIN
      svv_table_info t ON t.table_id = s.tbl
  WHERE
    starttime >= %s
  GROUP BY
    t.table

  UNION

  SELECT
      t.table,
      SUM(1) as num_records,
      SUM(datediff('second', starttime, endtime)) as total_duration_seconds,
      SUM(rows) as rows,
      'delete' as op_type
  FROM
      stl_delete s
  LEFT JOIN
      svv_table_info t ON t.table_id = s.tbl
  WHERE
    starttime >= %s
  GROUP BY
    t.table
)
GROUP BY
  "table"

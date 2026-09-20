# Persistencia Aislamiento

La migración crea claves compuestas con organización, unicidad documental,
índice de principal y RLS forzado. El host debe limpiar settings de tenant en
cada transacción/pool. No se usa `service_role` como prueba de aislamiento y
no se despliega una base real desde Persons.

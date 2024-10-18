-- List Glam rock bands by lifespan
SELECT band_name, (2022 - YEAR(formed)) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;

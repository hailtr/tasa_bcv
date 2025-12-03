CREATE TABLE IF NOT EXISTS `tasa-bcv-api.tasa_bcv.tasas` (
  fecha DATE NOT NULL,
  url STRING NOT NULL,
  monto FLOAT64 NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY fecha
OPTIONS(
  description="BCV exchange rates time series data",
  labels=[("source", "bcv-scraper"), ("type", "exchange-rate")]
);

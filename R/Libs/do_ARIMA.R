#===================================================
# FUNCTION TO DO ARIMA MODELING OF TIME-SERIES DATA
#===================================================
# ARIMA (Autoregressive Integrated MA) of order = c("AR","I","MA")
model.ARIMA <- function(tseries, order = c(0, 0, 1)){
  mod <- arima(tseries, order = order, include.mean = F)
  print(mod)
  mod
}

#==================================
# FUNCTION TO DO ARIMA FORECASTING
#==================================
do.forecast <- function(tseries, tstep = 12){
  library(forecast)
  fit <- auto.arima(tseries,
                    max.p = 3, max.q = 3,
                    max.P = 2, max.Q = 2,
                    max.d = 2, max.D = 1,
                    start.p = 0, start.q = 0,
                    start.P = 0, start.Q = 0,
                    max.order = 5)
#  summary(fit)
  fit.forcast <- forecast(fit, h = tstep)
  print(fit.forcast)

  # plot original data + forecast
  plot(fit.forcast, main = "Forecast", xlab = "", ylab = "")
}
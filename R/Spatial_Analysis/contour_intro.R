# intro code to do contour plot
x <- y <- seq(1, 11, 0.03)
xyz.func <- function(x,y){
  -10.4 + 6.53 * x + 6.53 * y - 0.167 * x^2 - 0.167 * y^2 + 0.05 * x * y
}
gg <- expand.grid(x = x, y = y)
gg$z <- with(gg, xyz.func(x, y))      # need long format for ggplot
library(ggplot2)
library(RColorBrewer)               #for brewer.pal()
print(ggplot() +
        geom_tile(aes(x = x, y = y, fill = z),
                  alpha = 0.5,
                  data = gg) +
        stat_contour(bins = 6,
                     aes(x, y, z = z),
                     color="black",
                     alpha = 0.3,
                     size = 0.6,
                     data = gg) +
        scale_fill_gradientn(name = "Copper",
                             colours = brewer.pal(6, "YlOrRd")) +
        scale_x_continuous(expand = c(0, 0)) +
        scale_y_continuous(expand = c(0, 0)) +
        coord_fixed())
